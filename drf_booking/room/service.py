"""
Сервисный слой для работы с номерами отеля.
"""

from rest_framework import status
from rest_framework.response import Response

from room.serializers import (
    RoomCreateSerializer,
)


class RoomService:
    """
    Класс, реализующий сервисный слой
    для работы с номерами отеля.
    """

    @staticmethod
    def create_room(serializer: RoomCreateSerializer) -> Response:
        """Добавить номер в отель."""

        room = serializer.save()
        return Response(data={"room_id": room.id}, status=status.HTTP_201_CREATED)
