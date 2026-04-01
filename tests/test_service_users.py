import os
import pytest
import requests
from urllib.parse import urlencode

BASE = "http://127.0.0.1:8000"
USERS_ENDPOINT = f"{BASE}/users"

def get_users_with_params(username, password):
    params = {"username": username, "password": password}
    url = f"{USERS_ENDPOINT}?{urlencode(params)}"
    return requests.get(url, timeout=5)

def test_users_bad_credentials():
    resp = get_users_with_params("notadmin", "wrongpass")
    assert resp.status_code == 401

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

@pytest.mark.skipif(not ADMIN_PASSWORD, reason="ADMIN_PASSWORD not set")
def test_users_admin_login():
    resp = get_users_with_params("admin", ADMIN_PASSWORD)
    assert resp.status_code == 200