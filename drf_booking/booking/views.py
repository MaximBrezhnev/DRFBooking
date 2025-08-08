"""
Модуль представлений для работы с бронями номеров.
"""

import uuid
from http import HTTPMethod

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingCreateSerializer
from booking.service import BookingService


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Набор представлений для работы с бронями."""

    service = BookingService
    queryset = Booking.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Оформить бронь на номер."""

        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.service.create_booking(serializer=serializer)

    @action(detail=False, methods=[HTTPMethod.GET], url_path="room/(?P<room_id>[^/.]+)")
    def get_booking_list(self, request: Request, room_id: uuid.UUID) -> Response:
        """Получить список броней, относящихся к номеру отеля."""

        return self.service.get_booking_list(room_id=room_id)
