# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    name="Connect Bot",
    trainer='chatterbot.trainers.ListTrainer',
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter='chatterbot.output.TerminalAdapter',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database='chatterbot-database'
    
)
trainer = ListTrainer(chatbot)
trainer.train([
    "Olá, sou o assistente virtual. Como posso ajudar?",
    "Quero saber sobre meu pedido",
    "Por favor, me diga o número do pedido",
    "1745495",
    "O status do seu pedido é DESPACHADO"
])

print('Digite alguma coisa..')

while True:
    try:
        bot_input = chatbot.get_response(None)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break




