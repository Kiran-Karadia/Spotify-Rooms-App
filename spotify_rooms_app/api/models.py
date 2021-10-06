from django.db import models
import string
import random

# Like a table in a database but Django uses models
# Takes Python code and does all the database stuff

# Create your models here.
# Django says to put most logic in models - Fat models, thin views


def generateRoomCode():
    code_length = 4

    while True:
        # Generate random upper case ascii code of length code_length
        code = "".join(random.choices(string.ascii_uppercase, k=code_length))

        # Check if code is unique
        if Room.objects.filter(room_code=code).count() == 0:    
            break

    return code

# Model for a 'music room'
class Room(models.Model):
    room_code = models.CharField(max_length=4, default=generateRoomCode, unique=True) # Unique code to identify a room
    host = models.CharField(max_length=50, unique=True)                 # Unique code to identify the host
    can_pause = models.BooleanField(null=False, default=False)          # Flag to determine if guests can pause the music
    votes_to_skip = models.IntegerField(null=False, default=1)          # Number of votes needed to skip current song
    created_at = models.DateTimeField(auto_now_add=True)                # Automatically get date and time info when a room is created