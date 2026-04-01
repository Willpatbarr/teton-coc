import requests

BASE = "http://127.0.0.1:8000"
DATA_ENDPOINT = f"{BASE}/data/all"

def test_data_all_returns_businesses():
    resp = requests.get(DATA_ENDPOINT, timeout=5)
    assert resp.status_code == 200

    data = resp.json()
    assert "businesses" in data
    assert isinstance(data["businesses"], list)
    assert len(data["businesses"]) > 0