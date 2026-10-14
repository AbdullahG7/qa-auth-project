"""Functional tests. Test case IDs match docs/test_cases.md."""
import pytest


# TC01 - valid registration
def test_tc01_register_valid_user(register):
    assert register().status_code == 201


# TC02-TC07 - boundary values
@pytest.mark.parametrize(
    "tc, username, password, expected",
    [
        ("TC02", "abc", "Passw0rd123", 201),            # username at min
        ("TC03", "ab", "Passw0rd123", 422),             # username below min
        ("TC04", "a" * 20, "Passw0rd123", 201),         # username at max
        ("TC05", "a" * 21, "Passw0rd123", 422),         # username above max
        ("TC06", "alice_1", "1234567", 422),            # password below min
        ("TC07", "alice_1", "12345678", 201),           # password at min
    ],
)
def test_boundaries(register, tc, username, password, expected):
    assert register(username, password).status_code == expected, tc


# TC08 - invalid characters
def test_tc08_bad_characters_in_username(register):
    assert register("bob!@#", "Passw0rd123").status_code == 422


# TC09 - duplicate username
def test_tc09_duplicate_username(register):
    assert register().status_code == 201
    assert register().status_code == 409


# TC10 - correct login returns a token
def test_tc10_login_success(register, login):
    register()
    r = login()
    assert r.status_code == 200
    assert "access_token" in r.json()


# TC11 - wrong password
def test_tc11_wrong_password(register, login):
    register()
    assert login(password="WrongPass999").status_code == 401


# TC12 - unknown user
def test_tc12_unknown_user(login):
    assert login(username="ghost_user").status_code == 401


# TC13 - lockout after 5 failures
def test_tc13_account_locks_after_five_failures(register, login):
    register()
    for _ in range(5):
        assert login(password="WrongPass999").status_code == 401
    assert login().status_code == 423  # correct password, still locked


# TC14 - counter resets after a successful login
def test_tc14_failed_counter_resets_on_success(register, login):
    register()
    for _ in range(3):
        login(password="WrongPass999")
    assert login().status_code == 200
    assert login(password="WrongPass999").status_code == 401  # not locked


# TC15 - no token
def test_tc15_me_without_token(client):
    assert client.get("/me").status_code == 401


# TC16 - fake token
def test_tc16_me_with_fake_token(client):
    r = client.get("/me", headers={"Authorization": "Bearer abc"})
    assert r.status_code == 401


# Extra - a real token works on /me
def test_me_with_valid_token(client, register, login):
    register()
    token = login().json()["access_token"]
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == {"username": "alice_1"}
