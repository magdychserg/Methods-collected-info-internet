from pprint import pprint
import json

import requests

user = 'magdychserg'
url = 'https://api.github.com/users/'
response = requests.get(url + user + '/repos')
response_json = response.json()
with open('task1.json', 'w') as file:
    json.dump(response_json, file)

print('Список репозиториев:')
for repo in response_json:
    pprint(repo['name'])
