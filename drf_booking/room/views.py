"""
Модуль представлений для работы с номерами отеля.
"""

from rest_framework import filters, mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from room.models import Room
from room.serializers import RoomCreateSerializer, RoomReadSerializer
from room.service import RoomService


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Набор представлений для работы с номерами отеля."""

    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price_per_night", "created_at"]
    ordering = ["created_at"]

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Добавить номер в отель."""

        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return RoomService.create_room(serializer=serializer)
