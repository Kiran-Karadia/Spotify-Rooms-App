# All URLs that are local to this app (api app)


from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom # Import views from /views.py


urlpatterns = [
    path("room", RoomView.as_view()),
    path("create-room", CreateRoomView.as_view()),
    path("get-room", GetRoom.as_view())
]