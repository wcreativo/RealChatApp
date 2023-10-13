from django.urls import path

from .views import index, room, SendMessageView


urlpatterns = [
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
    path("send_message/", SendMessageView.as_view(), name="send_message")
]