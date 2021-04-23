import json
import traceback

local_file = "E:\Roguetech\RogueTech\RISCtech\Items\Weapon\Weapon_PALASMA_RISC.json"

with open(local_file) as f:
    data = json.load(f)

##weapon heat damage module
max_dam_mode = 12
try:
    weapon_heat_damage = (data['HeatDamage'] + data['Modes'][max_dam_mode]['HeatDamagePerShot']) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
    print('Heat dam ' + str(weapon_heat_damage))
   
except KeyError:
    print('Either no HeatDamagePerShot in modes, no ShotsWhenFired in modes, or no modes, checking other possibilities in modes')
    try:
        weapon_heat_damage = (data['HeatDamage'] + data['Modes'][max_dam_mode]['HeatDamagePerShot']) * data['ProjectilesPerShot'] * data['ShotsWhenFired']
        print('Heat dam ' + str(weapon_heat_damage))           
    except KeyError:
        print('Either no HeatDamagePerShot in modes or no modes, checking other possibilities')                
        try:
            weapon_heat_damage = data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired']) #heat damage = heat damage per shot * projectilespershot
            print('Heat dam' + str(weapon_heat_damage))
        except KeyError:
            print('No heat damage key on this weapon!?')