import requests

url = "http://20.244.56.144/evaluation-service/register"

data = {
    "email": "akumar1_me24@thapar.edu",
    "name": "Amardeep Kumar",
    "mobileNo": "8958031795",
    "githubUsername": "Amardeep6007",
    "rollNo": "8024320013",
    "collegeName": "Thapar Institute of engineering and technology, Patiala",
    "accessCode": "XryeHD"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Registered successfully!")
    print(response.json())
else:
    print("Failed to register.")
    print(response.status_code, response.text)
