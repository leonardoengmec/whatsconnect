import pymongo
import os
from datetime import datetime

cliente = pymongo.MongoClient('mongodb://localhost:27017/')
banco = cliente['contatosRealizados']
tabela = banco['estados']
acesso = banco['acesso']
salesforce = banco['salesforce']

def cadastraEstado(telefone, estado):
    procurar = { "phone": telefone }
    novoValor = { "estado": estado }

    x = tabela.update_one(procurar, {'$set': novoValor}, upsert=True)
    print('Registro inserido {0}'.format(x.matched_count))

def procurarEstado(numero):
    queryStr = {}
    queryStr['phone'] = numero
    result = tabela.find_one(queryStr)
    print('### DEBUG ### {0}'.format(result))
    if result == None:
        return 0
    else:
        return result['estado']

def contar(numero):
    queryStr = {}
    queryStr['phone'] = numero
    result = tabela.count_documents(queryStr)
    print('Telefones encontrados: {0}'.format(result))
    return result

def cadastraToken(token):
    dadosToken = {}
    dadosToken["token"] = token
    acesso.drop()
    acesso.insert_one(dadosToken)
    
    for i in acesso.find():
        print(i)

def cadastraTokenSalesforce(token):
    dadosToken = {}
    dadosToken["token"] = token
    salesforce.drop()
    salesforce.insert_one(dadosToken)
    
    for i in salesforce.find():
        print(i)

def recuperaToken():
    return acesso.find_one()['token']  

def recuperaTokenSalesforce():
    return salesforce.find_one()['token']  

def arrumaData(data):
    #Thu, 29 Nov 2018 20:11:05 GMT
    dia = int(data[5:7])
    mes = data[8:11]
    ano = int(data[12:16])
    hora = int(data[17:19])
    minuto = int(data[20:22])

    def retornaMes(mes):
        dicMes = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        for k, v in dicMes.iteritems():
            if mes == k:
                return int(v)

    data = datetime(ano, retornaMes(mes), dia, hora, minuto)

    return data
    
def cadastraVeiculo(telefone, veiculo):
    procurar = { "phone": telefone }
    novoValor = { "veiculo": veiculo }

    x = tabela.update_one(procurar, {'$set': novoValor}, upsert=True)
    print('Veiculo inserido {0}'.format(x.matched_count))

def syncContato(telefone, nome):
    procurar = { "phone": telefone}
    x = tabela.find(procurar)
    telefone_certo = telefone.split('@')[0]

    if x.count() == 0:
        with open(os.path.abspath("./config.py"),"r+") as f:
            old = f.read()
            f.seek(len(old)-1)
            f.write('    "' + telefone_certo + '": "' + nome + '", \n}')
        cadastraEstado(telefone,99)

