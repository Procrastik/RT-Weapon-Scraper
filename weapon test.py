import json
import traceback
import re

local_file = "E:\Roguetech\RogueTech\PirateTech\Items\Weapons\Weapon_Autocannon_AC20_JuryRigged.json"

with open(local_file) as f:
    data = json.load(f)
weapon_recoil = 6
 ##Weapon jamming chance module
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
        try:
            pattern = '^wr-jam_chance_multiplier-[0-9]+'
            for i in data['ComponentTags']['items']:
                print(i)
                try:
                    multiplier = int(re.match(pattern, i).group()[-1])
                    weapon_flat_jam = weapon_recoil * multiplier
                except AttributeError:
                    continue
        except (KeyError, IndexError, TypeError) as e:
            traceback.print_exc()
            print('No flat jamming chance on this weapon.')
            weapon_flat_jam = 0
if weapon_flat_jam > 100:
    weapon_flat_jam = 100
print(weapon_flat_jam)
