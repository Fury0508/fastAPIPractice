import requests
import json

API = "http://127.0.0.1:8000/get_course"
re = requests.get(API)
print(re.status_code)
print(re.json())