#! /usr/bin/env python
import SimpleMFRC522 as RF
import RPi.GPIO as GPIO
import time
import requests
import json
import logging
logger = logging.getLogger('RFIDdoorlock')

URL = 'http://localhost:8080/api/k4/doorlock'
KEY = '6nUfj1KUZ6jhE5ajCG6L5hawb1K2Zgmu'
DOOR = 'door1'

TIME_DELAY = 2.0
PIN = 5 # must be BCM
PIN_NEGATIVE = True
DEBUG = True

class RFIDdoorlock:
	def __init__(s,pin,door,key,negative=PIN_NEGATIVE,timeDelay=TIME_DELAY):
		s.pin = pin
		s.door = door
		s.key = key
		s.negative = negative
		s.timeDelay = timeDelay
		s.running = True
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(s.pin,GPIO.OUT,initial=s.negative)
		s.RF = RF.SimpleMFRC522()
		
	def rfEvent(s,cardId):
		if DEBUG: print("rfEvent "+str(cardId))
		try:
			D = {'card':cardId,'doors':s.door,'authToken':s.key}
			response = requests.post(URL,data=json.dumps(D))
			R = response.json()
			if DEBUG: print(R)
			if R['status'] == 'ok': s.openDoor()
		except Exception as e:
			logger.error('Failed: '+ str(e))

	def openDoor(s):
		GPIO.output(s.pin,not s.negative)
		time.sleep(s.timeDelay)
		GPIO.output(s.pin,s.negative)

	def listen(s):
		while s.running:
			time.sleep(0.1)
			id = s.RF.read_id_no_block()
			if id: s.rfEvent(id)
			GPIO.output(s.pin,s.negative)
		
	def cleanup(s):
		s.running = False
		GPIO.cleanup()
		
if __name__ == '__main__':
	rf = RFIDdoorlock(PIN,DOOR,KEY)
	try:
		rf.listen()
	except KeyboardInterrupt:
		pass
	rf.cleanup()
