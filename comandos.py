from app.mac import mac, signals
from modules.Connect import callouts
import os
import threading

@signals.initialized.connect
def enviaMensagensSalesforce(texto):
	print(texto)
	listaMensagem = callouts.retornaMensagemSalesforce()
	for msg in listaMensagem:	
		# aqui entraria o rabbitMQ
		#mac.send_message_to('mensagem', 'telefone')
		mac.send_message_to(msg['mensagem__c'],msg['Name'])
		setTimeOut(10) # 5 seconds

def setTimeOut(sec):
	print('Rodou envia mensagens salesforce!!!')
	def func_wrapper():
		enviaMensagensSalesforce('')
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t