"""Сериализаторы для работы с номерами отеля."""

from rest_framework import serializers

from src.room.models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    """"""  # TODO

    class Meta:
        model = Room
        fields = ["description", "price_per_night"]


class CreatedRoomReadSerializer(serializers.Serializer):
    """"""  # TODO

    room_id = serializers.UUIDField()


class RoomReadSerializer(serializers.ModelSerializer):
    """"""  # TODO

    class Meta:
        model = Room
        fields = "__all__"
