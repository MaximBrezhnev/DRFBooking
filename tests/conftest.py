"""Модуль фикстур для тестирования."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from booking.models import Booking
from faker import Faker
from rest_framework.test import APIClient
from room.models import Room

# MARK: Common
faker = Faker()


@pytest.fixture
def api_client() -> APIClient:
    """Получить тестового клиента."""

    return APIClient()


# MARK: Room
@pytest.fixture
def room_create_data() -> dict[str, str]:
    """
    Подготовить данные для отправки в теле запроса с
    целью добавления номера.
    """

    return {
        "description": faker.text(),
        "price_per_night": str(
            faker.pyfloat(positive=True, left_digits=7, right_digits=2)
        ),
    }


@pytest.fixture
def invalid_room_create_data() -> dict[str, str]:
    """
    Подготовить некорректные данные для отправки в теле запроса
    с целью добавления номера.
    """

    return {
        "price_per_night": str(
            faker.pyfloat(positive=True, left_digits=7, right_digits=2)
        )
    }


@pytest.fixture
def room_db(db, room_create_data: dict[str, str | float]) -> Room:
    """Создать номер отеля в БД."""

    return Room.objects.create(**room_create_data)


@pytest.fixture
def second_room_db(db, room_create_data: dict[str, str]) -> Room:
    """
    Создать второй номер отеля в БД.

    Цена указана как большая, чем у первого номера, для проверки сортировки
    номеров при их получении в списке.
    """

    return Room.objects.create(
        description=faker.text(),
        price_per_night=Decimal(room_create_data["price_per_night"])
        + Decimal(str(faker.pyfloat(positive=True, left_digits=7, right_digits=2))),
    )


# MARK: Booking
@pytest.fixture
def booking_db(room_db: Room) -> Booking:
    """Создать в БД бронь первого номера."""

    return Booking.objects.create(
        room=room_db,
        date_start=datetime.now(tz=timezone.utc).date(),
        date_end=datetime.now(tz=timezone.utc).date() + timedelta(days=7),
    )
