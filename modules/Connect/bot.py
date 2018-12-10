# -*- coding: utf-8 -*-

from app.mac import mac, signals
from modules.Connect import helper
from modules.Connect import callouts
import json
import urllib
import random

@signals.message_received.connect
def handle(message):
    
    menuInicial = 0
    menuNivel1 = 99
    menuPedido = 1
    menuPromocoes = 2
    menuProduto = 3
    menuChat = 4
    menuChatPre = 5
    menuChatPos = 6

    if message.text.lower() == 'menu':
        helper.cadastraEstado(message.who, menuInicial)
    
    estado = helper.procurarEstado(message.who)
    print("Mensagem: {0}".format(message))
    
    if estado == menuInicial:
        helper.syncContato(message.who, message.who_name)
        var = [message.who_name]
        resposta = retornaResposta('menu', var)
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, menuNivel1)
    
    # Opcoeses do menu
    elif estado == menuNivel1:
        # Opcao 1 - Informacao do pedido
        if message.text.lower() == '1':
            resposta = retornaResposta('pedido.menu',[])
            helper.cadastraEstado(message.who, menuPedido)
        
        # Opcao 2 - Produto no site (https://busca.connectparts.com.br/busca?q=)
        elif message.text.lower() == '2':
            resposta = retornaResposta('produto.menu',[])
            helper.cadastraEstado(message.who, menuProduto)

        # Opcao 3 - Vale-credito
        elif message.text.lower() == '3':
            resposta = retornaResposta('promocoes',[])
            helper.cadastraEstado(message.who, menuNivel1)

        # Opcao 3 - Vale-credito
        elif message.text.lower() == '4':
            resposta = retornaResposta('vale.menu',[])
            helper.cadastraEstado(message.who, menuNivel1)

        # Opcao 4 - Atendimento no chat
        elif message.text.lower() == '5':
            resposta = retornaResposta('chat.menu',[])
            helper.cadastraEstado(message.who, menuChat)
        
        # Opcao 5 - Telefone
        elif message.text.lower() == '6':
            resposta = retornaResposta('telefone.menu',[])
            helper.cadastraEstado(message.who, menuNivel1)

        else:
            resposta = retornaResposta('nenhumaOpcao', [])
        
        mac.send_message(resposta, message.conversation)
    
    # Informacoes de pedido
    elif estado == menuPedido:
        
        resp = callouts.buscarPedido(message.text)
        
        if resp.status_code == 200:
            dadosPedido = json.loads(resp.text)          
            var = [dadosPedido['CodigoExterno'],validaStatus(dadosPedido['Status']['Descricao']),dadosPedido['Transportadora']['ServicoEntrega']['NumerosRastreio'][0]]  
            resposta = retornaResposta('pedido.dados',var)
            helper.cadastraEstado(message.who, menuNivel1)
        else:
            resposta = retornaResposta('pedido.naoLocalizado',[])
        
        mac.send_message(resposta, message.conversation)
        
    # Promocoes do site
    elif estado == menuPromocoes:
        resposta = retornaResposta('promocoes',[])
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, menuNivel1)

    # Buscar produto no site
    elif estado == menuProduto:
        resposta = retornaResposta('produto.link',[])
        resposta += message.text.replace(" ","+")
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, menuNivel1)
        helper.cadastraVeiculo(message.who, message.text)

    # Entrar no chat
    elif estado == menuChat:
        if message.text.lower() == '1':
                resposta = retornaResposta('chat.pre',[])
                helper.cadastraEstado(message.who, menuChatPre)
    
        elif message.text.lower() == '2':
                resposta = retornaResposta('chat.pos',[])
                helper.cadastraEstado(message.who, menuChatPos)

        mac.send_message(resposta, message.conversation)

    #Link do chat
    elif estado == menuChatPre:
        #nome={0}&email={1}&canal={2}&pedido={3}&codigoBtn={4}'
        var = [message.text,'','Chat%20Online%20%22Realizar%20uma%20compra%22','',1]
        resposta = retornaResposta('chat.link', var)
        helper.cadastraEstado(message.who, menuNivel1)
        mac.send_message(resposta, message.conversation)

    elif estado == menuChatPos:
        #nome={0}&email={1}&canal={2}&pedido={3}&codigoBtn={4}'
        var = ['','','Chat%20Online%20%22Falar%20sobre%20seu%20pedido%22',message.text,1]
        resposta = retornaResposta('chat.link', var)
        helper.cadastraEstado(message.who, menuNivel1)
        mac.send_message(resposta, message.conversation)

    else:
        resposta = "Desculpe, mas nao entendi a mensagem. "
        mac.send_message(resposta, message.conversation)
    

def retornaResposta(opcao, variaveis):
    
    if opcao == 'menu':
        lista = ["Olá {0}! Que legal falar com você. ".format(*variaveis), "Hey {0}, você por aqui? ".format(*variaveis)]
        resposta = random.choice(lista)
        resposta += "Posso te ajudar com as seguintes opcões:\n\n"
        resposta += "1. Informacões sobre um pedido. 📦\n"
        resposta += "2. Procurar um produto no site. 🚗\n"
        resposta += "3. Ver as promocões de hoje. 🎁\n"
        resposta += "4. Informacao sobre como utilizar um vale-crédito ou cupom de desconto. 🎫\n"
        resposta += "5. Falar com um atendente através do chat online. 💬\n"
        resposta += "6. Ver nosso telefone de contato. 📞\n\n"
        resposta += "Digite o número da opcao desejada. 😉\n\n"
        resposta += "*DICA*: digite *MENU* a qualquer momento para rever essas opcões."
    
    elif opcao == 'pedido.menu':
        resposta = "Por favor, digite o número do seu pedido."

    elif opcao == 'pedido.dados': 
        resposta = "*Pedido*: {0} \n"
        resposta += "*Status*: {1} \n"
        resposta += "*Rastreamento*: http://r.connectparts.com.br/?c={2}"
        resposta = resposta.format(*variaveis)
    
    elif opcao == 'pedido.naoLocalizado':
        resposta = "Nao localizei nenhum pedido com esse número. Pode digitar novamente?"

    elif opcao == 'promocoes':
        resposta = "Confira nossas promocões neste link: https://www.connectparts.com.br/cupons-de-desconto"

    elif opcao == 'produto.menu':
        resposta = "Qual é o *ano* e *modelo* do seu carro/moto ?"

    elif opcao == 'produto.link':
        resposta = "Legal! Acesse o link para ver os produtos! https://busca.connectparts.com.br/busca?q="

    elif opcao == 'vale.menu':
        resposta = "Acesse o nosso site, faca o seu login, selecione o produto desejado, adicione-o ao carrinho e clique em finalizar compra.\n\n"
        resposta += "Selecione o botao fechar pedido e na etapa de pagamento selecione a opcao adicionar vale-crédito.\n\n"
        resposta += "Insira o código do vale no campo disponível e clique no botao adicionar. Se o valor do vale for igual ao do pedido, finalize o pedido."
        resposta += "Caso contrário, selecione uma opcao de pagamento para complementar o valor antes de finalizá-lo."

    elif opcao == 'chat.menu':
        resposta = "Ok! Para direcionar você para o atendente certo, digite o número do motivo sobre qual deseja falar:\n\n"
        resposta += "1. Realizar uma compra\n"
        resposta += "2. Falar sobre um pedido"

    elif opcao == 'chat.pre':
        resposta = "Por favor, me fale o seu *nome*."
       
    elif opcao == 'chat.pos':
        resposta = "Ok, me informe o *número* do seu pedido."
        
    elif opcao == 'chat.link':
        url = 'https://connectparts.secure.force.com/AssistenteVirtual/ConectaChatLiveAgent?'
        url += 'nome={0}&email={1}&canal={2}&pedido={3}&codigoBtn={4}'.format(*variaveis)

        resposta = "Clique no link para você entrar no chat!\n"
        #resposta += "(Falta o link)"
        resposta += url

    elif opcao == 'telefone.menu':
        resposta = "📞 (14) 3311-8100 📞\n\n"
        resposta += "*Horário de atendimento SAC:* \n"
        resposta += "*Segunda à sexta-feira:* 9hs às 18h\n"
        resposta += "*Sábado:* 8hs às 14:15h\n"

    elif opcao == 'nenhumaOpcao':
        resposta = "Ahhh que pena, mas nao tenho essa opcao! 😥\nSe quiser ver as opcões novamente, digite *menu*."
    
    return resposta

def validaStatus(status):
    if status == 'AGUARDANDO ESTOQUE' or status == 'ESTOQUE RESERVADO PARCIALMENTE':
        return 'AGUARDANDO SEPARACAO DE MERCADORIAS'
    else:
        return status