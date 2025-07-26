"""
Сервисный слой для работы с номерами отеля.
"""

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.room.dao import RoomDAO
from src.room.serializers import RoomSerializer


class RoomService:
    """
    Класс, реализующий сервисный слой
    для работы с номерами отеля.
    """

    base_dao = RoomDAO

    @classmethod
    def create_room(cls, request: Request) -> Response:
        """
        #TODO
        """

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
