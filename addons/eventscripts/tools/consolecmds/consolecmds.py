import es

def load():

	#wcsusers
	es.regclientcmd('spendskills', 'wcs/wcsusers/wcs_spendskills', '')
	es.regclientcmd('playerinfo', 'wcs/wcsusers/wcs_playerinfo', '')
	es.regclientcmd('resetskills', 'wcs/wcsusers/wcs_resetskills', '')
	es.regclientcmd('showskills', 'wcs/wcsusers/wcs_showskills', '')
	es.regclientcmd('showcredits', 'wcs/wcsusers/wcs_showcredits', '')

	#wcstop
	es.regclientcmd('wcstop', 'wcs/wcstop10/wcs_showtop10', '')
	es.regclientcmd('showtop10', 'wcs/wcstop10/wcs_showtop10', '')

	#wcsshop
	es.regclientcmd('shopmenu', 'wcs/wcsshop/wcs_shopmenu', '')
	es.regclientcmd('shopinfo', 'wcs/wcsshop/wcs_showshopinfo', '')

	#wcsraces
	es.regclientcmd('changerace', 'wcs/wcsraces/wcs_changerace', '')
	es.regclientcmd('raceinfo', 'wcs/wcsraces/sraceinfo', '')

	#wcsfunctions
	es.regclientcmd('wcshelp', 'wcs/wcsfunctions/wcs_help', '')
	es.regclientcmd('warcraft', 'wcs/wcsfunctions/wcs_help', '')
	es.regclientcmd('feedback', 'wcs/wcsfunctions/wcs_feedback', '')
	es.regclientcmd('wcsmenu', 'wcs/wcsfunctions/wcs_wcsmenu', '')
	es.regclientcmd('wcs', 'wcs/wcsfunctions/wcs_wcsmenu', '')

	#wcsxp
	es.regclientcmd('showxp', 'wcs/wcsfunctions/wcsxp/wcs_showxp', '')
	

def unload():
	es.unregclientcmd('spendskills')
	es.unregclientcmd('playerinfo')
	es.unregclientcmd('resetskills')
	es.unregclientcmd('showskills')
	es.unregclientcmd('showcredits')
	es.unregclientcmd('wcstop')
	es.unregclientcmd('showtop10')
	es.unregclientcmd('shopmenu')
	es.unregclientcmd('shopinfo')
	es.unregclientcmd('changerace')
	es.unregclientcmd('raceinfo')
	es.unregclientcmd('wcshelp')
	es.unregclientcmd('warcraft')
	es.unregclientcmd('feedback')
	es.unregclientcmd('wcsmenu')
	es.unregclientcmd('wcs')
	es.unregclientcmd('showxp')