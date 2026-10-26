def test_user_bookings_start_empty(isolated_database):
    response = isolated_database.get("/my-bookings")

    assert response.status_code == 200
    assert response.json() == []
