import requests
import json
from modules.Connect import helper
from datetime import datetime

with open('config.json') as f:
    config = json.load(f)

urlSIGECO = 'http://api.dakotaparts.com.br/OAuth/Token?username={0}&password={1}'.format(config['user'], config['pass'])

headers = {'Content-Type': 'application/json', 'Accept':'*/*'}
r = requests.get(urlSIGECO, headers=headers)
j = json.loads(r.text)

helper.cadastraToken(j['access_token'])

urlSalesforce = 'https://cs51.salesforce.com/services/oauth2/token'

body = {'grant_type': 'password',
        'client_id': config['SLF_clientId'],
        'client_secret': config['SLF_clientSecret'], 
        'username': config['SLF_user'], 
        'password': config['SLF_pass']}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
r = requests.post(urlSalesforce, headers=headers, data=body)
j = json.loads(r.text)
helper.cadastraTokenSalesforce(j['access_token'])

