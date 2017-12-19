import es
import gamethread
import playerlib
import usermsg
import tools.expand.expand
import tools.wcsgroup.wcsgroup


def wcs_ulti_roots():
	userid = int(es.ServerVar('wcs_userid'))
	count = 0

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 1, 1, 10, 55, 5, 200)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))
			time = float(es.ServerVar('wcs_freezetime'))

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not tools.wcsgroup.wcsgroup.getUser(user, 'ulti_immunity'):
						playerlib.getPlayer(user).freeze = 1
						gamethread.delayed(time, reset, (user, 'freeze', 0))
						count += 1

					else:
						es.tell(user, '#multi', '#lightgreenYour ultimate was blocked, the enemy is #greenimmune.')
						es.tell(userid, '#multi', '#lightgreenYou #greenblocked #lightgreenan ultimate skill.')

	if count:
		es.centertell('Entangling Roots: %s' % (count))
	else:
		es.tell(userid, '#multi','#lightgreenEntangling Roots #greenfailed#lightgreen, because no enemy is close enough.')
		es.server.queuecmd('es wcs_reset_cooldown %s' % (userid))
		
def wcs_ulti_chain():
	userid = int(es.ServerVar('wcs_userid'))
	count = 0

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 2, 1, 240, 240, 240, 100)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))
			es.ServerVar('vector1').set(','.join(map(str, (x,y,z))))

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not tools.wcsgroup.wcsgroup.getUser(user, 'ulti_immunity'):
						tools.expand.expand.damage(user, 32, userid)
						count += 1

						if es.ServerVar('wcs_cfg_graphicfx'):
							es.server.insertcmd('es_xset vector2 '+','.join(map(str, (x1,y1,z1)))+';es_xdoblock wcs/addons/effect/ChainLightning')

					else:
						es.tell(user, '#multi', '#lightgreenYour ultimate was blocked, the enemy is #greenimmune.')
						es.tell(userid, '#multi', '#lightgreenYou #greenblocked #lightgreenan ultimate skill.')

	if count:
		es.centertell('Chain Lightning: %s players damaged' % (count))
	else:
		es.tell(userid, '#multi', '#lightgreenChain Lightning #greenfailed#lightgreen, because no enemy is close enough to be damaged.')
		es.server.queuecmd('es wcs_reset_cooldown %s' % (userid))

def wcs_ulti_suicide():
	userid = int(es.ServerVar('wcs_userid'))

	if es.getplayerteam(userid) >= 2:
		if playerlib.getUseridList('#alive'):
			usermsg.fade(userid, 0, 2, 1, 240, 240, 240, 100)
			x,y,z = es.getplayerlocation(userid)
			radius = float(es.ServerVar('wcs_radius'))
			magnitude = float(es.ServerVar('wcs_magnitude'))
			v = round(radius * magnitude) / 150

			for user in playerlib.getUseridList('#alive,#'+['ct','t'][es.getplayerteam(userid)-2]):
				x1,y1,z1 = es.getplayerlocation(user)

				if ((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) ** 0.5 <= radius:
					#check for wall between...

					if not tools.wcsgroup.wcsgroup.getUser(user, 'ulti_immunity'):
						tools.expand.expand.damage(user, v, userid)

					else:
						es.tell(user, '#multi', '#lightgreenYour ultimate was blocked, the enemy is #greenimmune.')
						es.tell(userid, '#multi', '#lightgreenYou #greenblocked #lightgreenan ultimate skill.')




def reset(userid, what, default):
	if es.exists('userid', userid):
		setattr(playerlib.getPlayer(userid), what, default)
