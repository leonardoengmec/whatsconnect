from app.mac import mac, signals
from modules.Connect import helper
from modules.Connect import callouts
import json

@signals.message_received.connect
def handle(message):

    menuInicial = 0
    menuNivel1 = 1
    menuPedido = 2
    menuProduto = 3
    menuChat = 4
    menuChatCanal = 5

    if message.text.lower() == 'menu':
        helper.cadastraEstado(message.who, menuInicial)
    
    estado = helper.procurarEstado(message.who)
    print("Mensagem: {0}".format(message))
    
    if estado == 0:
        resposta = retornaResposta('menu',[])
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, menuNivel1)
    
    # Opções do menu
    elif estado == 1:
        # Opção 1 - Informação do pedido
        if message.text.lower() == '1':
            resposta = retornaResposta('pedido.menu',[])
            helper.cadastraEstado(message.who, menuPedido)
        
        # Opção 2 - Produto no site (https://busca.connectparts.com.br/busca?q=)
        elif message.text.lower() == '2':
            resposta = retornaResposta('produto.menu',[])
            helper.cadastraEstado(message.who, menuProduto)

        # Opção 3 - Vale-crédito
        elif message.text.lower() == '3':
            resposta = retornaResposta('vale.menu',[])
            helper.cadastraEstado(message.who, menuNivel1)

        # Opção 4 - Atendimento no chat
        elif message.text.lower() == '4':
            resposta = retornaResposta('chat.menu',[])
            helper.cadastraEstado(message.who, menuChat)
        
        # Opção 5 - Telefone
        elif message.text.lower() == '5':
            resposta = retornaResposta('telefone.menu',[])
            helper.cadastraEstado(message.who, menuNivel1)

        else:
            resposta = retornaResposta('nenhumaOpcao', [])
        
        mac.send_message(resposta, message.conversation)
    
    # Informações de pedido
    elif estado == 2:
        
        resp = callouts.buscarPedido(message.text)
        
        if resp.status_code == 200:
            dadosPedido = json.loads(resp.text)          
            var = [dadosPedido['CodigoExterno'],dadosPedido['Status']['Descricao'],dadosPedido['Transportadora']['ServicoEntrega']['NumerosRastreio'][0]]  
            resposta = retornaResposta('pedido.dados',var)
            helper.cadastraEstado(message.who, menuNivel1)
        else:
            resposta = retornaResposta('pedido.naoLocalizado',[])
        
        mac.send_message(resposta, message.conversation)
        
    # Buscar produto no site
    elif estado == 3:
        resposta = retornaResposta('produto.link',[])
        resposta += message.text.replace(" ","+")
        mac.send_message(resposta, message.conversation)
        helper.cadastraEstado(message.who, menuNivel1)

    # Entrar no chat
    elif estado == 4:
        if message.text.lower() == '1':
                resposta = retornaResposta('chat.pre',[])
                helper.cadastraEstado(message.who, menuChatCanal)
    
        elif message.text.lower() == '2':
                resposta = retornaResposta('chat.pos',[])
                helper.cadastraEstado(message.who, menuChatCanal)

        mac.send_message(resposta, message.conversation)

    #Link do chat
    elif estado == 5:
        var = [message.text]
        resposta = retornaResposta('chat.link',var)
        helper.cadastraEstado(message.who, menuNivel1)
    
        mac.send_message(resposta, message.conversation)

    else:
        resposta = "Desculpe, mas não entendi a mensagem. "
        mac.send_message(resposta, message.conversation)



def retornaResposta(opcao, variaveis):
    
    if opcao == 'menu':
        resposta = "Olá! É um prazer falar com você. Veja as opções que tenho pra você:\n\n"
        resposta += "1. Informação sobre um pedido. 📦\n"
        resposta += "2. Procurar um produto no site. 🚗\n"
        resposta += "3. Informação sobre como utilizar um vale-crédito ou cupom de desconto. 🎫\n"
        resposta += "4. Falar com um atendente através do chat online. 💬\n"
        resposta += "5. Ver nosso telefone de contato. 📞\n\n"
        resposta += "Digite o número da opção desejada. 😉\n\n"
        resposta += "*DICA*: digite *MENU* a qualquer momento para rever essas opções."
    
    elif opcao == 'pedido.menu':
        resposta = "Por favor, digite um número de pedido válido (ex: 17518648 ou 00K12345678)"

    elif opcao == 'pedido.dados':        
        resposta = "*Pedido*: {0} \n"
        resposta += "*Status*: {1} \n"
        resposta += "*Rastrear*: http://r.connectparts.com.br/?c={2}"
        resposta = resposta.format(*variaveis)
    
    elif opcao == 'pedido.naoLocalizado':
        resposta = "Pedido não localizado."

    elif opcao == 'produto.menu':
        resposta = "Qual é o *ano* e *modelo* do seu carro/moto ?"

    elif opcao == 'vale.menu':
        resposta = "Informações de vale-crédito."

    elif opcao == 'chat.menu':
        resposta = "Ok! Para direcionar você para o atendente certo, digite o número do motivo sobre qual deseja falar:\n\n"
        resposta += "1. Realizar uma compra\n"
        resposta += "2. Falar sobre um pedido"

    elif opcao == 'chat.pre':
        resposta = "Por favor, me fale o seu nome."
       
    elif opcao == 'chat.pos':
        resposta = "Ok, me informe o número do seu pedido."
        
    elif opcao == 'chat.link':
        url = 'https://connectparts.secure.force.com/AssistenteVirtual/ConectaChatLiveAgent?'
        url += 'nome={0}&email={1}&canal={2}&pedido={3}&codigoBtn={4}'.format(*variaveis)

        resposta = "Clique no link para você entrar no chat! "

    elif opcao == 'telefone.menu':
        resposta = "📞 (14) 3311-8100 📞\n\n"
        resposta += "*Horário de atendimento:* \n"
        resposta += "Seg á sex: 9hs às 18h\n"
        resposta += "Sáb: 8hs às 14:15h\n"

    elif opcao == 'produto.link':
        resposta = "Legal! Acesse o link para ver os produtos! https://busca.connectparts.com.br/busca?q="

    elif opcao == 'nenhumaOpcao':
        resposta = "Desculpe, mas não tenho essa opção! Por favor, escolha uma opção do menu."
    
    return resposta