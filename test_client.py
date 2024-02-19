import requests
import dentalinktoken

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

def test_successfully_change_appointment_state():
    dummy_data = {
        "id_dentista"       : 2,
        "id_sucursal"       : 1,
        "id_estado"         : 7,
        "id_sillon"         : 1,
        "id_paciente"       : 2,
        "id_tratamiento"    : 2,
        "fecha"             : "2024-02-22",
        "hora_inicio"       : "10:00",
        "duracion"          : 30,
        "comentario"        : "Control exodoncia"
    }
    response = requests.post(
        f'https://api.dentalink.healthatom.com/api/v1/citas',
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN},
        data=dummy_data
    )
    appointment_id = response.json()["data"]["id"]
    print("dummy id:", appointment_id)

    # Parten en id_estado = 7

    response = client.put(f"/appointments/{appointment_id}", params={"new_state": 26})
    assert response.status_code == 200
    assert response.json()["data"]["id_estado"] == 26

def test_unsuccessfully_change_appointment_state():
    response = client.put(f"/appointments/336", params={"new_state": 1000})
    assert response.status_code == 400

    response =  client.put(f"/appointments/10000", params={"new_state": 1000})
    assert response.status_code == 400
