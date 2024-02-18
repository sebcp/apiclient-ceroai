import dentalinktoken
import requests

from fastapi import FastAPI
from utils import *

app = FastAPI()

@app.get("/appointments")
def root(lower_date: str = "", upper_date: str = "", state: int = -1, branch: int = -1):
    if not check_parameters([lower_date, upper_date], state, branch):
        return {"message": "Parámetros no cumplen con el formato o no existen"}
    else:
        query = '?q='
        filters = []
        if lower_date + upper_date != "":
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
