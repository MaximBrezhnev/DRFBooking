"""Сериализаторы для работы с номерами отеля."""

from rest_framework import serializers

from src.room.models import RoomModel


class RoomSerializer(serializers.ModelSerializer):
    """"""  # TODO

    class Meta:
        model = RoomModel
        fields = ["description", "price_per_night"]
