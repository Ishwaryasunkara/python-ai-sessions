def create_user(client, email="asha@example.com"):
    response = client.post(
        "/users/",
        json={"uname": "Asha", "uemail": email},
    )
    assert response.status_code == 200
    return response.json()


def test_authentication_required(client):
    no_token = client.get("/users/", headers={"Authorization": ""})
    assert no_token.status_code == 401
    assert no_token.json()["detail"] == "Bearer token required"

    invalid_token = client.get(
        "/users/",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert invalid_token.status_code == 401
    assert invalid_token.json()["detail"] == "Invalid or expired token"


def test_user_crud(client):
    user = create_user(client)
    assert user["uid"] == 1

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [user]

    response = client.put(
        f"/users/{user['uid']}",
        json={"uname": "Asha Singh", "uemail": "asha.singh@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["uname"] == "Asha Singh"

    response = client.delete(f"/users/{user['uid']}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    assert client.get(f"/users/{user['uid']}").status_code == 404


def test_user_validation_errors(client):
    create_user(client)

    duplicate = client.post(
        "/users/",
        json={"uname": "Other", "uemail": "asha@example.com"},
    )
    assert duplicate.status_code == 400
    assert duplicate.json()["detail"] == "Email already exists"

    assert client.get("/users/999").status_code == 404
    assert client.put(
        "/users/999",
        json={"uname": "Missing", "uemail": "missing@example.com"},
    ).status_code == 404
    assert client.delete("/users/999").status_code == 404


def test_policy_crud_and_owner_validation(client):
    user = create_user(client)
    policy_data = {"pname": "Health", "ptype": "Medical", "uid": user["uid"]}

    created = client.post("/policies/", json=policy_data)
    assert created.status_code == 200
    policy = created.json()
    assert policy["pname"] == "Health"
    assert policy["ptype"] == "Medical"

    updated = client.put(
        f"/policies/{policy['pid']}",
        json={
            "pid": policy["pid"],
            "pname": "Dental",
            "ptype": "Vision",
            "status": "INACTIVE",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["pname"] == "Dental"

    assert client.get("/policies/").json() == [updated.json()]
    assert client.get(f"/policies/{policy['pid']}").json() == updated.json()
    assert client.delete(f"/policies/{policy['pid']}").status_code == 200
    assert client.get(f"/policies/{policy['pid']}").status_code == 404

    missing_owner = client.post(
        "/policies/",
        json={"pname": "Travel", "ptype": "Trip", "uid": 999},
    )
    assert missing_owner.status_code == 404


def test_active_policy_blocks_user_deletion(client):
    user = create_user(client)
    policy = client.post(
        "/policies/",
        json={"pname": "Life", "ptype": "Protection", "uid": user["uid"]},
    ).json()

    blocked = client.delete(f"/users/{user['uid']}")
    assert blocked.status_code == 400
    assert blocked.json()["detail"] == (
        "User cannot be deleted because active policies exist"
    )

    assert client.delete(f"/policies/{policy['pid']}").status_code == 200
    assert client.delete(f"/users/{user['uid']}").status_code == 200