from django.shortcuts import render
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room
# Create your views here.
# This is where all the endpoints are

class RoomView(generics.CreateAPIView): #CreateAPIView gives the form that can be filled out to create a room
    # To view a room and create a room
    queryset = Room.objects.all()
    serializer_class = RoomSerializer