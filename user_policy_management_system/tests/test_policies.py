def make_user():
    return {
        "uname": "Policy User",
        "uemail": "policy@example.com",
        "uage": 30,
        "uphone": "9876543210",
        "uaddress": "Indore",
    }


def make_policy(uid):
    return {
        "uid": uid,
        "pname": "Life Secure",
        "ptype": "Life",
        "ppremium": 12000,
        "psumassured": 1000000,
    }


def test_policy_crud(client):
    user_response = client.post("/users/", json=make_user())
    uid = user_response.json()["uid"]

    response = client.post(
        "/policies/",
        json=make_policy(uid),
    )
    assert response.status_code == 201

    pid = response.json()["pid"]

    assert client.get("/policies/").status_code == 200
    assert client.get(f"/policies/{pid}").status_code == 200

    response = client.put(
        f"/policies/{pid}",
        json={"ppremium": 15000},
    )
    assert response.status_code == 200
    assert response.json()["ppremium"] == 15000

    assert client.delete(f"/policies/{pid}").status_code == 204
    assert client.get(f"/policies/{pid}").status_code == 404


def test_policy_validation(client):
    user_response = client.post("/users/", json=make_user())
    uid = user_response.json()["uid"]

    payload = make_policy(uid)
    payload["ppremium"] = -100

    response = client.post("/policies/", json=payload)

    assert response.status_code == 422
