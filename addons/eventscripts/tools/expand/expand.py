# ../addons/eventscripts/wcs/core/expand/__init__.py

# ==============================================================================
# >> IMPORTS
# ==============================================================================
import es
import gamethread
import playerlib
import spe
import vecmath


# ==============================================================================
# >> GLOBAL VARIABLES
# ==============================================================================
# Store the teams by their indexes...
g_TeamIndexes = {
    '1': 1, 'spec': 1, '2': 2, 't': 2, '3': 3, 'ct': 3
}

# Get the module instance...
g_SelfModule = __import__(__name__)


# ==============================================================================
# >> PRIVATE FUNCTIONS
# ==============================================================================
def _get_matching_players(users):
    '''Return a set() of players matching the given filter...'''
    
    # Get a set to store the matching players...
    return_value = set()
    
    # Is the player a single userid?
    if es.exists('userid', users):
        
        # Add that player...
        return_value.add(int(users))
        
    # Otherwise, is that a playerlib's filter?
    elif str(users).startswith('#'):
        
        # Loop through all matching players...
        for userid in playerlib.getUseridList(users):
            
            # Add the player...
            return_value.add(userid)
            
    # Otherwise...
    else:
        
        # Try to find a userid...
        userid = es.getuserid(users)
        
        # Any match found?
        if userid:
            
            # Add the player...
            return_value.add(userid)
            
    # Finaly, return the matching players...
    return return_value
    
    
def _remove_entity(index):
    '''Remove the given entity index...'''
    
    # Get the entity pointer...
    pEntity = spe.getEntityOfIndex(index)
    
    # Is the entity not valid?
    if not pEntity:
        
        # Don't go further...
        return
        
    # Remove the entity...
    spe.call('Remove', pEntity)
    
    
def _reset_player_fov(userid):
    '''Reset the given player's field of view...'''
    
    # Is the given userid not valid?
    if not es.exists('userid', userid):
        
        # Don't go further...
        return
        
    # Reset the player fov...
    es.setplayerprop(userid, 'CBasePlayer.m_iDefaultFOV', 90)
    es.setplayerprop(userid, 'CBasePlayer.m_iFOV', 90)
    
    
# ==============================================================================
# >> FUNCTIONS
# ==============================================================================
def spawn(users, force_respawn=False):
    '''Respawn a player...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Get the player's dead state...
        isdead = es.getplayerprop(userid, 'CBasePlayer.pl.deadflag')
        
        # Does we need to respawn the player?
        if force_respawn or isdead:
            
            # Respawn the player...
            spe.call('Respawn', spe.getPlayer(userid))
            
            
def strip(users):
    '''Remove all weapons owned by a player...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Loop through all weapon slots...
        for x in range(0, 65):
            
            # Get the weapon index...
            index = es.getindexfromhandle(es.getplayerprop(
                userid, 'CBaseCombatCharacter.m_hMyWeapons.%03d' % x))
                
            # Is the weapon not valid?
            if not index:
                
                # Don't go further...
                continue
                
            # Remove the weapon entity...
            spe.call('Remove', spe.getEntityOfIndex(index))
            
        # Remove the player's viewmodel...
        es.setplayerprop(
            userid, 'CBasePlayer.localdata.m_Local.m_bDrawViewmodel', 0)
            
            
def drop(users, weapon):
    '''Force a player to drop his weapon...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Is the given weapon an integer?
        if str(weapon).isdigit():
            
            # Get the weapon by its slots...
            pWeapon = spe.call(
                'GetWeapon', spe.getPlayer(userid), int(weapon))
                
        # Otherwise...
        else:
            
            # Is the weapon not starting by 'weapon_'?
            if not str(weapon).lower().startswith('weapon_'):
                
                # Add the 'weapon_' prefix...
                weapon = 'weapon_' + weapon
                
            # Get the weapon by its name...
            pWeapon = spe.call(
                'OwnsWeapon', spe.getPlayer(userid), weapon, 0)
                
        # Is the weapon found not valid?
        if not pWeapon:
            
            # Don't go further...
            continue
            
        # Make the player drop his weapon...
        spe.call('DropWeapon', spe.getPlayer(userid), pWeapon, 0, 1)
        
        
def push(users, *axes):
    '''Push a player in the given direction...'''
    
    # Get the given Vector...
    vector = vecmath.Vector(*axes)
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Push the player...
        es.setplayerprop(userid, 'CBasePlayer.localdata.m_vecBaseVelocity',
            es.createvectorstring(*vector))
            
            
def pushto(users, location, force):
    '''Push a player to the given location...'''
    
    # Get the given Vector...
    vector = vecmath.Vector(location)
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Get the vector from the player location...
        vector -= vecmath.Vector(es.getplayerlocation(userid))
        
        # Multiply the force...
        vector *= float(force)
        
        # Push the player...
        es.setplayerprop(userid, 'CBasePlayer.localdata.m_vecBaseVelocity',
            es.createvectorstring(*vector))
            
            
def damage(users, _damage, attacker=None, armor=False, weapon=None):
    '''Damage a player...'''
    
    # Is there no player on the server?
    if not es.getplayercount():
        
        # Don't go further...
        return
        
    # Create a 'point_hurt' entity...
    index = es.createentity('point_hurt')
    
    # Set the entity name...
    es.setentityname(index, index)
    
    # Does we need to apply damage on the player's armor?
    if armor:
        
        # Set the damage type to fall...
        es.entitysetvalue(index, 'damagetype', 32)
        
    # Is any weapon specified?
    if weapon:
        
        # Set the classname to the given weapon...
        es.entitysetvalue(index, 'classname', weapon)
        
    # Set the given damage...
    es.entitysetvalue(index, 'damage', _damage)
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Is the given damage need to be the player health?
        if _damage == '#health':
            
            # Set the damage to the player health...
            es.entitysetvalue(index, 'damage',
                es.getplayerprop(userid, 'CBasePlayer.m_iHealth'))
                
        # Get the player index...
        player_index = es.getindexfromhandle(es.getplayerhandle(userid))
        
        # Store the actual player name...
        targetname = es.entitygetvalue(index, 'targetname')
        
        # Set the player name to his index...
        es.setentityname(player_index, player_index)
        
        # Set the damage target...
        es.entitysetvalue(index, 'damagetarget', player_index)
        
        # Is there's no attacker?
        if not attacker:
            
            # Damage the player...
            es.fire(userid, index, 'Hurt')
            
        # Otherwise...
        else:
            
            # Damage the player...
            es.fire(attacker, index, 'Hurt')
            
        # Set back the player name...
        es.fire(userid, player_index, 'AddOutput', 'targetname %s' % targetname)
        
    # Remove the entity later...
    gamethread.delayedname(0.5, '_wcs_delay', _remove_entity, index)
	
def gravity(userid, value):
	es.server.queuecmd("es wcs_setgravity %s %s" % (userid, value))   
	
def _player_spawn(ev):
	userid = int(ev['userid'])
	es.cexec(userid, 'r_screenoverlay off')
	es.setplayerprop(userid, 'CBasePlayer.m_iDefaultFOV', 90)
	es.setplayerprop(userid, 'CBasePlayer.m_iFOV', 90)

def gravity2(users, value):
    '''Set a player gravity...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Set the player gravity...
        es.entitysetvalue(
            es.getindexfromhandle(es.getplayerhandle(userid)), 'gravity', value)
            
            
def removeWeapon(users, weapon):
    '''Remove a player weapon...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Is the given weapon an integer?
        if str(weapon).isdigit():
            
            # Get the weapon by its slot...
            pWeapon = spe.call(
                'GetWeapon', spe.getPlayer(userid), int(weapon))
                
        # Otherwise...
        else:
            
            # Is the weapon not starting by 'weapon_'?
            if not str(weapon).lower().startswith('weapon_'):
                
                # Add the 'weapon_' prefix...
                weapon = 'weapon_' + weapon
                
            # Get the weapon by its name...
            pWeapon = spe.call(
                'OwnsWeapon', spe.getPlayer(userid), str(weapon), 0)
                
        # Is the weapon not valid?
        if not pWeapon:
            
            # Don't go further...
            continue
            
        # Remove the weapon...
        spe.call('Remove', pWeapon)
        
        
def getViewEntity(userid):
    '''Get the entity a player is looking at...'''
    
    # Is the player not valid?
    if not es.exists('userid', userid):
        
        # Don't go further...
        return None
        
    # Get the entity pointer...
    pEntity = spe.call('FindPickerEntity', spe.getPlayer(int(userid)))
    
    # Is the entity not valid?
    if not pEntity:
        
        # Don't go further...
        return None
        
    # Return the entity index...
    return spe.getEntityIndex(pEntity)
    
    
def getViewPlayer(userid):
    '''Get the player a player is looking at...'''
    
    # Get the index of the entity the player is looking at...
    index = getViewEntity(userid)
    
    # Is the index not valid?
    if not index or es.entitygetvalue(index, 'classname') != 'player':
        
        # Don't go further...
        return None
        
    # Return the player userid...
    return es.getuserid(es.gethandlefromindex(index))
    
    
def keyHint(users, message):
    '''Send a KeyHintText message to the given player...'''
    
    # Create the UserMessage...
    es.usermsg('create', 'keyhint', 'KeyHintText')
    
    # Write the message to it...
    es.usermsg('write', 'byte', 'keyhint', 1)
    es.usermsg('write', 'string', 'keyhint', message)
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player a bot?
        if es.isbot(userid):
            
            # Don't go further...
            continue
            
        # Send the message...
        es.usermsg('send', 'keyhint', userid)
        
    # Finaly, delete the message from memory...
    es.usermsg('delete', 'keyhint')
    
    
def give(users, entity):
    '''Give a entity to a player...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Give the entity...
        spe.call('GiveNamedItem', spe.getPlayer(userid), entity, -0)
        
        
def fire(users, lifetime=999):
    '''Ignite a player for the given time...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player dead?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # Don't go further...
            continue
            
        # Ignite the player...
        es.fire(userid, '!self', 'IgniteLifeTime', lifetime)
        
        
def extinguish(users):
    '''Extinguish a burning player...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Extinguish the player...
        es.fire(userid, '!self', 'IgniteLifeTime', 0)
        
        
def drug(users, lifetime=0):
    '''Drug a player for the given time...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player a bot?
        if es.isbot(userid):
            
            # Don't go further...
            continue
            
        # Drug the player...
        es.cexec(userid, 'r_screenoverlay effects/tp_eyefx/tp_eyefx')
        
        # Is there any time given?
        if not lifetime:
            
            # Don't go further...
            continue
            
        # Undrug the player after the given time...
        gamethread.delayedname(
            lifetime, '_wcs_delay', es.cexec, (userid, 'r_screenoverlay off'))
            
            
def drunk(users, lifetime=0, iFov=155):
    '''Drunk a player for the given time...'''
    
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Is the player a bot?
        if es.isbot(userid):
            
            # Don't go further...
            continue
            
        # Set the fov to the given value...
        es.setplayerprop(userid, 'CBasePlayer.m_iDefaultFOV', iFov)
        es.setplayerprop(userid, 'CBasePlayer.m_iFOV', iFov)
        
        # Is there any time given?
        if not lifetime:
            
            # Don't go further...
            continue
            
        # Undrunk the player after the given time...
        gamethread.delayedname(
            lifetime, '_wcs_delay', _reset_player_fov, userid)
            
            
def dealPoison(users, attacker, _damage, lifetime):
    '''Poison a player for the given time...'''
    
    # Damage the given players...
    damage(users, _damage, attacker)
    
    # Is the lifetime not valid?
    if not lifetime >= 1:
        
        # Don't go further...
        return
        
    # Remove 1 second...
    lifetime -= 1
    
    # Repeat the function...
    gamethread.delayedname(1, '_wcs_delay',
        dealPoison, (users, attacker, _damage, lifetime))
        
        
def changeTeam(users, teamid):
    '''Switch a player to the given team...'''
    
    # Format the given team...
    teamid = str(teamid).lower()
    
    # Is the team not valid?
    if not g_TeamIndexes.has_key(teamid):
        
        # Don't go further...
        return
        
    # Loop through all matching players...
    for userid in _get_matching_players(users):
        
        # Switch the player...
        spe.call('ChangeTeam', spe.getPlayer(userid), g_TeamIndexes[teamid])
        
        
# ==============================================================================
# >> GAME EVENTS
# ==============================================================================
def round_end(event_var):
    '''Fired every time a round is ending...'''
    
    # Loop through all players...
    for userid in es.getUseridList():
        
        # Is the player death?
        if es.getplayerprop(userid, 'CBasePlayer.pl.deadflag'):
            
            # No need to go further...
            continue
            
        # Undrug the player...
        es.cexec(userid, 'r_screenoverlay off')
        
    # Cancel the delays...
    gamethread.cancelDelayed('_wcs_delay')
    
# Register the round_end event...
es.addons.registerForEvent(g_SelfModule, 'round_end', round_end)


def player_death(event_var):
    '''Fired every time a player is dying...'''
    
    # Undrug the player...
    es.cexec(event_var['userid'], 'r_screenoverlay off')
    
# Register the player_death event...
es.addons.registerForEvent(g_SelfModule, 'player_death', player_death)