import requests
import json

remote_url = "https://api.chucknorris.io/jokes/"


def get_joke_from_remote(id):
    url = remote_url + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return False
    response_json = json.loads(response.text)
    return response_json


def query_joke_from_remote(query):
    args = {"query": query}
    url = remote_url + 'search'
    response = requests.get(url, args)
    if response.status_code != 200:
        return False
    response_json = json.loads(response.text)
    return response_json