import requests
import json
import helper
from datetime import datetime

url = 'http://api.connectparts.com.br:8032/OAuth/Token?username={0}&password={1}'.format('leonardo.santos@connectparts.com.br','Connect@2018')
headers = {'Content-Type': 'application/json', 'Accept':'*/*'}
r = requests.get(url, headers=headers)
j = json.loads(r.text)

helper.cadastraToken(j['access_token'])

authLog = open('logAuth.txt', 'a')
authLog.write('\nAutenticado em ' + str(datetime.now()))



