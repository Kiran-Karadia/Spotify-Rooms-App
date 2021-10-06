from django.urls import path
from .views import index


# All of these urls link to index.html
# This is because Django will to HTML which React then takes over and renders the correct page
urlpatterns = [
    path("", index),
    path("join", index),
    path("create", index),
    path("room/<str:roomCode>", index) # Dynamic URL using the current room code
]