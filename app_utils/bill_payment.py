import requests
import app_utils.secret_keys as keys
from app_utils.custom_types import CustomResponse

def buyAirtime(provider:str, number:str, amount:str, reference:str)->CustomResponse:
    url = f"{keys.giftbills_base_url}/airtime/topup"
    payload = {
    "provider": provider,
    "number": number,
    "amount": amount,
    "reference": "GBR_2459392959593939"
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
        if (not has_error) and ("error" in data):
            error:dict = data['error']
            message = f"{data['message']}:\n{list(error.values())[0][0]}"
    return CustomResponse(code, data, has_error, message)

def buyData(provider:str, number:str, plan_id:str, reference:str)->CustomResponse:
    url = f"{keys.giftbills_base_url}/internet/data"
    payload = {
    "provider": provider,
    "number": number,
    "plan_id": plan_id,
    "reference": "GB_2459392959593939"
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
    return CustomResponse(code, data, has_error, message)

def payBetting(provider:str, customer_id:str, amount:str, reference:str)->CustomResponse:
    url = f"{keys.giftbills_base_url}/betting/topup"
    payload = {
    "provider": provider,
    "amount": amount,
    "customerId": customer_id,
    "reference": "GB_2459392959593939"
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
    return CustomResponse(code, data, has_error, message)

def payElectricity(provider:str, number:str, amount:str, reference:str)->CustomResponse:
    url = f"{keys.giftbills_base_url}/electricity/recharge"
    payload = {
        "provider": provider,
        "number": number,
        "amount": amount,
        "type": "prepaid",
        "reference": "34392002",
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
    return CustomResponse(code, data, has_error, message)

def payCable(provider:str, number:str, plan_id:str, reference:str)->CustomResponse:
    url = f"{keys.giftbills_base_url}/tv/pay"
    payload = {
        "provider": provider,
        "number": number,
        "plan_id": plan_id,
        "reference": "RE2324324"           
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
    return CustomResponse(code, data, has_error, message)

def sendBulkSMS(sender_name:str, message:str, numbers:list[str])->CustomResponse:
    url = f"{keys.giftbills_base_url}/send-sms"
    payload = {
        "sender_id": sender_name,
        "route": "1",
        "message": message,
        "type_recipient": "".join(numbers)
    }
    headers = {
        "Authorization": f"Bearer {keys.giftbills_api_key}",
        "MerchantId": "nitrobills", 
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    code = response.status_code
    data = response.json()
    has_error = True
    message = ""
    if code == 200:
        has_error = data['success']
        message = data['message']
    return CustomResponse(code, data, has_error, message)


buyAirtime("GLO", "234909", "f00", "")

# buyData("MTN", "2349060309095", "2", "")

# payBetting("BET9JA", "1028707","200", "")

# payElectricity("IBEDC", "11111111111", "1500", "")

# payCable("GOTV", "111111111111111", "24", "")

# sendBulkSMS("SomeUser", "how do you do", ["0902202826, 0803334237"])