import requests
import app_utils.secret_keys as keys
from app_utils.custom_types import CustomResponse


def createAccount(email: str, first_name: str, last_name: str, phone: str, bank: str) -> CustomResponse:
    url = "https://api.paystack.co/dedicated_account/assign"
    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "preferred_bank": bank,
        "country": "NG"
    }
    headers = {
        "Authorization": f"Bearer {keys.paystack_secret_key}",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    has_error = True
    data = dict()
    try:
        data = response.json()
        message = data.pop("message")
        data = data | {"msg": message}
    except:
        data = {"msg": "Server Error"}

    if code == 200:
        has_error = (not data['status'])

    return CustomResponse(code, data, has_error)


def getBankInfo() -> list:
    url = "https://api.paystack.co/dedicated_account/available_providers"
    headers = {
        "Authorization": f"Bearer {keys.paystack_secret_key}",
        'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers)
    try:
        res_data = response.json()
        data = res_data["data"]
        bank1 = data[0]["provider_slug"]
        bank2 = data[1]["provider_slug"]
        return [bank1, bank2]
    except:
        return "wema-bank"
