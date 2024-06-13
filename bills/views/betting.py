import requests

def get(url):
    try:
        # Make the API request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

        else:
            print('Error:', response.status_code)

    except requests.exceptions.RequestException as e:
        print('Error:', e)

def post(url, body:dict, headers):
    try:
        # Make the API request
        response = requests.post(url, data=body, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

        else:
            print('Error:', response.status_code)

    except requests.exceptions.RequestException as e:
        print('Error:', e)