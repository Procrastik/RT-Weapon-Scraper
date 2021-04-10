import json
import traceback

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Laser_LargeLaser_Bombast.json"

with open(local_file) as f:
    data = json.load(f)

try:
    max_mode_dam = 0
    max_dam_mode = 0
    for i in range(len(data['Modes'])):
        try:
            if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                max_mode_dam = data['Modes'][i]['DamagePerShot']
                max_dam_mode = i
        except KeyError:
            continue #this skips modes that have no damage
    print('Max Dam Mode ', max_dam_mode,'Max Mode Dam ', max_mode_dam)
        
    #weapon_damage = str(data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])) #damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
    #print('Dam ' + weapon_damage)
except (KeyError, IndexError) as e:
    pass
    #try:
       # weapon_damage = str(data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])) #damage = damage per shot * projectilespershot
     #   print('No damage in modes, defaulting to base', 'Dam ' + weapon_damage)
    #except KeyError:
     #   print('No damage on this weapon!?')