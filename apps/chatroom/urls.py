from django.urls import path

from .views import SendMessageView


urlpatterns = [
    path("send_messages_chat/", SendMessageView.as_view(), name="send_messages_chat"),
]