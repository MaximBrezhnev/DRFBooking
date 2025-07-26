"""
Модуль представлений для работы с номерами отеля.
"""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.room.service import RoomService


class RoomViewSet(ModelViewSet):
    """Набор представлений для работы с номерами отеля."""

    lookup_field = "id"
    service = RoomService

    def create(self, request, *args, **kwargs):
        """Добавить номер в отель."""

        return self.service.create_room(request=request)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Удалить номер из отеля."""

        return self.service.delete_room(room_id=kwargs[self.lookup_field])

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Получить список номеров отеля."""

        return self.service.get_room_list(request=request)
