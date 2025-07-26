"""
Сервисный слой для работы с номерами отеля.
"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.room.serializers import (
    RoomCreateSerializer,
)


class RoomService:
    """
    Класс, реализующий сервисный слой
    для работы с номерами отеля.
    """

    @staticmethod
    def create_room(request: Request) -> Response:
        """Добавить номер в отель."""

        serializer = RoomCreateSerializer(data=request.data)

        if serializer.is_valid():
            room = serializer.save()
            return Response(data={"room_id": room.id}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
