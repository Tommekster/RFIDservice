#! /usr/bin/env python
import SimpleMFRC522 as RF
import RPi.GPIO as GPIO
import threading
import time
from websocket_server import WebsocketServer

HOST = ''
#HOST = '127.0.0.1'
PORT = 50007
DEBUG = True

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	#server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])

class RFIDwebsocket:
	def __init__(s,host,port):
		s.server = WebsocketServer(port,host=host)
		if DEBUG:
			s.server.set_fn_new_client(new_client)
			s.server.set_fn_client_left(client_left)
		s.running = True
		s.RF = RF.SimpleMFRC522()
		def poolRF():
			while s.running:
				time.sleep(0.1)
				id = s.RF.read_id_no_block()
				if id: s.rfEvent(id)
		threading.Thread(target=poolRF).start()
		
	def rfEvent(s,cardId):
		if DEBUG: print("rfEvent "+str(cardId))
		msg = str(cardId)+"\r\n"
		#c.sendall(msg.encode('utf-8'))
		s.server.send_message_to_all(msg)

	def listen(s):
		if not s.running: return
		s.server.run_forever()
		
	def cleanup(s):
		s.running = False
		GPIO.cleanup()
		
if __name__ == '__main__':
	rf = RFIDwebsocket(HOST,PORT)
	try:
		rf.listen()
	except KeyboardInterrupt:
		pass
	rf.cleanup()

