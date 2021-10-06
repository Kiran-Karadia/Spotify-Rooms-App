from django.db.models import query
from django.shortcuts import render
from rest_framework import generics, serializers, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
# This is where all the endpoints are

class RoomView(generics.CreateAPIView): #CreateAPIView gives the form that can be filled out to create a room
    # To view a room and create a room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self, request, format=None):
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

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
