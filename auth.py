import requests

url = "http://20.244.56.144/evaluation-service/auth"

data = {
    "email": "akumar1_me24@thapar.edu",
    "name": "amardeep Kumar",
    "rollNo": "8024320013",
    "accessCode": "XryeHD",
    "clientID": "d3c0d142-49a8-4d72-a551-629778ff2943",
    "clientSecret": "cfPysBMAKAzvfMhQ"
}

try:
    response = requests.post(url, json=data, timeout=5)
    response.raise_for_status() 

    json_response = response.json()
    print("Token received successfully!")
    print("Access Token:", json_response.get("access_token"))
    print("Token Type:", json_response.get("token_type"))
    print("Expires In:", json_response.get("expires_in"))

except requests.exceptions.RequestException as e:
    print("An error occurred while making the request:", e)

except ValueError:
    print("Couldn't decode response as JSON. Raw response:")
    print(response.text)
