from app.mac import mac, signals
from modules.Connect import helper
from modules.Connect import callouts
import json

'''
Signals this module listents to:
1. When a message is received (signals.command_received)
==========================================================
'''
@signals.message_received.connect
def handle(message):
    if message.text.lower() == 'menu':
        helper.cadastraEstado(message.who, 0)
    
    estado = helper.procurarEstado(message.who)
    print("Mensagem: {0}".format(message))
    
    if estado == 0:
        resposta = retornaResposta('menu')
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, 1)
    
    elif estado == 1:
        # Opção 1 - Informação do pedido
        if message.text.lower() == '1':
                resposta = retornaResposta('pedido')
                mac.send_message(resposta, message.conversation)
                helper.cadastraEstado(message.who, 2)
        
        # Opção 2 - Informação do pedido (https://busca.connectparts.com.br/busca?q=corsa+2015)
        elif message.text.lower() == '2':
                resposta = retornaResposta('produto1')
                mac.send_message(resposta, message.conversation)
                helper.cadastraEstado(message.who, 3)

        # Opção 3 - Vale-crédito
        elif message.text.lower() == '3':
                resposta = retornaResposta('vale')
                mac.send_message(resposta, message.conversation)
                helper.cadastraEstado(message.who, 0)

        # Opção 4 - Atendimento no chat
        elif message.text.lower() == '4':
                resposta = retornaResposta('chat')
                mac.send_message(resposta, message.conversation)
                helper.cadastraEstado(message.who, 0)
        
        # Opção 5 - Telefone
        elif message.text.lower() == '5':
                resposta = retornaResposta('telefone')
                mac.send_message(resposta, message.conversation)
                helper.cadastraEstado(message.who, 0)
    
    elif estado == 2:
        print('### DEBUG ### Procurou pedido')
        resp = callouts.buscarPedido(message.text)
        print('### DEBUG ### Resposta {0}'.format(resp))
        if resp.status_code == 200:
            dadosPedido = json.loads(resp.text)            
            resposta = "*Pedido*: {0} \n*Status*: {1} \n*Rastrear*: http://r.connectparts.com.br/?c={2}".format(dadosPedido['CodigoExterno'],dadosPedido['Status']['Descricao'],dadosPedido['Transportadora']['ServicoEntrega']['NumerosRastreio'][0])
            helper.cadastraEstado(message.who, 0)
        else:
            resposta = "Pedido não localizado."
        mac.send_message(resposta, message.conversation)
        
    elif estado == 3:
        resposta = retornaResposta('produto2')
        resposta += message.text.replace(" ","+")
        print('### DEBUG ### Resposta {0}'.format(resposta))
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, 0)

    else:
        resposta = "Desculpe, mas não entendi a mensagem. "
        mac.send_message(resposta, message.conversation)



    

def help(message):
    answer = "*Bot called mac* \nWhatsapp framework made in Python \n*Version:* 1.0.0 \n*Status:* Beta \nhttps://github.com/danielcardeenas/whatsapp-framework"
    mac.send_message(answer, message.conversation)

def retornaResposta(opcao):
    
    if opcao == 'menu':
        resposta = "Heey! É um prazer falar com você. Veja as opções que tenho pra você:\n\n"
        resposta += "1. Falar sobre um pedido. 📦\n"
        resposta += "2. Procurar um produto no site. 🚗\n"
        resposta += "3. Ver informação sobre como utilizar um vale-crédito. 🎫\n"
        resposta += "4. Falar com um atendente através do chat online. 💬\n"
        resposta += "5. Ver nosso telefone de contato. 📞\n"
        resposta += "\n\nDigite o número da opção desejada. 😉\n"
        resposta += "*DICA*: digite *MENU* a qualquer momento para rever essas opções."
    
    elif opcao == 'pedido':
        resposta = "Por favor, digite um número de pedido válido (ex: 17518648 ou 00K12345678)"

    elif opcao == 'produto1':
        resposta = "Qual é o *ano* e *modelo* do seu carro/moto ?"

    elif opcao == 'vale':
        resposta = "Informações de vale-crédito."

    elif opcao == 'chat':
        resposta = "Clique no link para você entrar no chat! https://goo.gl/MQPJQr "

    elif opcao == 'telefone':
        resposta = "📞 (14) 3311-8100 📞\n\n"
        resposta += "*Horário de atendimento:* \n"
        resposta += "Seg á sex: 9hs às 18h\n"
        resposta += "Sáb: 8hs às 14:15h\n"

    elif opcao == 'produto2':
        resposta = "Legal! Acesse o link para ver os produtos! https://busca.connectparts.com.br/busca?q="

    return resposta