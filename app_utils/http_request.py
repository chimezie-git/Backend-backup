import requests


def test_request():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.request("GET", url)
    data = response.json()
    code = response.status_code
    print(f"code {code}")
    print(f"data {data}")

test_request()