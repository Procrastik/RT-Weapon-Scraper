import json
import traceback

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Rotary_Autocannon_2.json"

with open(local_file) as f:
    data = json.load(f)

    try:
        weapon_flat_jam = data['FlatJammingChance'] #FlatJammingChance is handled backwards to ShotsWhenFired. Most mode weapons don't have a base FlatJammingChance key and ONLY have them in the modes. Check for base FIRST then check for modes based on that.
        try:
            weapon_flat_jam = (data['FlatJammingChance'] + data['Modes'][-1]['FlatJammingChance'] * 100)  
            print('Flat jamming chance ' + str(weapon_flat_jam))
        except (KeyError, IndexError) as e:
            weapon_flat_jam = (data['FlatJammingChance'] * 100)
            print('No modes, reverting to base jam chance ' + str(weapon_flat_jam) + '%')
    except KeyError:
        try:
            weapon_flat_jam = (data['Modes'][-1]['FlatJammingChance'] * 100)
            print('No base flat jamming chance key, using modes ' + str(weapon_flat_jam) + '%')
        except (KeyError, IndexError) as e:
            print('No flat jamming chance on this weapon.')
            weapon_flat_jam = 0
    if weapon_flat_jam > 100:
        weapon_flat_jam = 100
    print(weapon_flat_jam)