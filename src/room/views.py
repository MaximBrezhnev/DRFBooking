"""
Модуль представлений для работы с номерами отеля.
"""

from http import HTTPMethod

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.room.service import RoomService


@api_view([HTTPMethod.POST])
def create_room(request: Request) -> Response:
    """
    Добавить номер в отель.
    """

    return RoomService.create_room(request=request)


@api_view([HTTPMethod.GET])
def get_room_list(request: Request) -> Response:
    """
    Получить список номеров отеля.
    """

    return RoomService.get_room_list(request=request)
