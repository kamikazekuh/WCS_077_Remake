# wcs PlayerInfo Menu Handler by MiB
import es,popuplib,cmdlib,gamethread
popups = ["wum_menu_","wum_menu_playerinfo_"]

def load():
    cmdlib.registerServerCommand("wcs_usersmenu",wum,"wcsusers_Menu_Handler")

def unload():
    cmdlib.unregisterServerCommand("wcs_usersmenu")

def wum(args):
	if es.getargv(1) and es.exists("userid",es.getargv(1)):
		genPlayerlistPop('%s%s'%(popups[0],es.getargv(1)), playerSelect).send(es.getargv(1))
	else: es.msg("#green", "Failed.")

def wum_handler(userid,choice,popupname):
	wum_playerinfo = popuplib.create("%s%s"%(popups[1],userid))
	wum_playerinfo.menuselect = wum_playerinfo_handler
	wum_playerinfo.addline("->1. %s"%es.getplayername(choice))
	wum_playerinfo.addline("-----------------------")
	wum_playerinfo.addline("TLevel: %s"%es.keygetvalue("wcsuserdata",choice,"total_level"))
	wum_playerinfo.addline("-----------------------")
	race = es.keygetvalue("wcsuserdata",choice,"race")
	wum_playerinfo.addline("o %s : %s"%(es.keygetvalue("wcsraces",race,"name"),es.keygetvalue("wcsuserdata",choice,"level")))
	numberofskills = int(es.keygetvalue("wcsraces",race,"numberofskills"))
	if numberofskills > 0:
		counter = 1
		scounter = 0
		skillnames = es.keygetvalue("wcsraces",race,"skillnames").split("|")
		while counter <= numberofskills:
			level = es.keygetvalue("wcsuserdata",choice,"skill_%s"%(counter))
			if not level or level == 0:
				level = 0
			wum_playerinfo.addline("- %s : %s"%(skillnames[scounter],level))
			scounter += 1
			counter += 1
	wum_playerinfo.addline("-----------------------")
	skulls = 0
	if es.keygetvalue("wcsuserdata",choice,"skulls"): skulls = int(es.keygetvalue("wcsuserdata",choice,"skulls"))
	if skulls and skulls != 0:
		wum_playerinfo.addline("- skulls: %s%%"%skulls)
	speed = 0
	if es.keygetvalue("wcsuserdata",choice,"speed"): speed = float(es.keygetvalue("wcsuserdata",choice,"speed"))
	if speed and speed != 0:
		speed = int(round(speed * 100))
		if speed != 100 and speed != 0: wum_playerinfo.addline("- speed: %s%%"%speed)
	gravity = 0
	if es.keygetvalue("wcsuserdata",choice,"gravity"): gravity = float(es.keygetvalue("wcsuserdata",choice,"gravity"))
	if gravity and gravity > 0:
		gravity = int(round(gravity * 100))
		if gravity != 100 and gravity != 0: wum_playerinfo.addline("- gravity: %s%%"%gravity)
	longjump = 0
	if es.keygetvalue("wcsuserdata",choice,"longjump"): longjump = float(es.keygetvalue("wcsuserdata",choice,"longjump"))
	if longjump and longjump > 0:
		longjump = int(round(longjump * 100))
		if longjump != 100 and longjump != 0: wum_playerinfo.addline("- longjump: %s%%"%longjump)
	invisp = 0
	if es.keygetvalue("wcsuserdata",choice,"invisp"): invisp = float(es.keygetvalue("wcsuserdata",choice,"invisp"))
	if invisp and invisp > 0:
		invisp = int(round(invisp))
		if invisp != 0: wum_playerinfo.addline("- invis: %s%%"%invisp)
	if es.getplayerprop(choice,"CCSPlayer.baseclass.pl.deadflag") == 0:
		wum_playerinfo.addline("- health %s%%"%es.getplayerprop(choice,"CCSPlayer.baseclass.m_iHealth"))
	wum_playerinfo.addline("-----------------------")
	wum_playerinfo.addline("->8. Back")
	wum_playerinfo.addline("->0. Exit")
	for popup in popups:
		if popuplib.exists("%s%s"%(popup,userid)): popuplib.close("%s%s"%(popup,userid),userid)
	gamethread.delayed(0.0001,wum_playerinfo.send,(userid))
	
def wum_playerinfo_handler(userid,choice,popupid):
	if choice == 8: 
		checkPop(popupid)
		es.delayed(0.0001, "es wcs_usersmenu %s"%userid)
	elif choice == 10: 
		checkPop(popupid)
		
def genPlayerlistPop(popupname, callback):
	checkPop(popupname)
	p = popuplib.easymenu(popupname, None, callback)
	p.settitle('Select Player')
	for i in es.getUseridList():
		p.addoption(i, es.getplayername(i))
	return p
	
def checkPop(p):
    if popuplib.exists(p): popuplib.delete(p)
	
def playerSelect(userid, choice, popupname):
    checkPop(popupname)
    if es.exists('userid', choice):
        gamethread.delayed(0.0001,wum_handler,(userid, choice, popupname))