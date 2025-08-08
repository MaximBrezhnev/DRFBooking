"""
Сериализаторы для работы с бронями.
"""

from rest_framework import serializers

from booking.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания брони на номер."""

    room_id = serializers.UUIDField()

    class Meta:
        model = Booking
        fields = ["room_id", "date_start", "date_end"]

    def validate(self, data):
        if data["date_start"] > data["date_end"]:
            raise serializers.ValidationError(
                "The start date cannot be later than the end date."
            )
        return data


class BookingReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения брони на номер."""

    class Meta:
        model = Booking
        fields = ["id", "date_start", "date_end"]
