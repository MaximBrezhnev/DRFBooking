"""Модуль моделей для работы с бронями."""

import uuid

from django.db import models
from room.models import Room


class Booking(models.Model):
    """Модель брони номера."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        help_text="ID брони в БД.",
    )
    date_start = models.DateField(help_text="Дата начала действия брони.")
    date_end = models.DateField(help_text="Дата окончания действия брони.")
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        help_text="Номер, на который оформлена бронь, в БД.",
    )
