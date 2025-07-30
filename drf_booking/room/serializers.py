"""Сериализаторы для работы с номерами отеля."""

from rest_framework import serializers
from room.models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания номера отеля."""

    class Meta:
        model = Room
        fields = ["description", "price_per_night"]


class RoomReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных номера."""

    class Meta:
        model = Room
        fields = "__all__"
