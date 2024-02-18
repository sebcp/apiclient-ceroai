from fastapi.testclient import TestClient

from client import app

client = TestClient(app)


def test_read_appointments():
    response = client.get("/appointments")
    assert response.status_code == 200
    assert response.json()["data"] != []

def test_read_appointments_error():
    response = client.get("/appointments", params={"lower_date": "18-02-2024", "upper_date": "20-02-2024"})
    assert response.status_code == 400

    response = client.get("/appointments", params={"state":10})
    assert response.status_code == 400

    response = client.get("/appointments", params={"branch":100})
    assert response.status_code == 400