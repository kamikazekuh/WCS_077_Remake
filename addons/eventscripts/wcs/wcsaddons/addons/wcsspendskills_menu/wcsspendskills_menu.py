import es
import popuplib,gamethread,cmdlib,playerlib

def load():
	cmdlib.registerServerCommand("wcs_spendskillsmenu",wssm,"wcsspendskills_Menu_Handler")
	
def unload():
    cmdlib.unregisterServerCommand("wcs_spendskillsmenu")
	
def wssm(args):
	userid = es.getargv(1)
	if userid and es.exists("userid", userid):
		genSkillsPop('spendskills_menu_%s'%userid, spendskills_handler, userid)
	else: es.msg("#green", "Failed.")
	
def checkPop(p):
    if popuplib.exists(p): popuplib.delete(p)
	
def genSkillsPop(popupname, callback, userid):
	checkPop(popupname)
	skills_menu = popuplib.easymenu(popupname, None, callback)
	steamid = es.getplayersteamid(userid)
	race = es.keygetvalue("wcsuserdata", userid, "race")
	racename = es.keygetvalue("wcsraces", race, "name")
	unusedp = es.keygetvalue("wcsuserdata", userid, "unused")
	level = int(es.keygetvalue("wcsuserdata", userid, "level"))
	ultimatelevel = es.getInt("wcs_ultimatelevel")
	numoflevels = int(es.keygetvalue("wcsraces", race, "numberoflevels"))
	numofskills = int(es.keygetvalue("wcsraces", race, "numberofskills"))
	skillnames = es.keygetvalue("wcsraces", race, "skillnames").split("|")
	counter = 1
	scounter = 0
	skills_menu.settitle("Select Skill to Level (%s Unused Points):"%unusedp)
	while(counter <= numofskills):
		skill = "skill_%s"%counter
		skillname = skillnames[scounter]
		skilllevel = int(es.keygetvalue("wcsuserdata", userid, skill))
		if skilllevel < numoflevels:
			if counter != numofskills:
				skills_menu.addoption(counter, "%s : %s > %s"%(skillname, skilllevel, skilllevel +1))
			else:
				if level >= ultimatelevel:
					skills_menu.addoption(counter, "%s (ultimate) : %s > %s"%(skillname, skilllevel, skilllevel +1))
				else:
					skills_menu.addoption(counter, "%s (ultimate) : %s > %s"%(skillname, skilllevel, skilllevel +1), 0)
		counter += 1
		scounter += 1
	skills_menu.send(userid)


def spendskills_handler(userid, choice, popupname):
	if es.exists("key", "wcsuserdata", userid):
		allowed = 0
		race = es.keygetvalue("wcsuserdata", userid, "race")
		unused = int(es.keygetvalue("wcsuserdata", userid, "unused"))
		level = int(es.keygetvalue("wcsuserdata", userid, "level"))
		ultimatelevel = es.getInt("wcs_ultimatelevel")
		numoflevels = int(es.keygetvalue("wcsraces", race, "numberoflevels"))
		numofskills = int(es.keygetvalue("wcsraces", race, "numberofskills"))
		skillnames = es.keygetvalue("wcsraces", race, "skillnames").split("|")
		if choice != 10:
			if unused > 0:
				if choice <= numofskills:
					skill = "skill_%s"%choice
					skilllevel = int(es.keygetvalue("wcsuserdata", userid, skill))
					if skilllevel < numoflevels:
						if choice == numofskills:
							if level >= ultimatelevel:
								allowed = 1
						else:
							allowed = 1
					if allowed == 1:
						skilllevel += 1
						unused -= 1
						es.keysetvalue("wcsuserdata", userid, skill, skilllevel)
						es.keysetvalue("wcsuserdata", userid, "unused", unused)
						skillname = skillnames[choice - 1]
						if skilllevel == 1:
							es.tell(userid, "#multi", "#lightgreenCongratulations, your new skill#green %s#lightgreen, is now level#green %s#lightgreen. Some skills are activated#green next round."%(skillname, skilllevel))
						else:
							es.tell(userid, "#multi", "#lightgreenYour skill#green %s#lightgreen, is now level#green %s#lightgreen."%(skillname, skilllevel))
					es.keysetvalue("wcsuserdata", userid, "skillcheck", 1)
			else:
				es.tell(userid, "#multi", "#lightgreenYou have no free#green Skill Points")
		if unused > 0:
			es.delayed(0.1, "wcs_spendskillsmenu %s"%userid)
						
			