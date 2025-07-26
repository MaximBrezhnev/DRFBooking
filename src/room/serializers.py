"""Сериализаторы для работы с номерами отеля."""

from rest_framework import serializers

from src.room.models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания номера отеля."""

    class Meta:
        model = Room
        fields = ["description", "price_per_night"]


class CreatedRoomReadSerializer(serializers.Serializer):
    """Сериализатор для отображения данных добавленного номера"""

    room_id = serializers.UUIDField()


class RoomReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных номера."""

    class Meta:
        model = Room
        fields = "__all__"
