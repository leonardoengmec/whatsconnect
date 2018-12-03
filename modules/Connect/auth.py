import requests
import json
import helper
from datetime import datetime

with open('config.json') as f:
    config = json.load(f)

url = 'http://api.dakotaparts.com.br/OAuth/Token?username={0}&password={1}'.format(config['user'], config['pass'])
print (url)
headers = {'Content-Type': 'application/json', 'Accept':'*/*'}
r = requests.get(url, headers=headers)
j = json.loads(r.text)

helper.cadastraToken(j['access_token'])
