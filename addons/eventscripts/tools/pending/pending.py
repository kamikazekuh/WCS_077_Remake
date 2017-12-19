import es
import popuplib

def unload():
	es.addons.unregisterTickListener(pending)

def load():
	es.addons.registerTickListener(pending)
		
	
def pending():
	for userid in es.getUseridList():
		if not es.isbot(userid):
			status = popuplib.active(userid)
			if status['count'] >= 3:
				popuplib.close(status['name'], userid)
		