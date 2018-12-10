from app.mac import mac, signals
from modules.Connect import callouts
import os

@signals.initialized.connect
def handle(entity):

	listaMensagem = callouts.retornaMensagemSalesforce()
	for msg in listaMensagem:	
		# aqui entraria o rabbitMQ
		#mac.send_message_to('mensagem', 'telefone')
		mac.send_message_to(msg['Name'],msg['mensagem__c'])