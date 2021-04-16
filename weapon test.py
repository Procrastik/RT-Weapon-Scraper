import json
import traceback

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Gauss_RAILGUN.json"

with open(local_file) as f:
    data = json.load(f)


#weapon damage falloff module, this will need to be after ranges are set!
weapon_dam_falloff_min = 0
weapon_dam_falloff_short = 0
weapon_dam_falloff_medium = 0
weapon_dam_falloff_long = 0
weapon_dam_falloff_max = 0
try:
    distance_variance = data['DistantVariance']
    if distance_variance > 0:
        if data['DistantVarianceReversed'] == False:
            try:
                weapon_dam_falloff_start = data['DamageFalloffStartDistance']
            except KeyError:
                weapon_dam_falloff_start = weapon_range_medium
            try:
                weapon_dam_falloff_end = data['DamageFalloffEndDistance']
            except KeyError:
                weapon_dam_falloff_end = weapon_range_max
            if weapon_range_min >= weapon_dam_falloff_start:
                print('this should not happen?')
            elif weapon_range_short > weapon_dam_falloff_start:
                distance_ratio = (weapon_range_short - weapon_dam_falloff_start) / (weapon_dam_falloff_end - weapon_dam_falloff_start)
               weapon_dam_falloff_short = (1.0 - (distance_ratio * distance_ratio)) * 

            #standard tree
        elif data['DistantVarianceReversed'] == True:
            #reversed tree


        print('do something')

except KeyError:
    print('No dam falloff, defaulting to zero.')
    

