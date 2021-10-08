from django.urls import path
from .views import *


# All of these urls link to index.html
# This is because Django will to HTML which React then takes over and renders the correct page
urlpatterns = [
    path("get-auth-url", AuthURL.as_view()),
    path("redirect", spotifyCallback),
    path("is-authenticated", IsAuthenticated.as_view()),
    path("current-song", CurrentSong.as_view()),
    path("pause-song", PauseSong.as_view()),
    path("play-song", PlaySong.as_view())

]