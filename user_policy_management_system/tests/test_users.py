def make_user(email="aakash@example.com"):
    return {
        "uname": "Aakash",
        "uemail": email,
        "uage": 25,
        "uphone": "9876543210",
        "uaddress": "Indore",
    }


def make_policy(uid):
    return {
        "uid": uid,
        "pname": "Health Secure",
        "ptype": "Health",
        "ppremium": 15000,
        "psumassured": 500000,
    }


def test_user_crud(client):
    response = client.post("/users/", json=make_user())
    assert response.status_code == 201

    uid = response.json()["uid"]

    assert client.get("/users/").status_code == 200
    assert client.get(f"/users/{uid}").status_code == 200

    response = client.put(
        f"/users/{uid}",
        json={"uname": "Aakash Rathor"},
    )
    assert response.status_code == 200
    assert response.json()["uname"] == "Aakash Rathor"

    assert client.delete(f"/users/{uid}").status_code == 204
    assert client.get(f"/users/{uid}").status_code == 404


def test_duplicate_email_is_not_allowed(client):
    assert client.post("/users/", json=make_user()).status_code == 201
    assert client.post("/users/", json=make_user()).status_code == 409


def test_pydantic_validation(client):
    payload = make_user("invalid-test@example.com")
    payload["uage"] = 15

    response = client.post("/users/", json=payload)

    assert response.status_code == 422


def test_user_cannot_be_deleted_when_policy_exists(client):
    user_response = client.post("/users/", json=make_user())
    uid = user_response.json()["uid"]

    policy_response = client.post(
        "/policies/",
        json=make_policy(uid),
    )
    assert policy_response.status_code == 201

    delete_response = client.delete(f"/users/{uid}")

    assert delete_response.status_code == 409


def test_policy_requires_existing_user(client):
    response = client.post(
        "/policies/",
        json=make_policy(99999),
    )

    assert response.status_code == 404
