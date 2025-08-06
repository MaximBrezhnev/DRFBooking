"""
Сервисный слой для работы с бронями.
"""

import uuid

from booking.models import Booking
from booking.serializers import BookingCreateSerializer, BookingReadSerializer
from rest_framework import status
from rest_framework.response import Response
from room.models import Room


class BookingService:
    """
    Класс, реализующий сервисный слой
    для работы с бронями.
    """

    @staticmethod
    def create_booking(serializer: BookingCreateSerializer) -> Response:
        """Оформить бронь на номер."""

        validated_data = serializer.validated_data

        room_exists = Room.objects.filter(id=validated_data["room_id"]).exists()
        if not room_exists:
            return Response(
                data={"detail": "Related room does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        overlap_exists = Booking.objects.filter(
            room_id=validated_data["room_id"],
            date_start__lt=validated_data["date_end"],
            date_end__gt=validated_data["date_start"],
        ).exists()
        if overlap_exists:
            return Response(
                data={"detail": "The room is already booked for these dates"},
                status=status.HTTP_409_CONFLICT,
            )

        booking = serializer.save()
        return Response(data={"booking_id": booking.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_booking_list(room_id: uuid.UUID) -> Response:
        """Получить список броней на номер."""

        room_exists = Room.objects.filter(id=room_id).exists()
        if not room_exists:
            return Response(
                data={"detail": "Room not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        booking_list = Booking.objects.filter(room_id=room_id).order_by("date_start")
        serializer = BookingReadSerializer(instance=booking_list, many=True)
        return Response(data=serializer.data)
