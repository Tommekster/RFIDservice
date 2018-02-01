#! /usr/bin/env python
import SimpleMFRC522 as RF
import RPi.GPIO as GPIO
import socket
import threading
import time

HOST = ''
#HOST = '127.0.0.1'
PORT = 50007
DEBUG = True

class RFIDservice:
	def __init__(s,host,port):
		s.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.socket.bind((host,port))
		s.socket.listen(5)
		s.clients = []
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
		if len(s.clients) == 0: return
		if DEBUG: print("clients "+str(len(s.clients)))
		for c in s.clients:
			msg = str(cardId)+"\r\n"
			try: 
				c.sendall(msg.encode('utf-8'))
				c.close()
			except: disconnected.append(c)
		s.clients = []

	def listen(s):
		if not s.running: return
		while True:
			conn, addr = s.socket.accept()
			s.clients.append(conn)
			if DEBUG: print("new connection "+str(addr))
		
	def cleanup(s):
		s.running = False
		s.socket.close()
		GPIO.cleanup()
		
if __name__ == '__main__':
	rf = RFIDservice(HOST,PORT)
	try:
		rf.listen()
	except KeyboardInterrupt:
		pass
	rf.cleanup()
