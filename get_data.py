import requests
import json

def get(url):
    response = requests.get(url)
    return json.loads(response.content)
