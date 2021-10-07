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

class UpdateRoomSerializer(serializers.ModelSerializer):
    # Need this so that the code isn't checked for being unique (in models)
    room_code = serializers.CharField(validators=[]) # Making a 'new' version of code since we need to pass the current room code
    class Meta:
        model = Room
        fields = ("can_pause", "votes_to_skip", "room_code") # So room_code here uses the one in this class, not the one from the Room model
