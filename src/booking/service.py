"""
Сервисный слой для работы с бронями.
"""
import uuid
from datetime import date

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.booking.models import Booking
from src.booking.serializers import BookingCreateSerializer, BookingReadSerializer
from src.room.models import Room


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
                data={"detail": "Related room does not exist"}, status=status.HTTP_400_BAD_REQUEST,
            )

        overlap_exists = (
            Booking.objects.filter(
                room_id=validated_data["room_id"],
                start_date__lt=validated_data["start_date"],
                end_date__gt=validated_data["end_date"]
            )
            .exists()
        )
        if overlap_exists:
            return Response(
                data={"detail": "The room is already booked for these dates", "status": status.HTTP_409_CONFLICT}
            )

        booking = serializer.save()
        return Response(data={"booking_id": booking.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_booking(booking_id: uuid.UUID) -> Response:
        """Снять бронь с номера."""

        try:
            room = Booking.objects.get(id=booking_id)
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Booking.DoesNotExist:
            return Response(
                data={"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def get_booking_list(room_id: uuid.UUID) -> Response:
        """Получить список броней на номер."""

        booking_list = Booking.objects.filter(room_id=room_id).order_by('date_start')
        serializer = BookingReadSerializer(instance=booking_list, many=True)
        return Response(data=serializer.data)


