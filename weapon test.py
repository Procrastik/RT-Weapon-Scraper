import json
import traceback

local_file = "E:\RT Analyzation\RT-Analyzation\Weapon_Gauss_RAILGUN.json"

with open(local_file) as f:
    data = json.load(f)


#weapon damage falloff module, this will need to be after ranges are set!

#weapon_dam_falloff_min = 0
#weapon_dam_falloff_short = 0
#weapon_dam_falloff_medium = 0
#weapon_dam_falloff_long = 0
#weapon_dam_falloff_max = 0
#data['DistantVariance']
#data['isDamageVariation'] boolean
#data['isHeatVariation'] boolean
#data['isStabilityVariation'] boolean
#data['RangedDmgFalloffType']
#data['DamageFalloffStartDistance']
#data['DamageFalloffEndDistance']

try:
    weapon_range_min = data['MinRange']
except KeyError:
    traceback.print_exc()

try:
    weapon_range_short = data['RangeSplit'][0]
except KeyError:
    traceback.print_exc()

try:
    weapon_range_medium = data['RangeSplit'][1]
except KeyError:
    traceback.print_exc()

try:
    weapon_range_long = data['RangeSplit'][2]
except KeyError:
    traceback.print_exc()

try:
    weapon_range_max = data['MaxRange']
except KeyError:
    traceback.print_exc()

range_list = [weapon_range_min, weapon_range_short, weapon_range_medium, weapon_range_long, weapon_range_max]
range_falloff_ratio_list = [0,0,0,0,0] #this is not being populated
range_falloff_total_damage = [0,0,0,0,0] #this is not bein populated zip related due to tuples


if data['isDamageVariation']: #verify weapon uses damage variance
    try:
        if data['DistantVarianceReversed'] == False:
            if data['DistantVariance'] > 0:
                ##INPUT PROTECTION
                try:
                    if data['DamageFalloffStartDistance'] > 1/1000:
                        falloff_start = data['DamageFalloffStartDistance']
                    elif data['DamageFalloffStartDistance'] < 1/1000:
                        print('Falloff start value is zero, using medium value')
                        falloff_start = weapon_range_medium
                except KeyError:
                    print('No falloff start distance key, using medium value')
                    falloff_start = weapon_range_medium
                try:
                    if data['DamageFalloffEndDistance'] < falloff_start:
                        falloff_end = weapon_range_max
                    elif data['DamageFalloffEndDistance'] > falloff_start:
                        falloff_end = data['DamageFalloffEndDistance']
                except KeyError:
                    print('No falloff end distance, using max value')
                    falloff_end = weapon_range_max
            ##GET RATIO
            #for i, j, k in zip(range_list, range_falloff_ratio_list, range_falloff_total_damage):
                #if (falloff_end - falloff_start > 1/1000):
                   # range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start))
            j = 0
            for i in range_list:
                if (falloff_end - falloff_start > 1/1000):
                    range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start)) 
            ##DEFAULT
                if i < falloff_start:
                    print('Range has no damage falloff')
                else:                   
                    range_falloff_total_damage[j] = (data['Damage'] * (1.0 - range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))
                    print('Adding damage' , j)
                j += 1
                      
        elif data['DistantVarianceReversed'] == True:
                    #reversed tree
            print('Im not done yet!')

    except KeyError:
        print('No DistantVarianceReversed key on weapon!')
elif not data['isDamageVariation']:
    print('No damage variance, using normal values')
print(range_falloff_ratio_list)
print(range_falloff_total_damage)