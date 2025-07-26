"""
Сервисный слой для работы с номерами отеля.
"""

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

    @classmethod
    def create_room(cls, request: Request) -> Response:
        """
        #TODO
        """

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

    @classmethod
    def get_room_list(cls, request: Request) -> Response:
        """
        #TODO
        """

        sort_by = request.GET.get("sort_by", "created_at")
        order = request.GET.get("order", "asc")

        if sort_by not in ["price_per_night", "created_at"]:
            sort_by = "created_at"

        if order == "desc":
            sort_by = "-" + sort_by

        rooms = Room.objects.all().order_by(sort_by)
        serializer = RoomReadSerializer(rooms, many=True)
        return Response(serializer.data)
