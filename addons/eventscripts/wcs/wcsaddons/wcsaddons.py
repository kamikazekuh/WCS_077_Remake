## ************************
## **Warcraft:OrangeBox****
## **wcsaddons*wcs*Module**
## **By*Shidobu************
## ************************
import es,cmdlib,os

def load():
	global path
	path = es.getAddonPath("wcs/wcsaddons")
	cmdlib.registerServerCommand("wcsaddons_load",wcsaddons_load,"Lets you load a wcs addon.")
	cmdlib.registerServerCommand("wcsaddons_unload",wcsaddons_unload,"Lets you unload a wcs addon.")

def unload():
	cmdlib.unregisterServerCommand("wcsaddons_load")
	cmdlib.unregisterServerCommand("wcsaddons_unload")

def wcsaddons_load(args):
	if len(args) == 1:
		epath = path + "/addons/%s"%args[0]
		if os.path.isdir(epath):
			ppath = epath + "/%s.py"%args[0]
			epath = epath + "/es_%s.txt"%args[0]
			if os.path.isfile(epath) or os.path.isfile(ppath):
				epath = "wcs/wcsaddons/addons/%s"%args[0]
				es.load(epath)
			else:
				es.dbgmsg(0,"Error could not load wcsaddon %s, file was not found."%args[0])
		else:
			es.dbgmsg(0,"Error could not load wcsaddon %s, directory %s was not found."%(args[0],epath))
	else:
		es.dbgmsg(0,"Error you have too many or too less arguments. Syntax - wcsaddons_load <addon>")

def wcsaddons_unload(args):
	if len(args) == 1:
		epath = path + "/addons/%s"%args[0]
		if os.path.isdir(epath):
			ppath = epath + "/%s.py"%args[0]
			epath = epath + "/es_%s.txt"%args[0]
			if os.path.isfile(epath) or os.path.isfile(ppath):
				epath = "wcs/wcsaddons/addons/%s"%args[0]
				es.unload(epath)
			else:
				es.dbgmsg(0,"Error could not unload wcsaddon %s, file was not found."%args[0])
		else:
			es.dbgmsg(0,"Error could not unload wcsaddon %s, directory %s was not found."%(args[0],epath))
	else:
		es.dbgmsg(0,"Error you have too many or too less arguments. Syntax - wcsaddons_load <addon>")