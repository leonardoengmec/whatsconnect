#from app.mac import mac, signals
from modules.Connect import callouts
import os

if __name__ == "__main__":
	enviaMensagensSalesforce()

def enviaMensagensSalesforce():
	listaMensagem = callouts.retornaMensagemSalesforce()
	for msg in listaMensagem:	
		# aqui entraria o rabbitMQ
		#mac.send_message_to('mensagem', 'telefone')
		mac.send_message_to(msg['Name'],msg['mensagem__c'])