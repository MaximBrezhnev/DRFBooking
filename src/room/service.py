"""
Сервисный слой для работы с номерами отеля.
"""

import uuid

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.room.models import Room
from src.room.serializers import (
    CreatedRoomReadSerializer,
    RoomCreateSerializer,
    RoomReadSerializer,
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
            response_serializer = CreatedRoomReadSerializer(
                instance={"room_id": room.id}
            )
            return Response(
                data=response_serializer.data, status=status.HTTP_201_CREATED
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_room_list(request: Request) -> Response:
        """Получить список номеров отеля."""

        sort_by = request.GET.get("sort_by", "created_at")
        order = request.GET.get("order", "asc")

        if sort_by not in ["price_per_night", "created_at"]:
            sort_by = "created_at"
        if order == "desc":
            sort_by = "-" + sort_by

        rooms = Room.objects.all().order_by(sort_by)
        serializer = RoomReadSerializer(rooms, many=True)
        return Response(serializer.data)

    @staticmethod
    def delete_room(room_id: uuid.UUID) -> Response:
        """Удалить номер из отеля."""

        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Room.DoesNotExist:
            return Response(
                data={"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )
