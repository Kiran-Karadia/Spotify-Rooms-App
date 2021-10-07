# All URLs that are local to this app (api app)


from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoomView, UserInRoom, LeaveRoom # Import views from /views.py


urlpatterns = [
    path("room", RoomView.as_view()),
    path("create-room", CreateRoomView.as_view()),
    path("get-room", GetRoom.as_view()),
    path("join-room", JoinRoomView.as_view()),
    path("user-in-room", UserInRoom.as_view()),
    path("leave-room", LeaveRoom.as_view())
]