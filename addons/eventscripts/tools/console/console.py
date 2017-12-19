import es
from es import ServerVar, exists
import playerlib
from playerlib import getPlayer as gP
from cmdlib import registerServerCommand, unregisterServerCommand
pyfilter = ("#alive", "#all", "#bot", "#ct", "#dead", "#human", "#spec", "#t", "#un")
filter_table = (("t","#t"), ("c","#ct"), ("3","#ct"), ("2","#t"), ("s","#spec"), ("1","#spec"), ("u","#un"), ("h","#human"), ("b","#bot"), ("l","#alive"), ("a","#all"), ("d","#dead"))



def load():
	registerServerCommand('wcs_decimal', decimalRegister, 'Syntax: wcs_decimal <var> <amount>')
	registerServerCommand('wcs_getindex', indexRegister, 'Syntax: wcs_getindex <var> <userid>')
	registerServerCommand('wcs_isnumeric', numericRegister, 'Syntax: wcs_isnumeric <var> <value>')
	registerServerCommand('wcs_near', nearRegister, 'Syntax: wcs_near <variable> <filter> <distance> <userid> <command>')
	registerServerCommand('wcs_fade', fadeRegister, 'Syntax: wcs_fade <identifier> <type> <fade time> <total time> <Red> <Green> <Blue> <Alpha>')
	registerServerCommand('wcs_blind', blindRegister, 'Syntax: wcs_blind <userid> <red> <green> <blue> <alpha>')
	registerServerCommand('wcs_unblind', unblindRegister, 'Syntax: wcs_unblind <userid>')
	registerServerCommand('wcs_capitalize', capitRegister, 'Syntax: wcs_capitalize <var> <string>')
 
def unload():
	unregisterServerCommand('wcs_decimal')
	unregisterServerCommand('wcs_getindex')
	unregisterServerCommand('wcs_isnumeric')
	unregisterServerCommand('wcs_near')
	unregisterServerCommand('wcs_fade')
	unregisterServerCommand('wcs_blind')
	unregisterServerCommand('wcs_unblind')
	unregisterServerCommand('wcs_capitalize')
	
def capitRegister(args):
	var = str(args[0])
	string = str(args[1])
	es.ServerVar(var).set(string.upper())
	
def unblindRegister(args):
	userid = str(args[0])
	es.server.queuecmd("es wcs_fade %s 2 1 1 255 255 255 0" % userid)
	
def blindRegister(args):
	userid = str(args[0])
	red = str(args[1])
	green  = str(args[2])
	blue = str(args[3])
	alpha = str(args[4])
	es.server.queuecmd("es wcs_fade %s 2 1 1 %s %s %s %s" % (userid, red, green, blue, alpha))
	
	
def fadeRegister(args):
	userid = str(args[0])
	type = str(args[1])
	fadetime = str(args[2])
	totaltime = str(args[3])
	r = str(args[4])
	g = str(args[5])
	b = str(args[6])
	a = str(args[7])
	t = int(type)
	if t == 1:
		type = 2
	elif t == 0:
		type = 1
	else:
		type = 8 + 16
	es.usermsg("create", "fade", "Fade")
	es.usermsg("write", "short", "fade", float(fadetime) * 1000)
	es.usermsg("write", "short", "fade", float(totaltime) * 1000)
	es.usermsg("write", "short", "fade", int(type))
	es.usermsg("write", "byte", "fade", int(r))
	es.usermsg("write", "byte", "fade", int(g))
	es.usermsg("write", "byte", "fade", int(b))
	es.usermsg("write", "byte", "fade", int(a))
	es.usermsg("send", "fade", userid)
	es.usermsg("delete", "fade")
	
	
def nearRegister(args):
	variable = str(args[0])
	users = str(args[1])
	distance = str(args[2])
	baseuser = str(args[3])
	command = str(args[4])
	vec = es.getplayerprop(baseuser, "CBaseEntity.m_vecOrigin").split(",")
	nearcoord(variable, users, distance, float(vec[0]), float(vec[1]), float(vec[2]), command)

def nearcoord(variable, users, distance, x, y, z, command):
	filter = getusers(users)
	players = playerlib.nearCoord((float(x), float(y), float(z)), float(distance))
	for player in players:
		userid = player.userid
		if userid in filter:
			es.ServerCommand("es_set %s %s" % (variable, userid))
			es.ServerCommand(command)
	
def numericRegister(args):
	if len(args) == 2:
		var = str(args[0])
		value = str(args[1])
		if value.startswith("-"):
			value = value[1:]
	value = value.replace(".", "")
	if value.isdigit():
		ServerVar(var).set("1")
	else:
		ServerVar(var).set("0")

	
def decimalRegister(args):
	if len(args) == 2:
		var = str(args[0])
		amount = str(args[1])
		ServerVar(var).set(round(float(amount)))			
				
def indexRegister(args):
	if len(args) == 2:
		var, userid = map(str, args)
 
		if exists('userid', userid):
			ServerVar(var).set(gP(userid).index)
		else:
			ServerVar(var).set(0)
 
def getusers(users):
	# http://www.eventscripts.com/pages/Est_PlayerSelection
	# Python style #alive, #all, #bot, #ct, #dead, #human, #spec, #t, #un
	# EST style #a, #c, #3, #t, #2, #s, #1, #u, #0, #h, #b, #l, #d
	# ex1: #alive,#ct (for CT who is alive)
	# ex2: #23!d (for all T and CT who is alive)
	# issue: names start with # are not supported
	global pyfilter
	if str(users).startswith("#"):
		status = 0
		notfilter = ""
		if "," in users:
			status = 1
		if "!" in users:
			all = users.split("!")
			users = all[0]
			notfilter = all[1]
			status = 2
		if status == 0:
			if users in pyfilter:
				status = 1
			else:
				status = 2
		if status == 2:
			global filter_table
			filter = []
			for item in filter_table:
				if item[0] in users:
					idlist = playerlib.getUseridList(item[1])
					filter.extend(idlist)
			users = set(filter)
			if notfilter != "":
				filter = []
				for item in filter_table:
					if item[0] in notfilter:
						idlist = playerlib.getUseridList(item[1])
						filter.extend(idlist)
				notfilter = set(filter)
				for item in notfilter:
					if int(item) in users:
						users.remove(int(item))
		else:
			users = playerlib.getUseridList(users)
		return users
	allusers = es.getUseridList()
	if not isinstance(users, tuple) and not isinstance(users, list):
		user = finduserid(users, allusers)
		if user:
			return (user,)
		return ()
	test = []
	for user in users:
		user = finduserid(user, allusers)
		if user:
			test.append(user)
	return users
	
def finduserid(user, allusers):
	if isinstance(user, basestring) and user.isdigit():
		user = int(user)
	if isinstance(user, int):
		if es.exists("userid", user):
			return user
		user = str(user)
	for userid in allusers:
		if user == es.getplayersteamid(userid):
			return userid
	for userid in allusers:
		if user == es.getplayername(userid):
			return userid
	for userid in allusers:
		if user in es.getplayername(userid):
			return userid
	return None