import uuid


def new_user():
    return {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}


# A second user with a name that is already taken is refused with 400.
def test_duplicate_username_is_refused(api):
    user = new_user()
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused with 401.
def test_wrong_password_is_refused(api):
    user = new_user()
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users/token/login", json={**user, "password": "wrong"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# A user with an empty name is refused with 400.
def test_empty_username_is_refused(api):
    user = {"username": "", "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
