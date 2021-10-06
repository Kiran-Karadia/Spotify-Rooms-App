# All URLs that are local to this app (api app)


from django.urls import path
from .views import RoomView # Import the RoomView class from /views.py

urlpatterns = [
    path("room", RoomView.as_view()) 
]