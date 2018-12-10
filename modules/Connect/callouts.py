import requests
import json
from modules.Connect import helper

def buscarPedido(numeroPedido):

    token = helper.recuperaToken()

    url = 'http://api.dakotaparts.com.br/fenix/Pedido/Buscar?codigoExterno={0}'.format(numeroPedido)
    headers = {'Authorization': 'bearer {0}'.format(token)}
    r = requests.get(url, headers=headers)
    print(r.json)
    return r

def enviaMensagemSalesforce(idwhats, mensagem):

    token = helper.recuperaTokenSalesforce()
    
    urlSalesforce = 'https://cs51.salesforce.com/services/apexrest/whatsapp/'
    headers = {'Authorization': 'OAuth {0}'.format(token), 'Content-Type': 'application/json'}
    
    data = {"idWhats": idwhats,
            "mensagem": mensagem}
    print(data)
    data = json.dumps(data)
    r = requests.post(urlSalesforce, headers=headers, data=data)
    print(r.text)
    
def retornaMensagemSalesforce():

    token = helper.recuperaTokenSalesforce()
    urlSalesforce = 'https://cs51.salesforce.com/services/apexrest/whatsapp/'
    headers = {'Authorization': 'OAuth {0}'.format(token), 'Content-Type': 'application/json'}
    
    r = requests.get(urlSalesforce, headers=headers)
    print(r.text)
    j = json.loads(r.text)
    return j
    
