import json

import pytest


def test_add_user(test_app, test_redis):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "tester@test.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "tester@test.io was added!" in data["message"]

    resp = client.post(
        "/users",
        data=json.dumps({"email": "tester@test.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_delete_user(test_app, test_redis, add_user):
    email = "tester@delete.io"
    client = test_app.test_client()
    resp = client.delete(f"/users/{email}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert f"User {email} does not exist" in data["message"]

    add_user(email)

    resp = client.delete(f"/users/{email}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200

    resp = client.get(f"/users/{email}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert f"User {email} does not exist" in data["message"]


def test_get_user(test_app, test_redis, add_user):
    email_fake = "thisdoesntexist@imaginary.io"
    email_real = "thisemailexists@real.io"
    client = test_app.test_client()

    add_user(email_real)

    resp = client.get(f"/users/{email_real}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert email_real in data["email"]

    resp = client.get(f"/users/{email_fake}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert f"User {email_fake} does not exist" in data["message"]
