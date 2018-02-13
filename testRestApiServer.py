import web
import json
import time

DOORS = [("door1","6nUfj1KUZ6jhE5ajCG6L5hawb1K2Zgmu")]
CARDS = {'door1': [917278450733,568565435597]}

def response(status = 'ok', error = None):
	''' status = ok | rejected | error '''
	#error = None
	if not status in ['ok', 'rejected', 'error']: 
		status = 'error'
		error = 'NA status'
	D = {'status': status, 'time': time.strftime("%y%m%d%H%M%S"), 'error': error}
	return json.dumps(D)

class doorlock:
	def POST(self):
		try:
			data = web.data()
			D = json.loads(data.decode())
			if not (D['doors'],D['authToken']) in DOORS: return response("error","Invalid doors")
			if not D['card'] in CARDS[D['doors']]: return response("rejected")
			return response()
		except Exception as e:
			return response("error",str(e))


urls = (
	'/api/k4/doorlock', 'doorlock'
)

app = web.application(urls,globals())

if __name__ == '__main__':
	app.run()
