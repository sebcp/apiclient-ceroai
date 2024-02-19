import dentalinktoken
import requests

from fastapi import FastAPI, HTTPException
from utils import *

app = FastAPI()

possible_states = get_states()
possible_branches = get_branches()

@app.get("/appointments")
def root(lower_date: str = "", upper_date: str = "", state: int = -1, branch: int = -1):
    if not check_parameters([lower_date, upper_date], state, possible_states, branch, possible_branches):
        raise HTTPException(status_code=400, detail="Los parámetros entregados no cumplen con el formato o no existen.")
    else:
        query = '?q='
        filters = []
        if len(lower_date + upper_date)==20:
            filters.append('"fecha":[{"gte":"'+lower_date+'"},{"lte":"'+upper_date+'"}]')
        if state != -1:
            filters.append('"estado_cita": {"eq":"'+str(state)+'"}')
        query = query + '{' + ','.join(filters) + '}'
        if branch != -1:
            uri = f"https://api.dentalink.healthatom.com/api/v1/sucursales/{branch}/citas"
        else:
            uri = "https://api.dentalink.healthatom.com/api/v1/citas"
        response = requests.get(
            uri+query,
            headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN}
        )

        return response.json()

@app.put("/appointments/{appointment_id}")
def root(appointment_id: int, new_state: int):
    if new_state not in possible_states:
        raise HTTPException(status_code=400, detail="El nuevo estado entregado no existe.")

    response = requests.put(
        f'https://api.dentalink.healthatom.com/api/v1/citas/{appointment_id}',
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN},
        data={"id_estado": new_state}
    )

    return response.json()