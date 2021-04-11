import json
import traceback

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Laser_LargeLaser_Bombast.json"

with open(local_file) as f:
    data = json.load(f)

try:
    max_mode_dam = 0 #set mode index of mode highest dam weapon
    max_dam_mode = 0 #set value of highest additional damage in modes
    for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
        try:
            if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                max_mode_dam = data['Modes'][i]['DamagePerShot']
                max_dam_mode = i
        except KeyError: #if no Modes found
            print('skipped')
            continue #this skips modes that have no damage
    print('Max Dam Mode ', max_dam_mode,'Max Mode Dam ', max_mode_dam)
    #this block is working and provides the max damage mode and the max number
        
    #weapon_damage = str(data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])) #damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
    #print('Dam ' + weapon_damage)
except (KeyError) as e: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
    pass
    #try:
       # weapon_damage = str(data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])) #damage = damage per shot * projectilespershot
     #   print('No damage in modes, defaulting to base', 'Dam ' + weapon_damage)
    #except KeyError:
     #   print('No damage on this weapon!?')