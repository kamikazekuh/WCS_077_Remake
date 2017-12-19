from es import exists, ServerVar, getUseridList
from cmdlib import registerServerCommand, unregisterServerCommand
import tools.wcsgroup.wcsgroup

tools.wcsgroup.wcsgroup.addUser('CT')
tools.wcsgroup.wcsgroup.addUser('T')

def load():
	registerServerCommand('wcsgroup', register, 'Syntax: wcsgroup <get/set>')

	for user in getUseridList():
		tools.wcsgroup.wcsgroup.addUser(user)

def unload():
	unregisterServerCommand('wcsgroup')

	tools.wcsgroup.wcsgroup.delUser('CT')
	tools.wcsgroup.wcsgroup.delUser('T')

def register(args):
	if len(args) >= 1:
		todo = str(args[0]).lower()
		if todo == 'get':
			if len(args) >= 4:
				key = str(args[1])
				var = str(args[2])
				userid = str(args[3])

				team = None
				if len(args) == 5:
					userid = team = {2:'T', 3:'CT'}[int(args[4])]

				if exists('userid', userid) or team is not None:
					if not tools.wcsgroup.wcsgroup.existsUser(userid):
						tools.wcsgroup.wcsgroup.addUser(userid)

					value = tools.wcsgroup.wcsgroup.getUser(userid, key)
					if value is None:
						ServerVar(var).set(0)
					else:
						ServerVar(var).set(value)
				else:
					logging.log('wcsgroup: Information: Unknown userid: '+userid)
					logging.log('wcsgroup: Information: Args: tools.wcsgroup.wcsgroup '+' '.join(map(str, args)))

			else:
				logging.log('wcsgroup: Error: Syntax: wcsgroup get <key> <var> <userid> <[team]>')
				logging.log('wcsgroup: Information: Got: wcsgroup '+' '.join(map(str, args)), 1)

		elif todo == 'set':
			if len(args) >= 4:
				key = str(args[1])
				userid = str(args[2])
				value = str(args[3])

				team = None
				if len(args) == 5:
					userid = team = {2:'T', 3:'CT'}[int(args[4])]

				if exists('userid', userid) or team is not None:
					if not tools.wcsgroup.wcsgroup.existsUser(userid):
						tools.wcsgroup.wcsgroup.addUser(userid)

					tools.wcsgroup.wcsgroup.setUser(userid, key, value)
		
		elif todo == 'foreach':
			var = str(args[1])
			com = str(args[2])
			tools.wcsgroup.wcsgroup.foreach(var, com)
			
		elif todo == 'foreachval':
			var = str(args[1])
			key = str(args[2])
			command = str(args[3])
			tools.wcsgroup.wcsgroup.foreachval(var, key, command)