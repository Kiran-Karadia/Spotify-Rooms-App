from django.urls import path
from .views import index

app_name = "frontend" # Needed for the redirect in spotify/views.py (spotifyCallback function)

# All of these urls link to index.html
# This is because Django will to HTML which React then takes over and renders the correct page
urlpatterns = [
    path("", index, name=""), # Same here, needed for the spotifyCallback function 
    path("join", index,),
    path("create", index),
    path("room/<str:roomCode>", index), # Dynamic URL using the current room code
    path("info", index)
]