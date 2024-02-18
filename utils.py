import re
import requests
import dentalinktoken

def check_dates(dates: list):
    pattern = re.compile("(^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$)?")
    for date in dates:
        if not pattern.fullmatch(date):
            return False
    return True

def get_states():
    states = [-1]

    appointments_response = requests.get(
        'https://api.dentalink.healthatom.com/api/v1/citas',
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN}
    ).json()["data"]

    for appointment in appointments_response:
        if appointment["id_estado"] not in states:
            states.append(appointment["id_estado"])

    return states

def check_state(state: int, possible_states: list):
    if state in possible_states:
        return True
    else:
        return False

def get_branches():
    branches = [-1]

    branches_response = requests.get(
        'https://api.dentalink.healthatom.com/api/v1/sucursales?q={"habilitada":{"eq":"1"}}',
        headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN}
    ).json()["data"]

    for branch in branches_response:
        if branch["id"] not in branches:
            branches.append(branch["id"])

    return branches

def check_branch(branch: int, possible_branches):
    if branch not in possible_branches:
        return False
    else:
        return True

def check_parameters(dates: list, state: int, possible_states: list, branch: int, possible_branches: list):
    return check_dates(dates) and check_state(state, possible_states) and check_branch(branch, possible_branches)

