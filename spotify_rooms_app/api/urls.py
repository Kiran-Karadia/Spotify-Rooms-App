# All URLs that are local to this app (api app)


from django.urls import path
from .views import RoomView, CreateRoomView # Import the RoomView class from /views.py


urlpatterns = [
    path("room", RoomView.as_view()),
    path("create", CreateRoomView.as_view())  
]