import es
 
def load():
    es.loadevents('declare', 'addons/eventscripts/wcs/wcsevents/wcsevents.res')
    es.loadevents('addons/eventscripts/wcs/wcsevents/wcsevents.res')
 
def es_map_start(event_var):
    es.loadevents('addons/eventscripts/wcs/wcsevents/wcsevents')