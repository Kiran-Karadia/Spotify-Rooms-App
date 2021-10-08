from django.shortcuts import redirect, render
from rest_framework.response import Response
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from .models import Vote

# Create your views here.
class AuthURL(APIView):
    def get(self, request, format=None):
        # Scope of what information we want access to
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        url = Request("GET", "https://accounts.spotify.com/authorize", params={
            "scope": scopes,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID
        }).prepare().url
        
        return Response({"url": url}, status=status.HTTP_200_OK)


def spotifyCallback(request, format=None):
    code = request.GET.get("code")
    error = request.GET.get("error")

    response = post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    updateOrCreateUserTokens(session_key=request.session.session_key, access_token=access_token, token_type=token_type, refresh_token=refresh_token, expires_in=expires_in)

    return redirect("frontend:")

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = isAuthenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK) 


class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(room_code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        host = room.host
        endpoint = "player/currently-playing"
        # host is the session_key (we decided that earlier)
        response = executeSpotifyApiRequest(host, endpoint) # Dont need post_, put_ since this is a get request
        

        if "error" in response or "item" not in response: 
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Can find how these are found in the API view at spotify/current-song
        item = response.get("item")
        duration = item.get("duration_ms")
        progress = response.get("progress_ms")
        album_cover = item.get("album").get("images")[0].get("url")
        is_playing = response.get("is_playing")
        song_id = item.get("id")
    
        # This will handle the case of having multiple artists, spotify does it weird
        artist_string = ""
        for i, artist in enumerate(item.get("artists")):
            if i > 0:
                artist_string += ", "
            name = artist.get("name")
            artist_string += name

        votes = len(Vote.objects.filter(room=room, song_id=song_id))

        song = { # All the information needed for the current song
            "title": item.get("name"),
            "artist": artist_string,
            "duration": duration,
            "time": progress,
            "image_url": album_cover,
            "is_playing": is_playing,
            "votes": votes,
            "votes_needed": room.votes_to_skip,
            "id": song_id
        }

        self.updateRoomSong(room, song_id)

        return Response(song, status=status.HTTP_200_OK)

    def updateRoomSong(self, room, song_id):
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=["current_song"])
            votes = Vote.objects.filter(room=room).delete()

class PauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(room_code=room_code)[0]

        if self.request.session.session_key == room.host or room.can_pause: # Check if use is a host or room has guest permissions
            pauseSong(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(room_code=room_code)[0]

        if self.request.session.session_key == room.host or room.can_pause: # Check if use is a host or room has guest permissions
            playSong(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(room_code=room_code)[0]
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip


        if self.request.session.session_key == room.host or len(votes)+1 >= votes_needed:
            votes.delete()
            skipSong(room.host)
        else:
            vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)