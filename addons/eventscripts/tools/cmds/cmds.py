from es import exists, getplayerlocation, getplayerhandle, ServerVar, server
from cmdlib import registerServerCommand, unregisterServerCommand
import tools.expand.expand
import time

starttime = time.time()

def load():
	registerServerCommand('wcs', register, 'wcs <damage/explode/spawn/strip/drop/push/pushto/gravity/removeweapon/getviewplayer/getviewentity/keyhint/give/fire/extinguish/drug/drunk/poison> <userid>')
	registerServerCommand('wcs_uptime', register_uptime, 'wcs_uptime <var>')
	registerServerCommand('wcs_reset_cooldown', register_cooldown, 'wcs_reset_cooldown <userid>')
	

def register_cooldown(args):
	if len(args) == 1:
		userid = str(args[0])
		server.queuecmd('es_keysetvalue WCSuserdata %s ultimate 0' % (userid))

def unload():
	unregisterServerCommand('wcs')
	unregisterServerCommand('wcs_uptime')
	unregisterServerCommand('wcs_reset_cooldown')
	
def register_uptime(args):
	if len(args) == 1:
		var = str(args[0])
		global starttime
		ServerVar(var).set(time.time() - starttime)	

def register(args):
	if len(args) >= 2:
		todo = str(args[0]).lower()
		userid = str(args[1])

		if exists('userid', userid):
			if todo == 'damage':
				if len(args) >= 4:
					v,q,w = int(args[2]) if int(args[2]) else None, int(args[4]) if len(args) >= 5 else False, str(args[5]) if len(args) == 6 else None
					tools.expand.expand.damage(userid, str(args[3]), v, q, w)
					#server.insertcmd('damage %s %s 32 %s'%(userid, int(float(args[3])), str(args[2])))

			elif todo == 'explode':
				if len(args) == 5:
						magnitude = round(float(args[3]) * float(args[4]) / 150)
						#server.damage(args[2], magnitude, 32, userid)
						tools.expand.expand.damage(args[2], magnitude, userid)
						#player.damage(magnitude, 32, args[2])
						#server.insertcmd('damage %s %s 32 %s'%(args[2], magnitude, userid))

			elif todo == 'spawn':
				if len(args) in (2,3):
					tools.expand.expand.spawn(userid, int(args[2]) if len(args) == 3 else False)

			elif todo == 'strip':
				if len(args) == 2:
					tools.expand.expand.strip(userid)

			elif todo == 'drop':
				if len(args) == 3:
					tools.expand.expand.drop(userid, args[2])

			elif todo == 'push':
				if len(args) >= 3:
					tools.expand.expand.push(userid, args[2], args[3] if len(args) >= 4 else 0, args[4] if len(args) == 5 else 0)

			elif todo == 'pushto':
				if len(args) == 4:
					tools.expand.expand.pushto(userid, args[2], args[3])

			elif todo == 'gravity':
				if len(args) == 3:
					tools.expand.expand.gravity(userid, args[2])

			elif todo == 'removeweapon':
				if len(args) == 3:
					tools.expand.expand.removeWeapon(userid, args[2])

			elif todo == 'getviewplayer':
				if len(args) == 3:
					v = tools.expand.expand.getViewPlayer(userid)
					ServerVar(args[2]).set(v if v is not None else 0)

			elif todo == 'getviewentity':
				if len(args) == 3:
					v = tools.expand.expand.getViewEntity(userid)
					ServerVar(args[2]).set(v if v is not None else 0)

			elif todo == 'keyhint':
				if len(args) >= 3:
					tools.expand.expand.keyHint(userid, ' '.join(map(str, args[3:])))

			elif todo == 'give':
				if len(args) == 3:
					tools.expand.expand.give(userid, args[2])

			elif todo == 'fire':
				if len(args) >= 2:
					tools.expand.expand.fire(userid, args[2] if len(args) == 3 else 0)

			elif todo == 'extinguish':
				if len(args) == 2:
					tools.expand.expand.extinguish(userid)

			elif todo == 'drug':
				if len(args) >= 2:
					tools.expand.expand.drug(userid, float(args[2]) if len(args) >= 3 else 0)

			elif todo == 'drunk':
				if len(args) >= 2:
					tools.expand.expand.drunk(userid, float(args[2]) if len(args) >= 3 else 0, int(args[3]) if len(args) == 4 else 155)

			elif todo == 'poison':
				if len(args) == 5:
					tools.expand.expand.dealPoison(userid, int(float(args[3])), str(args[2]), int(args[4]))

			elif todo == 'changeteam':
				if len(args) == 3:
					tools.expand.expand.changeTeam(userid, str(args[2]))