def test_user_bookings_start_empty(isolated_database):
    response = isolated_database.get("/my-bookings")

    assert response.status_code == 200
    assert response.json() == []


def test_list_bookings_for_room_returns_only_that_room(isolated_database):
    booking = {
        "room_id": 1,
        "booking_date": "2026-10-28",
        "start_time": "10:00",
        "end_time": "11:00",
    }
    created_response = isolated_database.post("/book-room", json=booking)

    assert created_response.status_code == 200

    response = isolated_database.get("/rooms/1/bookings")
    other_room_response = isolated_database.get("/rooms/2/bookings")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["room_id"] == 1
    assert other_room_response.status_code == 200
    assert other_room_response.json() == []


def test_list_bookings_for_unknown_room_returns_not_found(isolated_database):
    response = isolated_database.get("/rooms/999/bookings")

    assert response.status_code == 404
