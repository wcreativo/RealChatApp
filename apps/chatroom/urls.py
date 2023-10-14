from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SendMessageView, ChatRoomViewSet

router = DefaultRouter()
router.register("", ChatRoomViewSet, basename="")


urlpatterns = [
    path("send_messages_chat/", SendMessageView.as_view(), name="send_messages_chat"),
    path("", include(router.urls)),
]
