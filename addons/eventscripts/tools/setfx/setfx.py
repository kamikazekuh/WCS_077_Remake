import es
import cmdlib
import playerlib
import gamethread
import logging
reload(logging)

import tools.wcsgroup.wcsgroup as wcsgroup
import tools.expand.expand as expand

def load():
	cmdlib.registerServerCommand('wcs_setfx', setfx, 'wcs_setfx <type> <userid> <operator> <value> <time>')
	
def unload():
	cmdlib.unregisterServerCommand('wcs_setfx')
	cmdlib.unregisterServerCommand('wcs_removefx')

	
def setfx(args):
	if len(args) == 5:
		type = args[0]
		if not type in 'freeze|jetpack|god|noblock|burn|speed|health|armor|cash|gravity|ulti_immunity|disguiser|1stclip|2ndclip|longjump|lj|invisp|location|blind|evade':
			logging.log('wcs_setfx: '+type+' is not a valid type.')
			type = 0
		uid = args[1]
		op = args[2]
		if not op in '=|+|-':
			op = "="
		value = float(args[3])
		time = float(args[4])
		player = playerlib.getPlayer(uid)
		if type == 'freeze':
			if op == '=':
				speed = float(player.getSpeed())
				wcsgroup.setUser(uid, 'speed', speed)
				if value >= 1:
					player.setSpeed(0)
				if time > 0:
					gamethread.delayed(time, player.setSpeed, speed, 0)
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')
			
		if type == 'god':
			if op == '=':
				player.godmode(int(value))
				if time > 0:
					gamethread.delayed(time, player.godmode, 0, 0)
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')
				
		if type == 'ulti_immunity':
			if op == '=':
				wcsgroup.setUser(uid, 'ulti_immunity', value)
				if time > 0:
					if value == 1:
						value = 0
					if value == 0:
						value = 1
					wcsgroup.setUser(uid, 'ulti_immunity', value)
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')
		
		if type == 'jetpack':
			if op == '=':
				player.jetpack(int(value))
				if time > 0:
					gamethread.delayed(time, player.jetpack, 0, 0)
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')
				
		if type == 'noblock':
			if op == '=':
				player.noblock(int(value))
				if time > 0:
					gamethread.delayed(time, player.noblock, 0, 0)
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')
				
		if type == 'burn':
			if op == '=':
				if value == 1:
					es.set('wcs_uid', uid)
					es.set('wcs_time', time)
					es.server.queuecmd('es wcs fire server_var(wcs_uid) server_var(wcs_time)')
					es.delayed(time, 'es wcs extinguish server_var(wcs_uid)')
				if value == 0:
					es.set('wcs_uid', uid)
					es.server.queuecmd('es wcs extinguish server_var(wcs_uid)')
			else:
				logging.log('wcs_setfx: '+type+' can only use values 1 or 0.')	
				
		if type == 'speed':
			speed = float(player.getSpeed())
			if op == '=':
				player.setSpeed(value)
				if time > 0:
					gamethread.delayed(time, player.setSpeed, speed, 0)
			if op == '+': 
				player.setSpeed(value+speed)
				if time > 0:
					gamethread.delayed(time, player.setSpeed, speed, 0)
			if op == '-':
				player.setSpeed(speed-value)
				if time > 0:
					gamethread.delayed(time, player.setSpeed, speed, 0)
			
		if type == 'health':
			health = float(player.getHealth())
			if op == '=':
				player.setHealth(value)
				if time > 0:
					gamethread.delayed(time, player.setHealth, health, 0)
			if op == '+': 
				player.setHealth(value+health)
				if time > 0:
					gamethread.delayed(time, player.setHealth, health, 0)
			if op == '-':
				player.setHealth(health-value)
				if time > 0:
					gamethread.delayed(time, player.setHealth, health, 0)
		
		if type == 'armor':
			armor = float(player.getArmor())
			if op == '=':
				player.setArmor(value)
				if time > 0:
					gamethread.delayed(time, player.setArmor, armor, 0)
			if op == '+': 
				player.setArmor(value+armor)
				if time > 0:
					gamethread.delayed(time, player.setArmor, armor, 0)
			if op == '-':
				player.setArmor(armor-value)
				if time > 0:
					gamethread.delayed(time, player.setArmor, armor, 0)
					
		if type == 'cash':
			cash = float(player.getCash())
			if op == '=':
				player.setCash(value)
				if time > 0:
					gamethread.delayed(time, player.setCash, cash, 0)
			if op == '+': 
				player.setCash(value+cash)
				if time > 0:
					gamethread.delayed(time, player.setCash, cash, 0)
			if op == '-':
				player.setCash(cash-value)
				if time > 0:
					gamethread.delayed(time, player.setCash, cash, 0)
					
		if type == 'disguiser':
			team = player.teamid()
			if team == 2:
				if es.ServerVar('wcs_game') == cstrike:
					player.setModel('player/ct_urban')
					if time > 0:
						gamethread.delayed(time, player.setModel, 'player/t_pheonix', 0)
				if es.ServerVar('wcs_game') == dod:
					player.setModel('player/american_assault')
					if time > 0:
						gamethread.delayed(time, player.setModel, 'player/american_assault', 0)
			if team == 3:
				if es.ServerVar('wcs_game') == cstrike:
					player.setModel('player/t_phoenix')
					if time > 0:
						gamethread.delayed(time, player.setModel, 'player/ct_urban', 0)
				if es.ServerVar('wcs_game') == dod:
					player.setModel('player/german_assault')
					if es.ServerVar('wcs_game') == dod:
						player.setModel('player/american_assault')
						if time > 0:
							gamethread.delayed(time, player.setModel, 'player/german_assault', 0)
			
		if type == '1stclip':
			weapon = player.getPrimary()
			clip = float(player.getClip(weapon))
			if op == '=':
				player.setClip(weapon, value)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
			if op == '+': 
				player.setClip(weapon, value+clip)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
			if op == '-':
				player.setClip(weapon, clip-value)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
					
		if type == '2ndclip':
			weapon = player.getSecondary()
			clip = float(player.getClip(weapon))
			if op == '=':
				player.setClip(weapon, value)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
			if op == '+': 
				player.setClip(weapon, value+clip)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
			if op == '-':
				player.setClip(weapon, clip-value)
				if time > 0:
					gamethread.delayed(time, player.setClip, (weapon,clip), 0)
		
		if type == 'gravity':
			if wcsgroup.getUser(uid, 'gravity') != None:
				gravity = float(wcsgroup.getUser(uid, 'gravity'))
			else:
				gravity = 1.0
			if op == '=':
				expand.gravity(uid, value)
				wcsgroup.setUser(uid, 'gravity', value)
				if time > 0:
					gamethread.delayed(time, expand.gravity, (uid, gravity), 0)
			if op == '+':
				expand.gravity(uid, value+gravity)
				wcsgroup.setUser(uid, 'gravity', value+gravity)
				if time > 0:
					gamethread.delayed(time, expand.gravity, (uid, gravity), 0)
			if op == '-':
				expand.gravity(uid, gravity-value)
				wcsgroup.setUser(uid, 'gravity', gravity-value)
				if time > 0:
					gamethread.delayed(time, expand.gravity, (uid, gravity), 0)
					
		if type == 'invisp':
			try:
				invisp = int(wcsgroup.getUser(uid, 'invisp'))
			except:
				invisp = 255
			if value > 100:
				value = 100
			value2 = ((value - 100) * -2.55)
			if op == '=':
				player.setColor(255, 255, 255, value2)
				wcsgroup.setUser(uid, 'invisp', value2)
				if time > 0:
					gamethread.delayed(time, player.setColor, (255, 255, 255, invisp), 0)
			if op == '+':
				player.setColor(255, 255, 255, value2+invisp)
				wcsgroup.setUser(uid, 'invisp', value2+invisp)
				if time > 0:
					gamethread.delayed(time, player.setColor, (255, 255, 255, invisp), 0)
			if op == '-':
				player.setColor(255, 255, 255, invisp-value2)
				wcsgroup.setUser(uid, 'invisp', invisp-value2)
				if time > 0:
					gamethread.delayed(time, player.setColor, (255, 255, 255, invisp), 0)
					
		if type == 'longjump':
			longjump = float(wcsgroup.getUser(uid, 'longjump'))
			if op == '=':
				wcsgroup.setUser(uid, 'longjump', value)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'longjump', longjump), 0)
			if op == '+':
				wcsgroup.setUser(uid, 'longjump', value+longjump)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'longjump', longjump), 0)
			if op == '-':
				wcsgroup.setUser(uid, 'longjump', longjump-value)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'longjump', longjump), 0)
		
		if type == 'location':
			location = float(player.getLocation())
			vector = es.createvectorstring(location)
			if op != '=':
				logging.log('wcs_setfx: Location uses = only as an operator.')
			if op == '=':
				player.setLocation(value)
				if time > 0:
					gamethread.delayed(time, player.setLocation, vector)
		
		if type == 'blind':
			if value > 100:
				value = 100
			value2 = ((value - 100) * -2.55)
			if op == '=':
				player.blind(value2, time)
			else:
				logging.log('wcs_setfx: Blind uses = only as an operator.')

		if type == 'evade':
			evade = float(wcsgroup.getUser(uid, 'evade'))
			if op == '=':
				wcsgroup.setUser(uid, 'evade', value)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'evade', evade), 0)
			if op == '+':
				wcsgroup.setUser(uid, 'evade', value+evade)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'evade', evade), 0)
			if op == '-':
				wcsgroup.setUser(uid, 'evade', evade-value)
				if time > 0:
					gamethread.delayed(time, wcsgroup.setUser, (uid, 'evade', evade), 0)
		
