##ToDo List
#add checks for accuracy and evasion ignore (EvasivePipsIgnored and  AccuracyModifier)
#add max range damage falloff, or even better add damage expected at each range bracket (Weapon Heat/Damage/Stability falls off to {0} of starting value at long range) Done for standard, need to add for reversed
#add mode accuracy bonuses/maluses

#OPTIMIZATION
#Change for loop iterator for each file to check for modes at the start of the loop and set a variable has_modes, can call this for each check to save time/cycles

import os
import json
import traceback
import pandas
import time
time1 = time.time()#this is simply to test time efficiency

#change location variable to point to root of install location you want to analize.
location = 'E:\Roguetech\RogueTech'
file_keyword_exclusion_list = ['Quirks', 'Melee', 'Special', 'Turret', 'Ambush']
weapon_file_list = []
excepted_files = []
possible_invalid_jsons = []
df = pandas.DataFrame(columns=['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire', 'Tonnage', 'Slots', 'Max Recoil', 'Max Damage', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage', 'Max Firing Heat', 'Max Jam Chance', 'Can Misfire', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Minimum Range', 'Short Range', 'Medium Range', 'Long Range', 'Max Range', 'Min Range Damage', 'Short Range Damage', 'Medium Range Damage', 'Long range Damage','Max Range Damage'])
##

#This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list weapon_file_list
# r=>root, d=>directories, f=>files
for r, d, f in os.walk(location):
   for item in f:
      file_in_exclusion_list = False
      if 'Weapon_' in item:
         print('File has weapon in name: ', item)
         if 'json' in item:
            print('File also has json in name: ', item)
            for i in file_keyword_exclusion_list:
               print(i, file_in_exclusion_list)
               if i in item:
                  file_in_exclusion_list = True
                  continue
            if not file_in_exclusion_list:
               weapon_file_list.append(os.path.join(r, item))
               print('Passed ',item)            
##

#this iterates through the identified list of files meeting search criteria, prints the filename and loads them with the json module so you can search them and finally checks if there is any loading errors and adds them to lists to help identify invalid JSONs or bad characters.
for item in weapon_file_list:
   with open(item) as f:
      print(item)
      try: 
         data = json.load(f)
         current_row = []
         
         #Weapon hardpoint module
         try:
            hardpoint_type = str(data['Category'])
            print(hardpoint_type)
         except KeyError:
            print('Missing Hardpoint Type')
            try:
                hardpoint_type = str(data['weaponCategoryID'])
            except KeyError:
               print('Weapon has no Type?')
               hardpoint_type = 'N/A'
         current_row.append(hardpoint_type)

         #Weapon type module
         try:
            weapon_class = str(data['Type'])
            print(weapon_class)
            current_row.append(weapon_class)
         except KeyError:
            print('Missing Weapon Type')
            current_row.append('N/A')
         
         #Weapon name module
         try:
            weapon_name = str(data['Description']['UIName'])
            print(weapon_name)
            current_row.append(weapon_name)
         except KeyError:
            print('Missing Weapon Name')
            current_row.append('N/A')
         #weapon damage module - pulls the highest damage from base + any available modes and sets value to weapon_damage variable
         try:
            max_mode_dam = 0 #set mode index of mode highest dam weapon
            max_dam_mode = 0 #set value of highest additional damage in modes
            weapon_damage = 0 #Damage modes loop max damage value
            for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
               print('Damage mode', i)
               try:
                     if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                        max_mode_dam = data['Modes'][i]['DamagePerShot']
                        max_dam_mode = i
                     try:
                        if data['Modes'][i]['ShotsWhenFired']:#check for ShotsWhenFired in mode
                           weapon_damage = data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
                     except KeyError:
                        traceback.print_exc()
                        weapon_damage = data['Damage'] + max_mode_dam * data['ProjectilesPerShot'] * data['ShotsWhenFired']
               except KeyError: #if no DamagePerShot in mode found
                     traceback.print_exc()
                     print('skipped')
         except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
            print('No modes. Reverting to base values.')
            traceback.print_exc()
            weapon_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot

         try:
            max_shots_mode = 0 #set mode index of mode with highest shot count
            max_mode_shots = 0 #set value of mode with most additional shots
            weapon_damage2 = 0 #Shots modes loop max damage value
            for i in range(len(data['Modes'])):
               print('Shots loop:', i)
               try:#if no damage in modes found then check modes for additional shots and calculate damage against base value
                     if data['Modes'][i]['ShotsWhenFired'] > max_mode_shots:
                        max_mode_shots = data['Modes'][i]['ShotsWhenFired']
                        max_shots_mode = i
                     try:
                        weapon_damage2 = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_shots_mode]['ShotsWhenFired']) #damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
                        print(max_mode_shots)
                     except:
                        print('can this be reached?')
                        traceback.print_exc()
               except:
                     weapon_damage2 = data['Damage'] + max_mode_shots * data['ProjectilesPerShot'] * data['ShotsWhenFired']   
         except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
            print('No modes. Reverting to base values.')
            weapon_damage2 = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot

         if weapon_damage2 > weapon_damage:#checks the max damage mode and the max shots mode loop max damage values against each other and sets the highest 
            weapon_damage = weapon_damage2
         current_row.append(weapon_damage)
         print(weapon_damage, weapon_damage2)

         #Indirectfire check module
         try:
            for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
                  print('Mode ', i)
                  try:
                     if data['Modes'][i]['IndirectFireCapable'] == True:
                        indirect_fire = 'True'
                        break                    
                  except KeyError: #if no IndirectFireCapable in mode found
                        traceback.print_exc()
                        try:
                           indirect_fire = str(data['IndirectFireCapable'])
                        except KeyError:
                           print('Missing Indirect Fire boolean')
                           indirect_fire = 'False'
         except KeyError:
            try:
               indirect_fire = str(data['IndirectFireCapable'])
            except KeyError:
               print('Missing Indirect Fire boolean')
               indirect_fire = 'False'
         current_row.append(indirect_fire)
        
         #Tonnage check module
         try:
            weapon_tonnage = data['Tonnage']
            print('Tons ' + str(weapon_tonnage))
            current_row.append(weapon_tonnage)
            if weapon_tonnage > 50: #this filters deprecated weapons that are 100 to 6666 tons
               continue
         except:
            print('Missing Tonnage')
            current_row.append('N/A')

         #Weapon slot size module
         try:
            weapon_slots = data['InventorySize']
            print('Slots ' + str(weapon_slots))
            current_row.append(weapon_slots)
         except:
            print('Missing Weapon Slots')
            current_row.append('N/A')

         ##add logic to test which mode is has the highest refire! Output int Y
         try:
            weapon_recoil = data['RefireModifier'] + data['Modes'][max_dam_mode]['RefireModifier']
            print('Recoil ' + str(weapon_recoil))
            current_row.append(weapon_recoil)
         except (KeyError, IndexError) as e:
            try:
               weapon_recoil = data['RefireModifier']
               print('No recoil in modes, defaulting to base', 'Recoil ' + str(weapon_recoil))
               current_row.append(weapon_recoil)
            except KeyError:
               print('No Refire Modifier on this weapon')
               current_row.append(0)
         
         #Damage variance module
         try:
            weapon_damage_variance = data['DamageVariance']
            print('Dam Var ' + str(weapon_damage_variance))
            current_row.append(weapon_damage_variance)
         except KeyError:
            print('No damage variance key!?')
            current_row.append(0)

         #output float Y
         try:
            weapon_stability_damage = data['Instability'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
            print('Stability dam ' + str(weapon_stability_damage))
            current_row.append(weapon_stability_damage)
         except (KeyError, IndexError) as e:   
            try:
               weapon_stability_damage = data['Instability'] * data['ShotsWhenFired'] #stability damage = stability damage per shot * shotswhenfired
               print('Stability dam ' + str(weapon_stability_damage))
               current_row.append(weapon_stability_damage)
            except KeyError:
               print('No Stability damage key on this weapon!?')
               current_row.append('N/A')

         ##add logic here to test which mode has the highest heat damage! output int
         try:
            weapon_heat_damage = data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #heat damage = heat damage per shot * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes)
            print('Heat dam ' + str(weapon_heat_damage))
            current_row.append(weapon_heat_damage)
         except (KeyError, IndexError) as e:   
            try:
               weapon_heat_damage = data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired']) #heat damage = heat damage per shot * projectilespershot
               print('Heat dam' + str(weapon_heat_damage))
               current_row.append(weapon_heat_damage)
            except KeyError:
               print('No heat damage key on this weapon!?')
               current_row.append(0)

         ##add logic here to test which mode has the highest firing heat! output int
         try:
            weapon_firing_heat = data['HeatGenerated'] + data['Modes'][max_dam_mode]['HeatGenerated']
            print('Firing Heat ' + str(weapon_firing_heat))
            current_row.append(weapon_firing_heat)
         except (KeyError, IndexError) as e:
            try:
               weapon_firing_heat = data['HeatGenerated']
               print('No firing heat in modes, defaulting to base ', 'Firing Heat ' + str(weapon_firing_heat))
               current_row.append(weapon_firing_heat)
            except KeyError:
               print('No weapon firing heat key on this weapon')
               current_row.append(0)

         ##add logic here to test which mode has the highest jamming chance! output float
         try:
            weapon_flat_jam = data['FlatJammingChance'] #FlatJammingChance is handled backwards to ShotsWhenFired. Most mode weapons don't have a base FlatJammingChance key and ONLY have them in the modes. Check for base FIRST then check for modes based on that.
            try:
               weapon_flat_jam = (data['FlatJammingChance'] + data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)  
               print('Flat jamming chance ' + str(weapon_flat_jam))
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               weapon_flat_jam = (data['FlatJammingChance'] * 100)
               print('No modes, reverting to base jam chance ' + str(weapon_flat_jam) + '%')
               current_row.append(weapon_flat_jam)
         except KeyError:
            try:
               weapon_flat_jam = (data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)
               print('No base flat jamming chance key, using modes ' + str(weapon_flat_jam) + '%')
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               print('No flat jamming chance on this weapon.')
               current_row.append(0)

         #weapon can misfire in max damage mode?
         try:
            weapon_misfire = str(data['DamageOnJamming'])
            try:
               weapon_misfire = str(data['Modes'][max_dam_mode]['DamageOnJamming'])
            except KeyError:
               print('Weapon has no modes, using base')
         except KeyError:
            try:
               if 'wr-damage_when_jam' in data['ComponentTags']['items']:
                  weapon_misfire = 'True'
               else:
                  weapon_misfire = 'False'
            except KeyError:
               print('No jamming on this weapon')
               weapon_misfire = 'False'
         if weapon_misfire == 'False':
            try:
               for i in data['Custom']['BonusDescriptions']['Bonuses']:
                  if 'Explodium' in i: #this verifies that the weapon descriptions do not list misfires when traits do not have them
                     excepted_files.append(item)
            except KeyError:
               print('No Custom categories or BonusDescriptions')
         current_row.append(weapon_misfire)

         try:
            weapon_damage_per_heat = "{:.2f}".format(float(weapon_damage)/(float(weapon_firing_heat)))       
            print(weapon_damage_per_heat)
            current_row.append(weapon_damage_per_heat)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append('0')

         try:
            weapon_damage_per_slot = "{:.2f}".format(float(weapon_damage)/(float(weapon_slots)))
            print(weapon_damage_per_slot)
            current_row.append(weapon_damage_per_slot)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append('0')

         try:
            weapon_damage_per_ton = "{:.2f}".format(float(weapon_damage)/(float(weapon_tonnage)))
            print(weapon_damage_per_ton)
            current_row.append(weapon_damage_per_ton)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append('0')

         #output int
         try:
            weapon_range_min = data['MinRange']
            current_row.append(weapon_range_min)
         except KeyError:
            traceback.print_exc()
         
         try:
            weapon_range_short = data['RangeSplit'][0]
            current_row.append(weapon_range_short)
         except KeyError:
            traceback.print_exc()
         
         try:
            weapon_range_medium = data['RangeSplit'][1]
            current_row.append(weapon_range_medium)
         except KeyError:
            traceback.print_exc()

         try:
            weapon_range_long = data['RangeSplit'][2]
            current_row.append(weapon_range_long)
         except KeyError:
            traceback.print_exc()

         try:
            weapon_range_max = data['MaxRange']
            current_row.append(weapon_range_max)
         except KeyError:
            traceback.print_exc()
         
         print('Min ' + str(weapon_range_min)  + ' Short ' + str(weapon_range_short) + ' Medium ' + str(weapon_range_medium) + ' Long ' + str(weapon_range_long) + ' Max ' + str(weapon_range_max))

         range_list = [weapon_range_min, weapon_range_short, weapon_range_medium, weapon_range_long, weapon_range_max]
         range_falloff_ratio_list = [0,0,0,0,0] #this is not being populated
         range_falloff_total_damage = [0,0,0,0,0]

         try: 
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
                        j = 0
                        for i in range_list:
                           if (falloff_end - falloff_start > 1/1000):
                              range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start)) 
                        ##DEFAULT
                           if i < falloff_start:
                              print('Range has no damage falloff')
                              current_row.append(weapon_damage)
                           else: #DO THE THING                  
                              current_row.append(weapon_damage * (1.0 - range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))
                              print('Adding damage')
                           j += 1
                                 
                  elif data['DistantVarianceReversed'] == True:
                              #reversed tree
                     print('Im not done yet!')
                     for i in range(5):
                        current_row.append(weapon_damage)
               except KeyError:
                  print('No DistantVarianceReversed key on weapon!')
                  for i in range(5):
                     current_row.append(weapon_damage)
         except KeyError:
            print('No damage variance, using normal values')
            for i in range(5):
               current_row.append(weapon_damage)


         #l.insert(newindex, l.pop(oldindex))
         current_row.insert(7,current_row.pop(3)) #this rearranges the current_row list to properly format it for the excel sheet

         df2 = pandas.DataFrame([current_row], columns=(['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire', 'Tonnage', 'Slots', 'Max Recoil', 'Max Damage', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage', 'Max Firing Heat', 'Max Jam Chance', 'Can Misfire', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Minimum Range', 'Short Range', 'Medium Range', 'Long Range', 'Max Range', 'Min Range Damage', 'Short Range Damage', 'Medium Range Damage', 'Long range Damage','Max Range Damage']))
         print(df2)
         df = df.append(df2)
      except UnicodeDecodeError:
         excepted_files.append(item)
         print('Possible invalid character in JSON')
      except json.decoder.JSONDecodeError:
         possible_invalid_jsons.append(item)
         print('Possible invalid JSON!')

#Used to write filenames of different types of excepted files to separate text files for analyzation later
with open("excepted files.txt", "w") as output:
   for item in excepted_files:
       output.write(str(item) + '\n')

with open("possible invalid JSON.txt", "w") as output:
   for item in possible_invalid_jsons:
       output.write(str(item) + '\n')
##
df.to_excel('RT Weaponlist.xlsx',sheet_name='Weapons')
print('Parsed in', time.time() - time1, 'seconds')

#use this to write to json without unicode errors? future use?
#with open('s1Results/map.json', 'wb') as f:
 #   jdata = json.dumps(r.json(), indent=4, ensure_ascii=False)
  #  f.write(jdata.encode())



#OLD Damage module
         #try:
            #weapon_damage = str(data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired'])) #damage = damage per shot * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes)
            #print('Dam ' + weapon_damage)
            #current_row.append(weapon_damage)
        # except (KeyError, IndexError) as e:
            #try:
               #weapon_damage = str(data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])) #damage = damage per shot * projectilespershot
               #print('No damage in modes, defaulting to base', 'Dam ' + weapon_damage)
               #current_row.append(weapon_damage)
            #except KeyError:
               #print('No damage on this weapon!?')
               #current_row.append('N/A')
         ##