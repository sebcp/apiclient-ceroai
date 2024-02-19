import requests

import pytest
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import dentalinktoken
from utils import check_parameters, get_states, get_branches
'The module dentalinktoken is a local-only file with the Dentalink API token.'


app = FastAPI()
possible_states = get_states()
possible_branches = get_branches()

@app.get("/appointments")
def get_appointments(lower_date: str = "", upper_date: str = "", state: int = -1, branch: int = -1):
    '''
    This GET method retrieves existing appointments from the Dentalink API.
    The appointments can be filtered by date range, state and branch.

    It is assumed that you can filter by none, any or all of the parameters.
    It is assumed that the possible states an appointment can take can only be retrieved manually
    from the Dentalink API. The same is assumed for the branches.
    '''
    if not check_parameters([lower_date, upper_date], state, possible_states, branch, possible_branches):
        raise HTTPException(status_code=400, detail="Los parámetros entregados no cumplen con el formato o no existen.")
    '''
    A filter query is constructed by checking that there are parameters given to the request
    that aren't the default values.
    If the date range and the state aren't the default values, a filter string is created
    and appended to the list.
    The branch parameter is checked last because of the way the Dentalink API is defined.
    Since it's only possible to filter the appointments by date and state through their
    URI, it is necessary to use the URI provided by the branches to fetch the appointments
    if a branch is given.

    It is assumed that all SQL queries made through the Dentalink API are made using prepared
    statements and that it isn't the responsibility of this API client to protect the Dentalink API
    from SQL injections. It is also asummed that there will not be any XSS attacks.

    Pydantic is omitted because the rigorous validation of the library is too much for such a 
    simple application. It could be used if it wasn't an interface between the bot and the Dentalink API.
    '''
    filters = []
    if len(lower_date + upper_date)==20:
        filters.append('"fecha":[{"gte":"'+lower_date+'"},{"lte":"'+upper_date+'"}]')
    if state != -1:
        filters.append('"estado_cita": {"eq":"'+str(state)+'"}')
    query = '?q=' + '{' + ','.join(filters) + '}'
    if branch != -1:
        uri = f"https://api.dentalink.healthatom.com/api/v1/sucursales/{branch}/citas"
    else:
        uri = "https://api.dentalink.healthatom.com/api/v1/citas"
    response = requests.get(
        uri+query,
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN},
        timeout=10
    )

    return response.json()

@app.put("/appointments/{appointment_id}")
def change_appointment_state(appointment_id: int, new_state: int):
    '''
    This PUT request receives an appointment id and a new state.
    The request will make another request to the Dentalink API to change the appointment's
    state to the new one.
    '''
    if new_state not in possible_states:
        raise HTTPException(status_code=400, detail="El nuevo estado entregado no existe.")

    response = requests.put(
        f'https://api.dentalink.healthatom.com/api/v1/citas/{appointment_id}',
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN},
        data={"id_estado": new_state},
        timeout=10
    )

    return response.json()

if __name__ == "__main__":
    pytest.main(["-v", "test_client.py"])
    uvicorn.run("client:app", host="127.0.0.1", port=8000)
