"""Модуль моделей для работы с номерами отеля."""

import uuid

from django.db import models


class RoomModel(models.Model):
    """Модель номера отеля."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        help_text="ID номера в БД.",
    )
    description = models.TextField(help_text="Описание номера.")
    price_per_night = models.DecimalField(help_text="Цена за ночь за номер.")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время добавления номера."
    )
