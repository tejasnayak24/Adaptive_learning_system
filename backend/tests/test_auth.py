from conftest import register_and_login


def test_register_login_and_profile_returns_student_record(client):
    headers, profile = register_and_login(client, email="asha@example.com", name="Asha Rao")

    assert isinstance(profile["id"], int)
    assert profile["name"] == "Asha Rao"
    assert profile["email"] == "asha@example.com"
    assert profile["age"] == 14
    assert "password_hash" not in profile
    assert "sub" not in profile


def test_duplicate_registration_is_rejected(client):
    register_and_login(client, email="dup@example.com")
    response = client.post(
        "/register",
        json={"name": "X", "email": "dup@example.com", "password": "Passw0rd!", "age": 12},
    )
    assert response.status_code == 400


def test_wrong_password_is_rejected(client):
    register_and_login(client, email="pw@example.com", password="RightPass1!")
    response = client.post("/login", json={"email": "pw@example.com", "password": "nope"})
    assert response.status_code == 401


def test_oauth2_token_endpoint(client):
    register_and_login(client, email="form@example.com", password="FormPass1!")
    response = client.post(
        "/token",
        data={"username": "form@example.com", "password": "FormPass1!"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_profile_requires_valid_token(client):
    assert client.get("/profile").status_code == 401
    assert (
        client.get("/profile", headers={"Authorization": "Bearer not-a-token"}).status_code
        == 401
    )


def test_two_students_get_distinct_ids(client):
    _, first = register_and_login(client, email="one@example.com")
    _, second = register_and_login(client, email="two@example.com")
    assert first["id"] != second["id"]
