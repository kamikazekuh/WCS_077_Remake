import es,popuplib,gamethread,cmdlib

def load():
	cmdlib.registerServerCommand("wcs_raceinfomenu",wrim,"wcsraceinfo_Menu_Handler")
	
def unload():
    cmdlib.unregisterServerCommand("wcs_raceinfomenu")
	
def wrim(args):
	if es.getargv(1) and es.exists("userid",es.getargv(1)):
		genRaceinfoPop('raceinfo_menu_%s'%es.getargv(1), raceinfo_handler, es.getargv(1), es.keygetvalue("wcsuserdata", es.getargv(1), "race"))
	else: es.msg("#green", "Failed.")
	
def checkPop(p):
    if popuplib.exists(p): popuplib.delete(p)
	
def genRaceinfoPop(popupname, callback, userid, race):
	checkPop(popupname)
	raceinfop = popuplib.create("raceinfo_menu_%s"%userid)
	raceinfop.menuselect = raceinfo_handler
	raceinfop.addline("->%s. %s (%s levels/%s skills)"%(race, es.keygetvalue("wcsraces", race, "name"), es.keygetvalue("wcsraces", race, "numberoflevels"), es.keygetvalue("wcsraces", race, "numberofskills")))
	raceinfop.addline("Credits: %s"%es.keygetvalue("wcsraces", race, "author"))
	raceinfop.addline("------------------------")
	numofskills = int(es.keygetvalue("wcsraces", race, "numberofskills"))
	counter = 1
	scounter = 0
	skillnames = es.keygetvalue("wcsraces", race, "skillnames").split("|")
	skilldescr = es.keygetvalue("wcsraces", race, "skilldescr").split("|")
	while(counter <= numofskills):
		raceinfop.addline("->%s. %s"%(counter, skillnames[scounter]))
		raceinfop.addline("%s"%skilldescr[scounter])
		scounter += 1
		counter += 1
	raceinfop.addline("------------------------")
	raceinfop.addline("->8. Back")
	raceinfop.addline("->9. Next")
	gamethread.delayed(0.0001,raceinfop.send,(userid))
	es.keysetvalue("wcsuserdata", userid, "raceinfo", race)

def raceinfo_handler(userid, choice, popupname):
	if choice == 8:
		race = int(es.keygetvalue("wcsuserdata", userid, "raceinfo"))
		race -= 1
		if es.exists("key", "wcsraces", race):
			genRaceinfoPop(popupname, raceinfo_handler, userid, race)
		else:
			checkPop(popupname)
	elif choice == 9:
		race = int(es.keygetvalue("wcsuserdata", userid, "raceinfo"))
		race += 1
		if es.exists("key", "wcsraces", race):
			genRaceinfoPop(popupname, raceinfo_handler, userid, race)
		else:
			checkPop(popupname)
	else:
		checkPop(popupname)