"""Security and performance checks. IDs match docs/test_cases.md."""
import time
import pytest
from app import main


# TC17 - same error for wrong password and unknown user
@pytest.mark.security
def test_tc17_login_errors_do_not_leak_user_existence(register, login):
    register()
    wrong_pw = login(password="WrongPass999")
    unknown = login(username="ghost_user")
    assert wrong_pw.status_code == unknown.status_code == 401
    assert wrong_pw.json() == unknown.json()


# R1 - password is not stored in plain text
@pytest.mark.security
def test_r1_password_is_hashed(register):
    register(password="Passw0rd123")
    stored = main.users["alice_1"]
    assert "Passw0rd123" not in str(stored)
    assert len(stored["hash"]) == 64  # sha256 hex


# Same password, different users -> different hashes (salting works)
@pytest.mark.security
def test_salt_gives_different_hashes(register):
    register("user_a", "Passw0rd123")
    register("user_b", "Passw0rd123")
    assert main.users["user_a"]["hash"] != main.users["user_b"]["hash"]


# TC18 - performance
@pytest.mark.performance
def test_tc18_health_responds_under_500ms(client):
    start = time.perf_counter()
    r = client.get("/health")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert r.status_code == 200
    assert elapsed_ms < 500
