import requests
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_price():
    url = "http://localhost:8000/prices/latest?symbol=AAPL&provider=yfinance"
    response = client.get(url)

    assert response.status_code == 200

    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    assert isinstance(data, dict)
    assert "symbol" in data
    assert "price" in data
    assert "timestamp" in data
    assert "provider"in data

def test_poll_prices():
    url = "http://localhost:8000/prices/poll"
    body = {"symbols": ["AAPL", "MSFT"], "interval": 60, "provider": "alpha_vantage"}
    response = client.post(url, json=body)

    assert response.status_code == 202

    assert response.headers["Content-type"] == "application/json"

    data = response.json()
    assert isinstance(data, dict)
    assert "job_id" in data
    assert data["status"] == "accepted"
    assert "config" in data