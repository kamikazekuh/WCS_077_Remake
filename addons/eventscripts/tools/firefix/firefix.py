from es import server

joined = []

def player_spawn(ev):
    u = ev['userid']
    if u in joined:
        return
    server.mp_disable_autokick(u)
    joined.append(u)

def player_disconnect(ev):
    u = ev['userid']
    if not u in joined:
        return
    joined.remove(u)

def es_map_start(ev):
    global joined
    joined = []
