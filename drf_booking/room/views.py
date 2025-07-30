"""
Модуль представлений для работы с номерами отеля.
"""

from rest_framework import filters, mixins, viewsets
from room.models import Room
from room.serializers import RoomReadSerializer
from room.service import RoomService


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Набор представлений для работы с номерами отеля."""

    lookup_field = "id"
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price_per_night", "created_at"]
    ordering = ["created_at"]

    def create(self, request, *args, **kwargs):
        """Добавить номер в отель."""

        return RoomService.create_room(request=request)
