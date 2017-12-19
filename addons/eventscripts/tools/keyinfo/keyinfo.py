import es
import gamethread
import tools.expand.expand
import playerlib
import tools.wcsgroup.wcsgroup


def player_spawn(ev):
	player_death({'userid':ev['userid']})
	gamethread.delayedname(1, 'wcs_showinfo'+ev['userid'], showHint, ev['userid'])

def player_death(ev):
	gamethread.cancelDelayed('wcs_showinfo'+ev['userid'])

def player_disconnect(ev):
	player_death({'userid':ev['userid']})

def showHint(userid):
	key = es.getplayersteamid(userid)
	if not key == 'BOT':
		speed = playerlib.getPlayer(userid).getSpeed()
		color = playerlib.getPlayer(userid).getColor()
		index = float(es.getindexfromhandle(es.getplayerhandle(userid)))
		gravity = float(es.entitygetvalue(index, "gravity"))
		a,b,c,d = color
		playername = es.getplayername(userid)
		racenumber = tools.wcsgroup.wcsgroup.getUser(userid, "race")
		race = es.keygetvalue('wcsraces', racenumber, 'name')
		totallevel = tools.wcsgroup.wcsgroup.getUseruserid, "total_level")
		level = tools.wcsgroup.wcsgroup.getUseruserid, "level")
		xp = tools.wcsgroup.wcsgroup.getUseruserid, "xp")
		needed = (int(level)+1)*int(es.ServerVar("wcs_levelxp"))
		#rank = wcs.database.getRank(es.getplayersteamid(userid))
		text = str(playername)+'\n=============\nRace: '+str(race)+'\nTotallevel: ['+str(totallevel)+']\nLevel: ['+str(level)+']\nXp: ['+str(xp)+'/'+str(needed)+']\n=============\nSpeed: '+str(round(speed*100))+'%'
		tools.expand.expand.keyHint(userid, text)

		player_spawn({'userid':userid})