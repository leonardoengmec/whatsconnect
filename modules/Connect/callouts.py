import requests
import json
import helper

def buscarPedido(numeroPedido):

    token = helper.recuperaToken()

    url = 'http://api.dakotaparts.com.br/fenix/Pedido/Buscar?codigoExterno={0}'.format(numeroPedido)
    headers = {'Authorization': 'bearer {0}'.format(token)}
    r = requests.get(url, headers=headers)
    print(r.json)
    return r
    
    
    #return json.loads(r.json)

    #
    #http://api.dakotaparts.com.br/fenix/Pedido/Buscar?codigoExterno=00K45286189&ignorarCancelados=false
