import requests

req = requests.get('http://localhost:8084'+'/category={}'.format(1))
print(req.json())
