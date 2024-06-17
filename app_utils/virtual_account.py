import requests
import app_utils.secret_keys as keys
from app_utils.custom_types import CustomResponse


def createAccount(email:str, first_name:str, last_name:str, phone:str, bank:str)->CustomResponse:
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
        data = data|{"msg": message}
    except:
        data = {"msg": "Server Error"}
    
    if code == 200:
        has_error = (not data['status'])
        
    return CustomResponse(code, data, has_error)


# createAccount("janedoe@test.com","Jane", "karen", "+2348100000000", "test-bank")

# {'status': True, 'message': 'Assign dedicated account in progress'}