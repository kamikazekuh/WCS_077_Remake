import cPickle
import es
import os
from cmdlib import registerServerCommand, unregisterServerCommand

wcsusers = {}

def load():
	global wcsusers
	str_path = es.getAddonPath('wcs/wcsusers') + '/wcsusers.db'
	if os.path.isfile(str_path):
		file_users = open(str_path)
		wcsusers = cPickle.load(file_users)
		file_users.close()
	
	registerServerCommand('wcs_keyfilter', Keyfilter, "")
	registerServerCommand('wcs_foreachval', Foreachval, "")
	registerServerCommand('wcs_foreachkey', Foreachkey, "")	
	registerServerCommand('wcs_createsubkey', Keycreatesub, "")
	registerServerCommand('wcs_keysetvalue', Keysetvalue, "")
	registerServerCommand('wcs_keygetvalue', Keygetvalue, "")
	registerServerCommand('wcs_keyexists', Keyexists, "")
	registerServerCommand('wcs_keycreate', Keycreate, "")
	registerServerCommand('wcs_keygroupsave', Keygroupsave, "")
	registerServerCommand('wcs_getplayer2', Getplayer2, "")
		
		
def unload():
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()
	
	unregisterServerCommand('wcs_getplayer2')
	unregisterServerCommand('wcs_keygroupsave')
	unregisterServerCommand('wcs_keyfilter')
	unregisterServerCommand('wcs_foreachval')
	unregisterServerCommand('wcs_foreachkey')
	unregisterServerCommand('wcs_createsubkey')
	unregisterServerCommand('wcs_keysetvalue')
	unregisterServerCommand('wcs_keygetvalue')
	unregisterServerCommand('wcs_keyexists')
	unregisterServerCommand('wcs_keycreate')

def Keygroupsave(args):
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()	
	
def Keyfilter(args):
	varname = str(args[0])
	not_only = str(args[1])
	varvalue = str(args[2])
	for key in list(wcsusers):
		if not_only == "ONLY":
			if wcsusers[key][varname] != varvalue:
				del wcsusers[key]
		if not_only == "NOT":
			if wcsusers[key][varname] == varvalue:
				del wcsusers[key]
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()
			
	
def Foreachval(args):
	buffer = str(args[0])
	key = str(args[1])
	command = str(args[2])
	for value in wcsusers[key]:
		es.ServerVar(buffer).set(value)
		es.server.cmd(command)

def Getplayer2(args):
	userid = str(args[0])
	key = es.getplayersteamid(userid)
	if key == "BOT":
		name = es.getplayername(userid)
		name = name.upper()
		key = "BOT_"+name
	for value in wcsusers[key]:
		if "race_" in value:
			levels = wcsusers[key][value]
			level = levels.split('|')
			es.keysetvalue('wcsuserdata', userid, value, level[0])
			
	
def Foreachkey(args):
	buffer =  str(args[0])
	command = str(args[1])
	for key in wcsusers:
		es.ServerVar(buffer).set(key)
		es.server.cmd(command)
	
def Keycreatesub(args):
	key = str(args[0])
	subkey = str(args[1])
	wcsusers[key][subkey] = {}
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()
		
def Keycreate(args):
	key = str(args[0])
	wcsusers[key] = {}
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()
	
	
def Keyexists(args):
	buffer = str(args[0])
	key = str(args[1])
	if wcsusers.has_key(key):
		es.ServerVar(buffer).set('1')
	else:
		es.ServerVar(buffer).set('0')
	
	
def Keysetvalue(args):
	key = str(args[0])
	subkey = str(args[1])
	value = str(args[2])
	wcsusers[key][subkey] = {}
	wcsusers[key][subkey] = value
	str_path = open(es.getAddonPath('wcs/wcsusers') + '/wcsusers.db', 'w')
	cPickle.dump(wcsusers, str_path)
	str_path.close()
	
def Keygetvalue(args):
	buffer = str(args[0])
	key = str(args[1])
	var = str(args[2])
	value = wcsusers[key][var]
	es.ServerVar(buffer).set(value)
	
def getUseridFromSteamid(steamid):
    for userid in es.getUseridList():
        if steamid == es.getplayersteamid(userid):
            return userid
    return None