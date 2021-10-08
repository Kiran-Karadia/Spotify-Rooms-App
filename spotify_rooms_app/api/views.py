from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.
# This is where all the endpoints are



class RoomView(generics.ListAPIView): #CreateAPIView gives the form that can be filled out to create a room
    # To view a room and create a room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_code"

    def get(self, request, format=None):
        room_code = request.GET.get(self.lookup_url_kwarg)
        if room_code != None:
            room = Room.objects.filter(room_code=room_code)
            if room.exists():
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host # Look at the session key and if it's the same as the room's then the current user is a host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"Bad Request": "Code parameter not found in request"}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self, request, format=None): # Check if they have an active session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            can_pause = serializer.data.get("can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)

            if queryset.exists():
                room = queryset[0]
                room.can_pause = can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, can_pause=can_pause, votes_to_skip=votes_to_skip)
                room.save()

            self.request.session['room_code'] = room.room_code
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoomView(APIView):
    
    lookup_url_kwarg = "room_code"
    def post(self, request, formate=None): # Check if they have an active session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        room_code = request.data.get(self.lookup_url_kwarg)
        if room_code != None:
            room_result = Room.objects.filter(room_code=room_code)
            if room_result.exists():
                room = room_result[0]
                self.request.session['room_code'] = room_code # Used for backend, 'this user is in this room'
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)

            return Response({"Bad Request": "Invalid room code!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"Bad Request": "Invalid post data"}, status=status.HTTP_400_BAD_REQUEST)

class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {
            "room_code": self.request.session.get("room_code")

        }
        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if room_results.exists():
                room = room_results[0]
                room.delete()
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    def patch(self, request, format=None): # Usually use patch to update something, maybe change above method?
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            can_pause = serializer.data.get("can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            room_code = serializer.data.get("room_code")

            queryset = Room.objects.filter(room_code=room_code)
            if not queryset.exists():
                return Response({"msg": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({"msg": "RYou are not the host!"}, status=status.HTTP_403_FORBIDDEN)
            room.can_pause = can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=["can_pause", "votes_to_skip"])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({"Bad Request": "Invalid Data!"}, status=status.HTTP_400_BAD_REQUEST)


        
