from django.http import response
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import updateOrCreateUserTokens, isAuthenticated


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

    if not request.session.exists(request.sessions.session_key):
        request.session.create()

    updateOrCreateUserTokens(session_key=request.sessions.session_key, access_token=access_token, token_type=token_type, expires_in=expires_in)

    return redirect("frontend:")

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = isAuthenticated(self.request.session.session_key)
        return Response({"status": is_authenticated}, status=status.HTTP_200_OK) 