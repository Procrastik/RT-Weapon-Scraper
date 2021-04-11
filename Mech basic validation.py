import json
import traceback

mechdef_file = r"C:\Users\fireb\Desktop\WIP\mechdef_zeus_ZEU-6S.json"
chassisdef_file = r"C:\Users\fireb\Desktop\WIP\chassisdef_zeus_ZEU-X.json"
#def_list = [mechdef_file, chassisdef_file]

heatsink_num = int(input('Input total number of Heat Sinks:'))
weapon_num = int(input('Input total number of Weapons:'))
left_arm_limit = str(input('Input lowest Left Arm part:')).lower
right_arm_limit = str(input('Input lowest Right Arm part:')).lower
file_heatsink_num = 0
file_weapon_num = 0

with open(mechdef_file) as mechdef:
    mdata = json.load(mechdef)

with open(chassisdef_file) as chassisdef:
    cdata = json.load(chassisdef)

for i in mdata['inventory']:
    print(i)
    print(i['ComponentDefID'])
    if 'Gear_HeatSink' or 'Gear_Engine_Heatsinks' in i['ComponentDefID']:
        print('check 1 works')
        if 'Gear_HeatSink' in i['ComponentDefID']:
            print('check 2')
            file_heatsink_num += 1
        elif 'Gear_Engine_Heatsinks_' in i['ComponentDefID']:
            print('check 3')
            file_heatsink_num += int(i['ComponentDefID'][-1])
        elif 'Gear_EmergencyCoolant' in i['ComponentDefID']:
            print('check 4')
            file_heatsink_num += int(i['ComponentDefID'][-1])
    if file_heatsink_num + 10 is heatsink_num:
        print('Heat Sinks match entered value')
    elif file_heatsink_num + 10 is not heatsink_num:
        print('Heat Sinks DO NOT match entered value!')
print('Heatsinks in file: ' + str(file_heatsink_num))


    #check for heatsink number match

    #check for weapon number match

    #check for left/right arm actuator match

    #check for armor match??

