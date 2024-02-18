import re
import requests
import dentalinktoken

def check_dates(dates: list):
    pattern = re.compile("(^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$)?")
    for date in dates:
        if not pattern.match(date):
            return False
    return True

def check_state(state: int):
    possible_states = [-1, 0, 1]
    if state in possible_states:
        return True
    else:
        return False

cached_branches = [-1]

branches_response = requests.get(
    'https://api.dentalink.healthatom.com/api/v1/sucursales?q={"habilitada":{"eq":"1"}}',
    headers={"Authorization": "Token " + dentalinktoken.DENTALINK_TOKEN}
).json()["data"]

for branch in branches_response:
    if branch["id"] not in cached_branches:
        cached_branches.append(branch["id"])

def check_branch(branch: int):
    if branch not in cached_branches:
        return False
    else:
        return True

def check_parameters(dates: list, state: int, branch: int):
    return check_dates(dates) and check_state(state) and check_branch(branch)

