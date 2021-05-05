import json
import traceback
import re

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Rotary_Autocannon_2.json"

with open(local_file) as f:
    data = json.load(f)

#weapon base mode module
try:
    weapon_base_damage = 0
    for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
        print('Base mode check', i)
        try:
            if data['Modes'][i]['isBaseMode']:
                weapon_base_damage = (data['Damage'] + data['Modes'][i]['DamagePerShot']) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired'])
                #would like to use break here but it doesn't exit the for loop??
        except KeyError: #if no DamagePerShot in mode found
            print('No DamagePerShot in modes, checking for extra shots in mode')
            try:
                weapon_base_damage = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired'])
            except KeyError: #if no ShotsWhenFired in mode found
                print('Weapon has no extra shots in modes, using base values')
                weapon_base_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])
except KeyError: #This will catch errors when a weapon has no modes.
    print('No modes, reverting to base values')
    weapon_base_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot
print("Base weapon damage ", weapon_base_damage)
