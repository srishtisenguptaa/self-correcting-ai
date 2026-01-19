import requests
import json

url = "http://localhost:8000/process"
payload = {"text": "John is 30 years old from New York, works at Google, salary 150000"}
headers = {"Content-Type": "application/json"}

print("Testing API at", url)
try:
    response = requests.post(url, json=payload, timeout=120)
    print("Status:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", str(e))
