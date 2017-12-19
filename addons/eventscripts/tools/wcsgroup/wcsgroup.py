import es
keys = {}


def addUser(userid):
	userid = str(userid)
	if not userid in keys:
		keys[userid] = {}

def delUser(userid):
	userid = str(userid)
	if userid in keys:
		del keys[userid]

def existsUser(userid):
	userid = str(userid)
	return userid in keys

def setUser(userid, key, value):
	userid = str(userid)
	addUser(userid)
	keys[userid][key] = value

def getUser(userid, key):
	userid = str(userid)
	addUser(userid)
	if key in keys[userid]:
		value = str(keys[userid][key])
		if value.isdigit():
			return int(value)
		return value
	return None

def foreach(variable, command):
	for user in es.getUseridList():
		es.ServerVar(variable).set(user)
		es.server.queuecmd(command)

def foreachval(var, key, command):
	for x in keys[key]:
		es.ServerVar(var).set(x)
		es.server.queuecmd(command)