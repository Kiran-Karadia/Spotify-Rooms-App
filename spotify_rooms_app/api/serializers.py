# Takes the information from a Django model and transform into a JSON response

from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # All fields are the same as Room model in models.py
        # "id" field is automatically added as a unique key for every room model
        fields = ("id", "room_code", "host", "can_pause", "votes_to_skip", "created_at")

# Ensure data in post request is valid and fits the correct ields
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("can_pause", "votes_to_skip")
