import es
import popuplib,gamethread,cmdlib,playerlib
from tools.expand.expand import damage

def load():
	cmdlib.registerServerCommand("wcs_myracemenu",wcrm,"wcschangerace_Menu_Handler")
	es.regclientcmd('myraces', 'tools/myraces/myracecmd', '')
	es.regsaycmd('myraces', 'tools/myraces/myracecmd', '')
	
def unload():
    cmdlib.unregisterServerCommand("wcs_myracemenu")
    es.unregclientcmd('myraces')
    es.unregsaycmd('myraces')
		
def wcrm(args):
	userid = es.getargv(1)
	if userid and es.exists("userid", userid):
		genRacelistPop('myrace_menu_%s'%userid, changerace_handler, userid)
	else: es.msg("#green", "Failed.")	
	
def checkPop(p):
    if popuplib.exists(p): popuplib.delete(p)

def myracecmd():
	userid = es.getcmduserid()
	es.server.queuecmd("es wcs_myracemenu %s" % userid)
		
def genRacelistPop(popupname, callback, userid):
	checkPop(popupname)
	changerace_menu = popuplib.easymenu(popupname, None, callback)
	changerace_menu.settitle('Select Race')
	counter = 1
	counter2 = 0
	while es.exists("key", "wcsraces", counter):
		allow_only = es.keygetvalue("wcsraces", counter, "allow_only")
		steamid = es.getplayersteamid(userid)
		if steamid in allow_only:		
			racename = es.keygetvalue("wcsraces", counter, "name")
			##ADMIN RACE
			if es.keygetvalue("wcsraces", counter, "allow_only") == "<admins>":
				if es.exists("key", "wcsadmin", es.getplayersteamid(userid)):
					if (es.keygetvalue("wcsuserdata", userid, "race_%s"%counter) != None):
						racelevel = es.keygetvalue("wcsuserdata", userid, "race_%s"%counter).split("|")
					else:
						racelevel = 0
					try:
						level = int(racelevel[0])
						if level > 0:
							racename = racename + " (Level %s)"%racelevel[0]
						changerace_menu.addoption(counter, racename)
					except:
						changerace_menu.addoption(counter, racename)
				else:
					racename = racename + " - Admin race"
					changerace_menu.addoption(counter, racename, 0)
			#END ADMIN RACE
			##PRIVATE RACE
			elif es.keygetvalue("wcsraces", counter, "allow_only") != "0":
				usersa = es.keygetvalue("wcsraces", counter, "allow_only").split("|")
				if es.getplayersteamid(userid) in usersa:
					if (es.keygetvalue("wcsuserdata", userid, "race_%s"%counter) != None):
						racelevel = es.keygetvalue("wcsuserdata", userid, "race_%s"%counter).split("|")
					else:
						racelevel = 0
					try:
						level = int(racelevel[0])
						if level > 0:
							racename = racename + " (Level %s)"%racelevel[0]
						changerace_menu.addoption(counter, racename)
					except:
						changerace_menu.addoption(counter, racename)
				else:
					racename = racename + " - Private race"
					changerace_menu.addoption(counter, racename, 0)
			#END PRIVATE RACE
			#TOO LOW LEVEL
			elif int(es.keygetvalue("wcsuserdata", userid, "total_level")) < int(es.keygetvalue("wcsraces", counter, "required_level")):
				levelsneeded = int(es.keygetvalue("wcsraces", counter, "required_level")) - int(es.keygetvalue("wcsuserdata", userid, "total_level"))
				levelsneeded = str(levelsneeded)
				racename = racename + " - %s Levels needed"%levelsneeded
				changerace_menu.addoption(counter, racename, 0)
			#END TOO LOW LEVEL
			elif int(es.keygetvalue("wcsraces", counter, "restrictteam")) == int(es.getplayerteam(userid)):
				racename = racename + " - Restricted Team"
				changerace_menu.addoption(counter, racename, 0)			
			else:
				racelevel = {}
				if (es.keygetvalue("wcsuserdata", userid, "race_%s"%counter) != None):
					racelevel = es.keygetvalue("wcsuserdata", userid, "race_%s"%counter).split("|")
				else:
					racelevel = 0
				try:
					level = int(racelevel[0])
					if level > 0:
						racename = racename + " (Level %s)"%racelevel[0]
					changerace_menu.addoption(counter, racename)
				except:
					changerace_menu.addoption(counter, racename)
			counter2 += 1
		counter += 1
	if counter2 >= 1:
		gamethread.delayed(0.001, changerace_menu.send, userid)
		es.tell(userid, "#multi", "#greenWARNING:#lightgreen If you change race while you are alive you will die.")
	else:
		es.tell(userid, "#multi", "#green[WCS] #lightgreenYou don't have #greenprivate #lightgreenraces!")
	

def changerace_handler(userid, choice, popupname):
	if es.exists("key", "wcsraces", choice):
		##If race is not restricted
		if int(es.keygetvalue("wcsuserdata", userid, "total_level")) < int(es.keygetvalue("wcsraces", choice, "required_level")):
			levelsneeded = str(int(es.keygetvalue("wcsraces", choice, "required_level")) - int(es.keygetvalue("wcsuserdata", userid, "total_level")))
			es.tell(userid, "#multi", "#lightgreenYou cannot choose this race because you are too low level, #green" + levelsneeded + "#lightgreen levels needed.")
		elif es.keygetvalue("wcsraces", choice, "allow_only") == "0":
			changerace_successful(userid, choice)
		elif es.keygetvalue("wcsraces", choice, "allow_only") == "<admins>":
			if not es.exists("key", "wcsadmin", es.getplayersteamid(userid)):
				es.tell(userid, "#multi", "#lightgreenSorry you can't pick this race because it is a#green Admin Only Race")
			else:
				changerace_successful(userid, choice)
		elif es.keygetvalue("wcsraces", choice, "allow_only") != "0":
			users = es.keygetvalue("wcsraces", choice, "allow_only").split("|")
			if es.getplayersteamid(userid) not in users:
				es.tell(userid, "#multi", "#lightgreenSorry you can't pick this race because it is a#green Private Race")
			else:
				changerace_successful(userid, choice)
				
def changerace_successful(userid, race):
	if es.getplayerprop(userid,"CCSPlayer.baseclass.pl.deadflag") == 0:
		es.server.queuecmd("es wcs_dealdamage %s %s 9999" % (userid, userid))
	es.server.queuecmd("es wcs_saveplayer %s"%userid)
	player_race = es.keygetvalue("wcsuserdata", userid, "race")
	command_buffer = es.keygetvalue("wcsraces", player_race, "onchange")
	es.server.queuecmd("es_xset wcs_userid %s" % userid)
	es.server.queuecmd(command_buffer)
	es.server.queuecmd("es_keysetvalue \"wcsuserdata\" %s \"race\" %s"%(userid, race))
	es.server.queuecmd("es wcs_keysetvalue  \"%s\" \"race\" %s"%(es.getplayersteamid(userid), race))
	es.server.queuecmd("es_xset wcs_id \"%s\""%es.getplayersteamid(userid))
	es.server.queuecmd("es_xdoblock wcs/wcsfunctions/wcs_playercheck")
	es.server.queuecmd("es wcs_getplayer %s"%userid)
	es.server.queuecmd("es_keysetvalue \"wcsuserdata\" %s \"skillcheck\" \"1\""%userid)
	es.tell(userid, "#multi", "#lightgreenYou changed your race to#green " + es.keygetvalue("wcsraces", race, "name"))
	old_name = es.keygetvalue("wcsraces", player_race, "name")
	new_name = es.keygetvalue("wcsraces", race, "name")
	es.event('initialize', "wcs_changerace")
	es.event('setint', "wcs_changerace", "userid", int(userid))
	es.event('setstring', "wcs_changerace", "oldrace", str(old_name))
	es.event('setstring', "wcs_changerace", "newrace", str(new_namead))
	es.event('fire', "wcs_changerace")