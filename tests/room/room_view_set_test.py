"""Модуль тестирования набора представления для работы с номерами отеля."""

import uuid
from decimal import Decimal

import pytest
from booking.models import Booking
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from room.models import Room


# MARK: POST
@pytest.mark.django_db
def test_create_room(api_client: APIClient, room_create_data: dict[str, str]) -> None:
    """Возможно добавить номер в отель."""

    response = api_client.post(
        path="/api/v1/room/",
        data=room_create_data,
        format="json",
    )

    room = Room.objects.get()
    assert isinstance(room.id, uuid.UUID)
    assert room.description == room_create_data["description"]
    assert room.price_per_night == Decimal(room_create_data["price_per_night"])

    response_data = response.data
    assert len(response_data) == 1
    assert response_data["room_id"] == room.id

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_room_invalid_data(
    api_client: APIClient, invalid_room_create_data: dict[str, float]
) -> None:
    """Невозможно добавить номер в отель, передав некорректные данные."""

    response = api_client.post(
        path="/api/v1/room/",
        data=invalid_room_create_data,
        format="json",
    )

    assert response.data == {
        "description": [ErrorDetail(string="This field is required.", code="required")]
    }

    assert not Room.objects.exists()

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# MARK: GET
@pytest.mark.django_db
def test_get_room_list(
    api_client: APIClient,
    room_db: Room,
    second_room_db: Room,
) -> None:
    """Возможно получить несортированный список номеров отеля."""

    response = api_client.get(path="/api/v1/room/")

    response_data = response.data
    assert len(response_data) == 2

    if response_data[0]["id"] == str(room_db.id):
        received_room = response_data[0]
        second_received_room = response_data[1]
    else:
        received_room = response_data[1]
        second_received_room = response_data[0]

    assert received_room["id"] == str(room_db.id)
    assert received_room["description"] == room_db.description
    assert Decimal(received_room["price_per_night"]) == Decimal(room_db.price_per_night)

    assert second_received_room["id"] == str(second_room_db.id)
    assert second_received_room["description"] == second_room_db.description
    assert (
        Decimal(second_received_room["price_per_night"])
        == second_room_db.price_per_night
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_room_list_sorted(
    api_client: APIClient,
    room_db: Room,
    second_room_db: Room,
) -> None:
    """Возможно получить отсортированный список номеров отеля."""

    response = api_client.get(
        path="/api/v1/room/", query_params={"ordering": "-price_per_night"}
    )

    response_data = response.data
    assert len(response_data) == 2

    first_received_room = response_data[0]
    second_received_room = response_data[1]

    assert first_received_room["id"] == str(second_room_db.id)
    assert first_received_room["description"] == second_room_db.description
    assert (
        Decimal(first_received_room["price_per_night"])
        == second_room_db.price_per_night
    )

    assert second_received_room["id"] == str(room_db.id)
    assert second_received_room["description"] == room_db.description
    assert Decimal(second_received_room["price_per_night"]) == Decimal(
        room_db.price_per_night
    )

    assert response.status_code == status.HTTP_200_OK


# MARK: DELETE
@pytest.mark.django_db
def test_delete_room(api_client: APIClient, booking_db: Booking) -> None:
    """Возможно удалить из отеля номер и все его брони."""

    response = api_client.delete(path=f"/api/v1/room/{booking_db.room_id}/")

    assert response.data is None

    assert not Room.objects.filter(id=booking_db.room_id).exists()
    assert not Booking.objects.filter(id=booking_db.id).exists()

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_room_not_found(api_client: APIClient) -> None:
    """Невозможно удалить несуществующий номер отеля."""

    response = api_client.delete(path=f"/api/v1/room/{uuid.uuid4()}/")

    assert response.data == {
        "detail": ErrorDetail(
            string="No Room matches the given query.", code="not_found"
        )
    }
    assert response.status_code == status.HTTP_404_NOT_FOUND
