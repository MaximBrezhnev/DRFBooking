"""Модуль тестирования набора представления для работы с бронированиями номеров отеля."""

import uuid
from datetime import date

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from booking.models import Booking


# MARK: POST
def test_create_booking(
    db, api_client: APIClient, booking_create_data: dict[str, uuid.UUID | date]
):
    """
    Возможно забронировать номер.
    """

    response = api_client.post(
        path="/api/v1/booking/",
        data=booking_create_data,
        format="json",
    )

    created_booking_db = Booking.objects.get()
    assert isinstance(created_booking_db.id, uuid.UUID)
    assert created_booking_db.date_start == booking_create_data["date_start"]
    assert created_booking_db.date_end == booking_create_data["date_end"]

    assert response.data["booking_id"] == created_booking_db.id
    assert response.status_code == status.HTTP_201_CREATED


def test_create_booking_invalid_dates(
    api_client: APIClient,
    booking_create_date_invalid_dates: dict[str, uuid.UUID | date],
):
    """
    Нельзя забронировать номер, передав некорректные диапазон дат для бронирования.
    """

    response = api_client.post(
        path="/api/v1/booking/",
        data=booking_create_date_invalid_dates,
        format="json",
    )

    assert response.data == {
        "non_field_errors": [
            ErrorDetail(
                string="The start date cannot be later than the end date.",
                code="invalid",
            )
        ]
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_booking_room_not_found(
    db,
    api_client: APIClient,
    booking_create_data_not_existing_room: dict[str, uuid.UUID | date],
):
    """
    Нельзя забронировать несуществующий номер.
    """

    response = api_client.post(
        path="/api/v1/booking/",
        data=booking_create_data_not_existing_room,
        format="json",
    )

    assert response.data == {"detail": "Related room does not exist"}
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_booking_room_already_booked(
    api_client: APIClient,
    booking_db: Booking,
    booking_create_data: dict[str, uuid.UUID | date],
):
    """
    Нельзя забронировать номер на даты, когда он уже был забронирован.

    *Фикстура `booking_db` передана для создания в БД записи о брони, пересекающейся
    с создаваемой*
    """

    response = api_client.post(
        path="/api/v1/booking/",
        data=booking_create_data,
        format="json",
    )

    assert response.data == {"detail": "The room is already booked for these dates"}
    assert response.status_code == status.HTTP_409_CONFLICT


# MARK: GET
def test_get_booking_list(
    api_client: APIClient,
    booking_db: Booking,
    second_booking_db: Booking,
):
    """
    Возможно получить список бронирований номера отеля.
    """

    response = api_client.get(
        path=f"/api/v1/booking/room/{booking_db.room_id}/",
    )

    received_bookings = response.data
    assert len(received_bookings) == 2

    first_received_booking = received_bookings[0]
    second_received_booking = received_bookings[1]

    assert first_received_booking["id"] == str(booking_db.id)
    assert first_received_booking["date_start"] == str(booking_db.date_start)
    assert first_received_booking["date_end"] == str(booking_db.date_end)

    assert second_received_booking["id"] == str(second_booking_db.id)
    assert second_received_booking["date_start"] == str(second_booking_db.date_start)
    assert second_received_booking["date_end"] == str(second_booking_db.date_end)

    assert response.status_code == status.HTTP_200_OK


def test_get_booking_list_room_not_found(
    db,
    api_client: APIClient,
):
    """
    Нельзя получить список бронирований несуществующего номера.
    """

    response = api_client.get(path=f"/api/v1/booking/room/{uuid.uuid4()}/")

    assert response.data == {"detail": "Room not found"}
    assert response.status_code == status.HTTP_404_NOT_FOUND


# MARK: DELETE
def test_delete_booking(
    booking_db: Booking,
    api_client: APIClient,
):
    """
    Возможно удалить бронь номера отеля.
    """

    response = api_client.delete(path=f"/api/v1/booking/{booking_db.id}/")

    assert response.data is None

    assert not Booking.objects.exists()

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_booking_not_found(db, api_client: APIClient):
    """
    Нельзя удалить несуществующую бронь номера отеля.
    """

    response = api_client.delete(path=f"/api/v1/booking/{uuid.uuid4()}/")

    assert response.data == {
        "detail": ErrorDetail(
            string="No Booking matches the given query.", code="not_found"
        )
    }
    assert response.status_code == status.HTTP_404_NOT_FOUND
