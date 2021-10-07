from django.urls import path

from spotify_rooms_app.spotify.util import isAuthenticated
from .views import AuthURL, spotifyCallback, IsAuthenticated


# All of these urls link to index.html
# This is because Django will to HTML which React then takes over and renders the correct page
urlpatterns = [
    path("get-auth-url", AuthURL.as_view()),
    path("redirect", spotifyCallback),
    path("is-authenticated", IsAuthenticated.as_view())
]