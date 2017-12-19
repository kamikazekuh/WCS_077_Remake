import es
from cmdlib import registerServerCommand, unregisterServerCommand

def load():
	registerServerCommand('wcs_forcerace', force_race, 'wcs_forcerace <userid> <racenumber>')
	
def unload():
	unregisterServerCommand('wcs_forcerace')

def force_race(args):
	userid = str(args[0])
	race = str(args[1])
	if es.getplayerprop(userid,"CCSPlayer.baseclass.pl.deadflag") == 0:
		es.server.queuecmd("es wcs_dealdamage %s %s 9999" % (userid, userid))
	steamid = es.getplayersteamid(userid)
	if steamid == 'BOT':
		name = es.getplayername(userid)
		steamid = 'BOT_%s' % name.upper()
	es.server.queuecmd("es wcs_saveplayer %s"%userid)
	player_race = es.keygetvalue("wcsuserdata", userid, "race")
	command_buffer = es.keygetvalue("wcsraces", player_race, "onchange")
	es.server.queuecmd("es_xset wcs_userid %s" % userid)
	es.server.queuecmd(command_buffer)
	es.server.queuecmd("es_keysetvalue \"wcsuserdata\" %s \"race\" %s"%(userid, race))
	es.server.queuecmd("es wcs_keysetvalue  \"%s\" \"race\" %s"%(steamid, race))
	es.server.queuecmd("es_xset wcs_id \"%s\""% steamid)
	es.server.queuecmd("es_xdoblock wcs/wcsfunctions/wcs_playercheck")
	es.server.queuecmd("es wcs_getplayer %s"%userid)
	es.server.queuecmd("es_keysetvalue \"wcsuserdata\" %s \"skillcheck\" \"1\""%userid)
	es.tell(userid, "#multi", "#lightgreenYou changed your race to#green " + es.keygetvalue("wcsraces", race, "name"))
	old_name = es.keygetvalue("wcsraces", player_race, "name")
	new_name = es.keygetvalue("wcsraces", race, "name")
	es.event('initialize', "wcs_changerace")
	es.event('setint', "wcs_changerace", "userid", int(userid))
	es.event('setstring', "wcs_changerace", "oldrace", str(old_name))
	es.event('setstring', "wcs_changerace", "newrace", str(new_name))
	es.event('fire', "wcs_changerace")