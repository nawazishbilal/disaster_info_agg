import requests

response = requests.post("http://127.0.0.1:5000/predict", json={"text": "Flooding in the city!"})
print(response.json())