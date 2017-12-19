import es

def load():
	es.dbgmsg(0, "--- WCS Tools loading ---")
	es.load('tools/cmds')
	es.load('tools/commands')
	es.load('tools/console')
	es.load('tools/effect')
	es.load('tools/effects')
	es.load('tools/expand')
	es.load('tools/firefix')
	es.load('tools/getcolor')
	es.load('tools/longjump')
	es.load('tools/nearcoord')
	es.load('tools/pending')
	es.load('tools/randplayer')
	es.load('tools/ultimates')
	es.load('tools/ultimatespy')
	es.load('tools/wcsgroup')
	es.load('tools/wcsgroup_es')
	es.load('tools/xcommands')
	es.load('tools/setfx')
	es.load('tools/myraces')
	es.dbgmsg(0, "--- WCS Tools loaded ---")
	
	
def unload():
	es.dbgmsg(0, "--- WCS Tools unloading ---")
	es.unload('tools/cmds')
	es.unload('tools/commands')
	es.unload('tools/console')
	es.unload('tools/effect')
	es.unload('tools/effects')
	es.unload('tools/expand')
	es.unload('tools/firefix')
	es.unload('tools/getcolor')
	es.unload('tools/longjump')
	es.unload('tools/nearcoord')
	es.unload('tools/pending')
	es.unload('tools/randplayer')
	es.unload('tools/ultimates')
	es.unload('tools/ultimatespy')
	es.unload('tools/wcsgroup')
	es.unload('tools/wcsgroup_es')
	es.unload('tools/xcommands')
	es.unload('tools/setfx')
	es.unload('tools/myraces')
	es.dbgmsg(0, "--- WCS Tools unloaded ---")