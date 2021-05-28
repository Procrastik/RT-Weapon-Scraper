#OPTIMIZATION
#Change for loop iterator for each file to check for modes at the start of the loop and set a variable has_modes, can call this for each check to save time/cycles
#set a logging variable to enable full logging or no logging

import os
import json
import traceback
import pandas
import time
import re
time1 = time.time()#this is simply to test time efficiency

#change location variable to point to root of install location you want to analyze.
location = 'D:\RogueTech Git\RogueTech'
file_keyword_exclusion_list = ['Melee', 'Special', 'Turret', 'Ambush','Infantry', 'deprecated']
weapon_file_list = []
ams_file_list = []
filtered_files = []
excepted_files = []
possible_invalid_jsons = []
columns_list = ['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire', 'Clustering Capable (Weapon or with ammo)', 'Tonnage', 'Slots', 'Max Recoil', 'Base Damage', 'Max Damage', 'Max Ammo Damage', 'Highest Direct Damage Ammo', 'AOE Damage', 'AOE Radius', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage', 'Max Ammo Heat Damage', 'Highest Direct Heat Damage Ammo', 'Max Firing Heat', 'Max Jam Chance', 'Can Misfire', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Weapon Crit Multiplier', 'Weapon Base Crit Chance', 'Weapon TAC Chance (50% Max Thickness)', 'Max TAC Armor Thickness', 'Base Accuracy Bonus', 'Base Evasion Ignore', 'Minimum Range', 'Short Range', 'Medium Range', 'Long Range', 'Max Range', 'Damage Falloff %', 'Min Range Damage', 'Short Range Damage', 'Medium Range Damage', 'Long Range Damage','Max Range Damage']
ams_columns_list = ['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Tonnage', 'Slots', 'Multiple Activations Per Round', 'Base Damage Per Shot', 'Base Average Damage', 'Base Max Damage Per Activation', 'Base Shots Per Activation', 'Base Hit Chance', 'Base Heat Per Activation', 'Base Jam Chance', 'Base Max Range', 'Base Protect Allies', 'OL Damage Per Shot', 'OL Average Damage', 'OL Max Damage Per Activation', 'OL Shots Per Activation', 'OL Hit Chance', 'OL Heat Per Activation', 'OL Jam Chance', 'OL Max Range', 'OL Protect Allies', 'Full Power Damage Per Shot', 'Full Power Average Damage', 'Full Power Max Damage Per Activation', 'Full Power Shots Per Activation', 'Full Power Hit Chance', 'Full Power Heat Per Activation', 'Full Power Jam Chance', 'Full Power Max Range', 'Full Power Protect Allies']
df = pandas.DataFrame(columns=columns_list)
ams_df = pandas.DataFrame(columns=ams_columns_list)
##

ammo_file_list = []
ammotype_dam_dict = {}
ammotype_dam_best_dict = {}
ammotype_heatdam_dict = {}
ammotype_heatdam_best_dict = {}
ammotype_doescluster_dict = {}
ammotype_dam_multi_dict = {}
ammotype_dam_multi_best_dict = {}
##

#This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list ammo_file_list
# r=>root, d=>directories, f=>files
for r, d, f in os.walk(location):
   print(r)
   for item in f:
      file_in_exclusion_list = False
      if 'Ammunition_' in item:
         print('File has Ammunition in name: ', item)
         if 'json' in item:
            print('File also has json in name: ', item)
            for i in file_keyword_exclusion_list:
               print(i, file_in_exclusion_list)
               if i in item:
                  file_in_exclusion_list = True
                  continue
               elif i in r:
                  file_in_exclusion_list = True
                  continue
            if not file_in_exclusion_list:
               ammo_file_list.append(os.path.join(r, item))
               print('Passed ',item)            
##

#this iterates through the identified list of files meeting search criteria, prints the filename and loads them with the json module so you can search them and finally checks if there is any loading errors and adds them to lists to help identify invalid JSONs or bad characters.
#Do not combine this with the weapon_file_list because it is twice as fast this way than combined
for item in ammo_file_list:
   with open(item) as f:
        print(item)
        try: 
            data = json.load(f)
            try:
               if data['Category'] not in ammotype_dam_multi_dict.keys():#this if block handles building new keys in the dict for ammo types not already in the dict
                  print('New category, adding')
                  try:
                     if data['DamageMultiplier'] > 1:
                        ammotype_dam_multi_dict[data['Category']] = data['DamageMultiplier']
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam Multiplier', ammotype_dam_multi_dict[data['Category']])
                     else:
                        print('No DamageMultiplier on ammo; Defaulting to 1.')
                        ammotype_dam_multi_dict[data['Category']] = 1
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam Multiplier', ammotype_dam_multi_dict[data['Category']])
                  except KeyError:
                     print('No DamageMultiplier on ammo; Defaulting to 1.')
                     ammotype_dam_multi_dict[data['Category']] = 1
                     ammotype_dam_multi_best_dict[data['Category']] = f.name
                     print('Dam Multiplier ', ammotype_dam_multi_dict[data['Category']])

                  try:
                     if data['DamagePerShot'] > 0:
                        ammotype_dam_dict[data['Category']] = data['DamagePerShot']
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dampershot', ammotype_dam_dict[data['Category']])
                     else:
                        print('No DamagePerShot on ammo; Defaulting to 0.')
                        ammotype_dam_dict[data['Category']] = 0
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dampershot ', ammotype_dam_multi_dict[data['Category']])
                  except KeyError:
                     print('No DamagePerShot on ammo; Defaulting to 0.')
                     ammotype_dam_dict[data['Category']] = 0
                     ammotype_dam_best_dict[data['Category']] = f.name
                     print('Dampershot ', ammotype_dam_dict[data['Category']])

                  try:
                     if data['HeatDamagePerShot'] > 0:
                        ammotype_heatdam_dict[data['Category']] = data['HeatDamagePerShot']
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                     else:
                        print('No HeatDamagePerShot on ammo; Defaulting to 0.')
                        ammotype_heatdam_dict[data['Category']] = 0
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                  except KeyError:
                     print('No HeatDamagePerShot on ammo; Defaulting to 0.')
                     ammotype_heatdam_dict[data['Category']] = 0
                     ammotype_heatdam_best_dict[data['Category']] = f.name
                     print('Heatdam ', ammotype_heatdam_dict[data['Category']])

                  try:
                     if data['HitGenerator'] == 'Cluster':
                        ammotype_doescluster_dict[data['Category']] = True
                        print(ammotype_doescluster_dict[data['Category']], ' does cluster!')
                     else:
                        ammotype_doescluster_dict[data['Category']] = False
                        print(ammotype_doescluster_dict[data['Category']], ' Ammo does not Cluster')
                  except KeyError:
                     print('No HitGenerator trait on ammo, defaulting to False')
                     ammotype_doescluster_dict[data['Category']] = False
                     print(ammotype_doescluster_dict[data['Category']], ' does not Cluster')
                  
               elif data['Category'] in ammotype_dam_multi_dict.keys():#this block compares existing key values to the currently evaluated ammo type
                  print('Existing category, comparing')
                  try:
                     if data['DamageMultiplier'] > ammotype_dam_multi_dict[data['Category']]:
                        ammotype_dam_multi_dict[data['Category']] = data['DamageMultiplier']
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam ', ammotype_dam_multi_dict[data['Category']])
                     elif data['DamageMultiplier'] == ammotype_dam_multi_dict[data['Category']]:
                        ammotype_dam_multi_best_dict[data['Category']] = 'Multiple'
                  except KeyError:
                     print('No DamageMultiplier on ammo; Comparing to best in case they are the same')
                     if ammotype_dam_multi_dict[data['Category']] == 1:
                        ammotype_dam_multi_best_dict[data['Category']] = 'Multiple'
                  
                  try:
                     if data['DamagePerShot'] > ammotype_dam_dict[data['Category']]:
                        ammotype_dam_dict[data['Category']] = data['DamagePerShot']
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dam ', ammotype_dam_dict[data['Category']])
                     elif data['DamagePerShot'] == ammotype_dam_dict[data['Category']]:
                        print('Ammo DamagePerShot equal to existing best, setting best to multiple')
                        ammotype_dam_best_dict[data['Category']] = 'Multiple'
                  except KeyError:                     
                     print('No DamagePerShot on ammo; Comparing to best in case they are the same')
                     if ammotype_dam_dict[data['Category']] == 0:
                        print('Ammo DamagePerShot equal to 0 or existing best, setting best to multiple')
                        ammotype_dam_best_dict[data['Category']] = 'Multiple'

                  try:
                     if data['HeatDamagePerShot'] > ammotype_heatdam_dict[data['Category']]:
                        ammotype_heatdam_dict[data['Category']] = data['HeatDamagePerShot']
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                     elif data['DamagePerShot'] == ammotype_heatdam_dict[data['Category']]:
                        ammotype_heatdam_best_dict[data['Category']] = 'Multiple'
                  except KeyError:
                     print('No HeatDamagePerShot on ammo; Skipping as key already has an entry of 0 or above')
                     if ammotype_heatdam_dict[data['Category']] == 1:
                        ammotype_heatdam_best_dict[data['Category']] = 'Multiple'
                  try:
                     if ammotype_doescluster_dict[data['Category']] == False:
                        if data['HitGenerator'] == 'Cluster':
                           ammotype_doescluster_dict[data['Category']] = True
                           print(ammotype_doescluster_dict[data['Category']], ' does cluster!')
                  except KeyError:
                     print('No HitGenerator trait on ammo, skipping.')
            except KeyError:
               traceback.print_exc()
               print('No Category on ammo! Skipping.')
        except UnicodeDecodeError:
            excepted_files.append(item)
            print('Possible invalid character in JSON')
        except json.decoder.JSONDecodeError:
            possible_invalid_jsons.append(item)
            print('Possible invalid JSON!')
print(ammotype_dam_multi_best_dict, ammotype_dam_multi_dict, ammotype_heatdam_best_dict, ammotype_heatdam_dict, ammotype_dam_best_dict, ammotype_dam_dict, ammotype_doescluster_dict)

#This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list weapon_file_list
# r=>root, d=>directories, f=>files
for r, d, f in os.walk(location):
   print(r)
   for item in f:
      file_in_exclusion_list = False
      if 'Weapon_' in item:
         print('File has weapon in name: ', item)
         if 'json' in item:
            print('File also has json in name: ', item)
            if 'AMS' in item:
               print('AMS in weapon loop, skipping')
               continue
            for i in file_keyword_exclusion_list:
               print(i, file_in_exclusion_list)
               if i in item:
                  file_in_exclusion_list = True
                  continue
               elif i in r:
                  file_in_exclusion_list = True
                  continue
            if not file_in_exclusion_list:
               weapon_file_list.append(os.path.join(r, item))
               print('Passed ',item)            
##

#This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list ams_file_list
# r=>root, d=>directories, f=>files
for r, d, f in os.walk(location):
   print(r)
   for item in f:
      file_in_exclusion_list = False
      if 'AMS' in item:
         print('File has weapon and AMS in name: ', item)
         if 'Weapon_' in item:
            print('File also has Weapon also in name')
            if 'json' in item:
               print('File also has json in name: ', item)
               for i in file_keyword_exclusion_list:
                  print(i, file_in_exclusion_list)
                  if i in item:
                     file_in_exclusion_list = True
                     continue
                  elif i in r:
                     file_in_exclusion_list = True
                     continue
               if not file_in_exclusion_list:
                  ams_file_list.append(os.path.join(r, item))
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
            if 'deprecated' in str(data['Description']['UIName']).lower():
               print('Deprecated in name, skipping')
               filtered_files.append(item)
               continue
            weapon_name = str(data['Description']['UIName'])
            print(weapon_name)
            current_row.append(weapon_name)
         except KeyError:
            print('Missing Weapon Name')
            current_row.append('N/A')

         #weapon damage module - pulls the highest damage from base + any available modes and sets value to weapon_damage variable
         try:
            max_mode_dam = 0 #set value of highest additional damage in modes
            max_dam_mode = 0  #set value of highest additional damage in modes
            weapon_damage = 0 #Damage modes loop max damage value
            for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
               print('Damage mode', i)
               try:
                  if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                     max_mode_dam = data['Modes'][i]['DamagePerShot']
                     max_dam_mode = i
                  try:
                     if data['Modes'][i]['ShotsWhenFired']:#check for ShotsWhenFired in mode
                        weapon_damage = (data['Damage'] + max_mode_dam) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
                  except KeyError:
                     weapon_damage = (data['Damage'] + max_mode_dam) * data['ProjectilesPerShot'] * data['ShotsWhenFired']
               except KeyError: #if no DamagePerShot in mode found
                     print('No DamagePerShot in modes, reverting to base values')
                     weapon_damage = data['Damage'] * data['ProjectilesPerShot'] * data['ShotsWhenFired']
         except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
            print('No modes, reverting to base values')
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
                     weapon_damage2 = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + max_mode_shots) #damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
                     print(max_mode_shots)
                  except:
                     print('can this be reached?')
                     traceback.print_exc()
               except:
                  traceback.print_exc()
                  print('No additional ShotsWhenFired found in modes, reverting to base')   
         except KeyError: #removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
            print('No modes. Reverting to base values.')
            weapon_damage2 = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired']) #damage = damage per shot * projectilespershot
         print('DMG Modes ' + str(weapon_damage),' Shots Modes ', str(weapon_damage2))
         if weapon_damage2 > weapon_damage:#checks the max damage mode and the max shots mode loop max damage values against each other and sets the highest 
            weapon_damage = weapon_damage2
            max_dam_mode = max_shots_mode
         current_row.append(weapon_damage)

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

         #Weapon cluster module
         weapon_cluster = 'False'
         try:
            if data['HitGenerator'] == 'Cluster':
               weapon_cluster = 'True'
               print('HitGenerator cluster on weapon')
            else:
               try:
                  if 'wr-clustered_shots' in data['ComponentTags']['items']:
                     weapon_cluster = 'True'
                     print('wr-clustered_shots on weapon')
                  elif data['Type'] == 'LRM':
                     print('WeaponType is LRM')
                     try:
                        if data['HitGenerator'] == 'Cluster':
                           weapon_cluster = 'True'
                     except KeyError:
                        print('Weapon is LRM and has no other HitGenerators, it does cluster.')
                        weapon_cluster = 'True'
               except KeyError:
                  print('No wr-clustered_shots or Weapon Type, skipping')
         except KeyError:
            print('No HitGenerator trait on base weapon, checking other options')
            try:
               if 'wr-clustered_shots' in data['ComponentTags']['items']:
                  weapon_cluster = 'True'
               elif data['Type'] == 'LRM':
                  try:
                     if data['HitGenerator'] == 'Cluster':
                        weapon_cluster = 'True'
                  except KeyError:
                     print('Weapon is LRM and has no other HitGenerators, it does cluster.')
                     weapon_cluster = 'True'
            except KeyError:
               print('No wr-clustered_shots or Weapon Type, skipping')
         try:
            if weapon_cluster == 'False': 
               for i in range(len(data['Modes'])): #for loop to iterate over the number of Modes found
                  print('Cluster check Mode ', i)
                  try:
                     if data['Modes'][i]['HitGenerator'] == 'Cluster':
                        weapon_cluster = 'True in Mode'
                        continue
                  except KeyError:
                     print('No clustering on this mode, trying next')
         except KeyError:
            print('No modes found on weapon for cluster check')
         try:
            if ammotype_doescluster_dict[data['AmmoCategory']] == True:
               weapon_cluster = 'True in Ammo'
         except KeyError:
            print('No ammo clustering for this weapon')
                            
         current_row.append(weapon_cluster)

         #Tonnage check module
         if hardpoint_type == 'Special':
            weapon_tonnage = data['Custom']['HandHeld']['Tonnage']
            current_row.append(weapon_tonnage)
         elif hardpoint_type == 'SpecialMelee':
            weapon_tonnage = data['Custom']['HandHeld']['Tonnage']
            current_row.append(weapon_tonnage)
         else:
            try:
               weapon_tonnage = data['Tonnage']
               print('Tons ' + str(weapon_tonnage))
               current_row.append(weapon_tonnage)
               if weapon_tonnage > 50: #this filters deprecated weapons that are 100 to 6666 tons
                  print('Filtered out deprecated weapon by tonnage')
                  filtered_files.append(item)
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

         ##weapon refire module
         try:
            if weapon_damage > weapon_damage2:
               weapon_recoil = data['RefireModifier'] + data['Modes'][max_dam_mode]['RefireModifier']
               print('Recoil ' + str(weapon_recoil))
               current_row.append(weapon_recoil)
            elif weapon_damage2 >= weapon_damage:
               weapon_recoil = data['RefireModifier'] + data['Modes'][max_shots_mode]['RefireModifier']
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
         current_row.append(weapon_base_damage)

         #Weapon most damaging ammotype damage value module
         try:
            current_row.append(ammotype_dam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
         except KeyError:
            print('Weapon has no ammo')
            current_row.append('N/A')

         #Weapon most damaging ammotype module
         try:
            pattern = '\w*.json'
            match_var = re.search(pattern,ammotype_dam_best_dict[data['AmmoCategory']])
            current_row.append(match_var.group()[:-5])
            print('Best ammo is ' + match_var.group()[:-5])
         except (KeyError, TypeError) as e:
            traceback.print_exc()
            current_row.append('N/A')
            print('Weapon has no ammo category')
         except AttributeError:
            traceback.print_exc()
            current_row.append(ammotype_dam_best_dict[data['AmmoCategory']])         

         #Weapon AOE damage and range module
         try:
            if data['AOECapable'] == True:
               print('Weapon has base AOE capability')
               weapon_damage_AOE = data['AOEDamage']
               weapon_AOE_radius = data['AOERange']
               current_row.append(weapon_damage_AOE)
               current_row.append(weapon_AOE_radius)
            else:
               weapon_damage_AOE = 0
               weapon_AOE_radius = 0 
               current_row.append(0)
               current_row.append(0)
         except KeyError:
            print('Weapon does not have base AOE capability; AOE could be through through modes or ammo though')
            weapon_damage_AOE = 0
            weapon_AOE_radius = 0
            current_row.append(0)
            current_row.append(0)

         #Damage variance module
         try:
            weapon_damage_variance = data['DamageVariance']
            print('Dam Var ' + str(weapon_damage_variance))
            current_row.append(weapon_damage_variance)
         except KeyError:
            print('No damage variance key!?')
            current_row.append(0)

         #Weapon stability damage module
         try:
            if data['ImprovedBallistic'] == True: #instability is divided among all projectiles per shot
               print('ImprovedBallistic True')
               try:
                  weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * data['InstabilityMultiplier'] * data['Modes']['InstabilityMultiplier'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                  print('Stability dam ' + str(weapon_stability_damage))
                  current_row.append(weapon_stability_damage)
               except (KeyError, IndexError, TypeError) as e:
                  print('No modes or no other mode related key, trying another combo (1st try)')
                  try:
                     weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * data['Modes']['InstabilityMultiplier'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                     print('Stability dam ' + str(weapon_stability_damage))
                     current_row.append(weapon_stability_damage)
                  except (KeyError, IndexError, TypeError) as e:
                     print('No modes or no other mode related key, trying another combo (2nd try)')
                     try:
                        weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                        print('Stability dam ' + str(weapon_stability_damage))
                        current_row.append(weapon_stability_damage)
                     except (KeyError, IndexError, TypeError) as e:
                        print('No modes or no other mode related key, trying another combo (3rd try)')
                        try:
                           weapon_stability_damage = data['Instability'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                           print('Stability dam ' + str(weapon_stability_damage))
                           current_row.append(weapon_stability_damage)
                        except (KeyError, IndexError) as e:
                           print('No modes, trying base values')
                           try:
                              weapon_stability_damage = data['Instability'] * data['ShotsWhenFired'] #stability damage = stability damage per shot * shotswhenfired
                              print('Stability dam ' + str(weapon_stability_damage))
                              current_row.append(weapon_stability_damage)
                           except KeyError:
                              print('No Stability damage key on this weapon!?')
                              current_row.append(0)

            elif data['ImprovedBallistic'] == False: #Instability is not divided up across projectiles per shot and is applied fully per projectile.
               print('ImprovedBallistic False')
               try:
                  weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * data['InstabilityMultiplier'] * data['Modes']['InstabilityMultiplier'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                  print('Stability dam ' + str(weapon_stability_damage))
                  current_row.append(weapon_stability_damage)
               except (KeyError, IndexError, TypeError) as e:
                  print('No modes or no other mode related key, trying another combo (1st try)')
                  try:
                     weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * data['Modes']['InstabilityMultiplier'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                     print('Stability dam ' + str(weapon_stability_damage))
                     current_row.append(weapon_stability_damage)
                  except KeyError:
                     print('No modes or no other mode related key, trying another combo (2nd try)')
                     try:
                        weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                        print('Stability dam ' + str(weapon_stability_damage))
                        current_row.append(weapon_stability_damage)
                     except (KeyError, IndexError, TypeError) as e:
                        print('No modes or no other mode related key, trying another combo (3rd try)')
                        try:
                           weapon_stability_damage = data['Instability'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                           print('Stability dam ' + str(weapon_stability_damage))
                           current_row.append(weapon_stability_damage)
                        except (KeyError, IndexError) as e:
                           print('No modes, trying base values')
                           try:
                              weapon_stability_damage = data['Instability'] * (data['ShotsWhenFired'] * data['ProjectilesPerShot']) #stability damage = stability damage per shot * shotswhenfired
                              print('Stability dam ' + str(weapon_stability_damage))
                              current_row.append(weapon_stability_damage)
                           except KeyError:
                              print('No Stability damage key on this weapon!?')
                              current_row.append(0)
            
         except KeyError: #if no ImprovedBallistic key found on weapon (Custom Bundle assumes true if not present)
            print('No ImprovedBallistic key found on weapon, defaulting to true')
            try:
               weapon_stability_damage = (data['Instability'] + data['Modes']['Instability']) * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
               print('Stability dam ' + str(weapon_stability_damage))
               current_row.append(weapon_stability_damage)
            except (KeyError, IndexError, TypeError) as e:
               print('No modes or no other mode related key, trying another combo')
               try:
                  weapon_stability_damage = data['Instability'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                  print('Stability dam ' + str(weapon_stability_damage))
                  current_row.append(weapon_stability_damage)
               except (KeyError, IndexError) as e:
                  print('No modes, trying base values')
                  try:
                     weapon_stability_damage = data['Instability'] * data['ShotsWhenFired'] #stability damage = stability damage per shot * shotswhenfired
                     print('Stability dam ' + str(weapon_stability_damage))
                     current_row.append(weapon_stability_damage)
                  except KeyError:
                     print('No Stability damage key on this weapon!?')
                     current_row.append(0)

         ##weapon heat damage module
         try:
            weapon_heat_damage = (data['HeatDamage'] + data['Modes'][max_dam_mode]['HeatDamagePerShot']) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
            print('Heat dam ' + str(weapon_heat_damage))
            current_row.append(weapon_heat_damage)
         except (KeyError, IndexError) as e:
            print('Either no HeatDamagePerShot in modes, no ShotsWhenFired in modes, or no modes, checking other possibilities in modes')
            try:
               weapon_heat_damage = (data['HeatDamage'] + data['Modes'][max_dam_mode]['HeatDamagePerShot']) * data['ProjectilesPerShot'] * data['ShotsWhenFired']
               print('Heat dam ' + str(weapon_heat_damage))
               current_row.append(weapon_heat_damage)            
            except (KeyError, IndexError) as e:
               print('Either no HeatDamagePerShot in modes or no modes, checking other possibilities')                
               try:
                  weapon_heat_damage = data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired']) #heat damage = heat damage per shot * projectilespershot
                  print('Heat dam' + str(weapon_heat_damage))
                  current_row.append(weapon_heat_damage)
               except KeyError:
                  print('No heat damage key on this weapon!?')
                  current_row.append(0)

         #Weapon most heat damage ammotype damage value module
         try:
            current_row.append(ammotype_heatdam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
         except KeyError:
            print('Weapon has no ammo')
            current_row.append('N/A')

         #Weapon most heat damage ammotype module
         try:
            if ammotype_heatdam_dict[data['AmmoCategory']] == 0:
               current_row.append('N/A')
               print('Weapon ammo has no heat damage variant')
            else:
               pattern = '\w*.json'
               match_var = re.search(pattern,ammotype_heatdam_best_dict[data['AmmoCategory']])
               current_row.append(match_var.group()[:-5])
               print('Best ammo is ' + match_var.group()[:-5])
         except (KeyError, TypeError) as e:
            traceback.print_exc()
            current_row.append('N/A')
            print('Weapon has no ammo category')
         except AttributeError:
            traceback.print_exc()
            if ammotype_heatdam_dict[data['AmmoCategory']] == 0:
               current_row.append('N/A')
               print('Weapon ammo has no heat damage variant')
            else:   
               current_row.append(ammotype_heatdam_best_dict[data['AmmoCategory']])   

         ##weapon firing heat module
         try:
            weapon_firing_heat = data['HeatGenerated'] + data['Modes'][max_dam_mode]['HeatGenerated']
            print('HeatGenerated1 ' + str(weapon_firing_heat))
            current_row.append(weapon_firing_heat)
         except (KeyError, IndexError) as e:
            print('No modes, using base values')
            try:
               weapon_firing_heat = data['HeatGenerated']
               print('No firing heat in modes, defaulting to base ', 'Firing Heat ' + str(weapon_firing_heat))
               current_row.append(weapon_firing_heat)
            except KeyError:
               print('No weapon firing heat key on this weapon')
               current_row.append(0)

         ##Weapon jamming chance module
         try:
            weapon_flat_jam = 0
            weapon_flat_jam = data['FlatJammingChance'] #FlatJammingChance is handled backwards to ShotsWhenFired. Most mode weapons don't have a base FlatJammingChance key and ONLY have them in the modes. Check for base FIRST then check for modes based on that.
            try:
               weapon_flat_jam = (data['FlatJammingChance'] + data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)  
               print('Flat jamming chance ' + str(weapon_flat_jam))
            except (KeyError, IndexError) as e:
               weapon_flat_jam = (data['FlatJammingChance'] * 100)
               print('No modes, reverting to base jam chance ' + str(weapon_flat_jam) + '%')
         except KeyError:
            try:
               weapon_flat_jam = (data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)
               print('No base flat jamming chance key, using modes ' + str(weapon_flat_jam) + '%')
            except (KeyError, IndexError) as e:
               try:
                  pattern = '^wr-jam_chance_multiplier-[0-9]+'
                  for i in data['ComponentTags']['items']:
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
         current_row.append(weapon_flat_jam)

         #weapon can misfire module
         try:
            weapon_misfire = 'False'
            weapon_misfire = str(data['DamageOnJamming'])
            try:
               weapon_misfire = str(data['Modes'][max_dam_mode]['DamageOnJamming'])
            except KeyError:
               print('Weapon has no modes, or no base, checking for modes')
         except KeyError:
            try:
               weapon_misfire = str(data['Modes'][max_dam_mode]['DamageOnJamming'])
            except (KeyError, IndexError) as e:
               print('Weapon has no modes, checking ComponentTags for wr tags')
               try:
                  if 'wr-damage_when_jam' in data['ComponentTags']['items']:
                     weapon_misfire = 'True'
               except KeyError:
                  print('No jamming on this weapon')
         if weapon_misfire == 'False':
            try:
               for i in data['Custom']['BonusDescriptions']['Bonuses']:
                  if 'Explodium' in i: #this verifies that the weapon descriptions do not list misfires when traits do not have them
                     excepted_files.append(item)
            except KeyError:
               print('No Custom categories or BonusDescriptions')
         current_row.append(weapon_misfire)

         #damage compare modules
         try:
            weapon_damage_per_heat = float("{:.2f}".format(float(weapon_damage + weapon_damage_AOE)/(float(weapon_firing_heat))))    
            print(weapon_damage_per_heat)
            current_row.append(weapon_damage_per_heat)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_slot = float("{:.2f}".format(float(weapon_damage + weapon_damage_AOE)/(float(weapon_slots))))
            print(weapon_damage_per_slot)
            current_row.append(weapon_damage_per_slot)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_ton = float("{:.2f}".format(float(weapon_damage + weapon_damage_AOE)/(float(weapon_tonnage))))
            print(weapon_damage_per_ton)
            current_row.append(weapon_damage_per_ton)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         #Standard crit module against location
         #In english (base crit from RTCore/GameConstants.json of 0.5 overwritten by AIM to 0.56)
	      #0.56 * weapon crit chance * gear crit chance * ammo crit chance * target crit bonuses/penalties
         #does NOT take into account 
         try:
            weapon_base_crit = (0.56 * data['CriticalChanceMultiplier']) * 100
            current_row.append(data['CriticalChanceMultiplier'])
            current_row.append(weapon_base_crit)
         except KeyError:
            print('No CriticalChanceMultiplier on this weapon')
            current_row.append(0)
            current_row.append(0)

         #TAC module
         #to get a comparable baseline for all weapons we will compare (1 + (1 - half APMaxArmorThickness/APMaxArmorThickness) * (weapon APArmorShardsMod)) Add column for TAC and TAC max armor, TAC chance will be based on 50% of max AP armor for every weapon.
         #APShardsMod = (1 + (1 - half APMaxArmorThickness/APMaxArmorThickness) * (weapon APArmorShardsMod))
         #APThicknessMod = (1.0 - half APMaxArmorThickness/weapon APMaxArmorThickness) This will always be 0.5!
         #weapon ap crit mod = weapon.APCriticalChanceMultiplier (if weapon.APCriticalChanceMultiplier = 0, weapon ap crit mod set to 1.0)
         #final TAC chance = basic crit chance (0.1) * APShardsMod * APThicknessMod * weapon ap crit mod
         try:
            weapon_AP_crit_chance_multiplier = data['APCriticalChanceMultiplier']
            weapon_max_AP_thickness = data['APMaxArmorThickness']
            AP_shards_mod = (1 + (1 - 0.5)) * (data['APArmorShardsMod'])#hard coded to equal armor value of half of APMaxArmorThickness
            AP_thickness_mod = 0.5 #hard coded value to represent percentage of APMaxArmorThickness remaining on target, this checks at 50%
            weapon_TAC = float("{:0.6f}".format(0.1 * AP_shards_mod * AP_thickness_mod * weapon_AP_crit_chance_multiplier))
            print('90% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.9) * weapon_AP_crit_chance_multiplier)))
            print('80% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.8) * weapon_AP_crit_chance_multiplier)))
            print('70% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.7) * weapon_AP_crit_chance_multiplier)))
            print('60% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.6) * weapon_AP_crit_chance_multiplier)))
            print('50% ', weapon_TAC, ' = 0.1 * ', AP_shards_mod, ' * ', AP_thickness_mod, ' * ', weapon_AP_crit_chance_multiplier)
            print('40% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.4) * weapon_AP_crit_chance_multiplier)))
            print('30% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.3) * weapon_AP_crit_chance_multiplier)))
            print('20% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.2) * weapon_AP_crit_chance_multiplier)))
            print('10% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.1) * weapon_AP_crit_chance_multiplier)))
            print('00% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.0) * weapon_AP_crit_chance_multiplier)))
            current_row.append(weapon_TAC)
            current_row.append(weapon_max_AP_thickness)
         except KeyError:
            print('TAC KeyError, checking using default APCriticalChanceMultiplier')
            try:
               weapon_AP_crit_chance_multiplier = 1.0
               weapon_max_AP_thickness = data['APMaxArmorThickness']
               AP_shards_mod = (1 + (1 - 0.5)) * (data['APArmorShardsMod'])#hard coded to equal armor value of half of APMaxArmorThickness
               AP_thickness_mod = 0.5 #hard coded value to represent percentage of APMaxArmorThickness remaining on target, this checks at 50%
               weapon_TAC = float("{:0.6f}".format(0.1 * AP_shards_mod * AP_thickness_mod * weapon_AP_crit_chance_multiplier))
               print('90% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.9) * weapon_AP_crit_chance_multiplier)))
               print('80% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.8) * weapon_AP_crit_chance_multiplier)))
               print('70% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.7) * weapon_AP_crit_chance_multiplier)))
               print('60% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.6) * weapon_AP_crit_chance_multiplier)))
               print('50% ', weapon_TAC, ' = 0.1 * ', AP_shards_mod, ' * ', AP_thickness_mod, ' * ', weapon_AP_crit_chance_multiplier)
               print('40% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.4) * weapon_AP_crit_chance_multiplier)))
               print('30% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.3) * weapon_AP_crit_chance_multiplier)))
               print('20% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.2) * weapon_AP_crit_chance_multiplier)))
               print('10% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.1) * weapon_AP_crit_chance_multiplier)))
               print('00% ', float("{:0.6f}".format(0.1 * AP_shards_mod * (1 - 0.0) * weapon_AP_crit_chance_multiplier)))
               current_row.append(weapon_TAC)
               current_row.append(weapon_max_AP_thickness)
            except KeyError:
               print('No TAC on this weapon')
               current_row.append(0)
               current_row.append(0)

         #Accuracy bonus module, negative is better
         try:
            weapon_accuracy_mod = data['AccuracyModifier']
            print(weapon_accuracy_mod)
         except KeyError:
            print('Missing Base Accuracy Type')
            weapon_accuracy_mod = 0
         current_row.append(weapon_accuracy_mod)

         #Evasion ignore module, positive is better
         try:
            weapon_evasion_ignore = data['EvasivePipsIgnored']
            print(weapon_evasion_ignore)
         except KeyError:
            print('Missing Base Accuracy Type')
            weapon_evasion_ignore = 0
         current_row.append(weapon_evasion_ignore)

         #Weapon range module
         try:
            weapon_range_min = data['MinRange']
            current_row.append(weapon_range_min)
         except KeyError:
            print('No minimum range on this weapon')
         
         try:
            weapon_range_short = data['RangeSplit'][0]
            current_row.append(weapon_range_short)
         except KeyError:
            print('No short range on this weapon')
         
         try:
            weapon_range_medium = data['RangeSplit'][1]
            current_row.append(weapon_range_medium)
         except KeyError:
            print('No medium range on this weapon')

         try:
            weapon_range_long = data['RangeSplit'][2]
            current_row.append(weapon_range_long)
         except KeyError:
            print('No long range on this weapon')

         try:
            weapon_range_max = data['MaxRange']
            current_row.append(weapon_range_max)
         except KeyError:
            print('No max range on this weapon')         
         print('Min ' + str(weapon_range_min)  + ' Short ' + str(weapon_range_short) + ' Medium ' + str(weapon_range_medium) + ' Long ' + str(weapon_range_long) + ' Max ' + str(weapon_range_max))

         #Damage variance field module
         try:
            weapon_distance_variance = data['DistantVariance'] * 100
         except KeyError:
            print('No Distance Variance on weapon')
            weapon_distance_variance = 0
         current_row.append(weapon_distance_variance)

         #damage variance calculation module
         range_list = [weapon_range_min, weapon_range_short, weapon_range_medium, weapon_range_long, weapon_range_max]
         range_falloff_ratio_list = [0,0,0,0,0]
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
                              current_row.append(float("{:.2f}".format(weapon_damage * (1.0 - range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))))
                              print('Adding damage')
                           j += 1
                  #reversed tree               
                  elif data['DistantVarianceReversed'] == True:
                     print('Reversed Distance Variance')
                     try:
                        if data['DamageFalloffStartDistance'] > 1/1000:
                           falloff_start = data['DamageFalloffStartDistance']
                        else:
                           print('Falloff start value is zero, using minimum value')
                           falloff_start = weapon_range_min
                     except KeyError:
                        print('No falloff start distance key, using minimum value')
                        falloff_start = weapon_range_min                     
                     try:
                        if data['DamageFalloffEndDistance'] < falloff_start:
                           falloff_end = weapon_range_medium
                        else:
                           falloff_end = data['DamageFalloffEndDistance']
                        print('Falloff start ', falloff_start,'Falloff end ', falloff_end)
                     except KeyError:
                        print('No falloff end distance, using max value')
                        falloff_end = weapon_range_max
                     ##GET RATIO
                     j = 0
                     for i in range_list:
                        if (i <= falloff_end and falloff_end - falloff_start > 1/1000):
                           range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start))
                     ##DEFAULT
                        if i < falloff_start:
                           print('Range has no damage falloff')
                           current_row.append(weapon_damage)
                        else: #DO THE THING                  
                           current_row.append(float("{:.2f}".format(weapon_damage * (data['DistantVariance'] + range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))))
                           print('Adding reversed damage')
                        j += 1
               except KeyError:
                  print('No DistantVarianceReversed key on weapon!')
                  for i in range(5):
                     current_row.append(weapon_damage)
         except KeyError:
            print('No damage variance, using normal values')
            for i in range(5):
               current_row.append(weapon_damage)


         #l.insert(newindex, l.pop(oldindex))
         current_row.insert(9,current_row.pop(3)) #this rearranges the current_row list to properly format it for the excel sheet; this should go bye bye in next version, just use variables and append them all at the end man!

         df2 = pandas.DataFrame([current_row], columns=columns_list)
         print(df2)
         df = df.append(df2)
      except UnicodeDecodeError:
         excepted_files.append(item)
         print('Possible invalid character in JSON')
      except json.decoder.JSONDecodeError:
         possible_invalid_jsons.append(item)
         print('Possible invalid JSON!')

#AMS Modules
for item in ams_file_list:
   with open(item) as f:
      print(item)
      try: 
         data = json.load(f)
         current_row_ams = []
         #Initializing all loop variables in so any unused do not throw off row alignment by being empty
         basemode_ams_damage = 'N/A'
         basemode_ams_hitchance = 'N/A'
         basemode_ams_shots = 'N/A'
         basemode_ams_avg_damage = 'N/A'
         basemode_ams_heat = 'N/A'
         basemode_ams_jam = 'N/A'
         basemode_ams_maxrange = 'N/A'
         basemode_aams = 'N/A'
         olmode_ams_damage = 'N/A'
         olmode_ams_hitchance = 'N/A'
         olmode_ams_shots = 'N/A'
         olmode_ams_avg_damage = 'N/A'
         olmode_ams_heat = 'N/A'
         olmode_ams_jam = 'N/A'
         olmode_ams_maxrange = 'N/A'
         olmode_aams = 'N/A'
         fpmode_ams_damage = 'N/A'
         fpmode_ams_hitchance = 'N/A'
         fpmode_ams_shots = 'N/A'
         fpmode_ams_avg_damage = 'N/A'
         fpmode_ams_heat = 'N/A'
         fpmode_ams_jam = 'N/A'
         fpmode_ams_maxrange = 'N/A'
         fpmode_aams = 'N/A'

         #AMS hardpoint module
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
         current_row_ams.append(hardpoint_type)

         #AMS type module
         try:
            weapon_class = str(data['Type'])
            print(weapon_class)
            current_row_ams.append(weapon_class)
         except KeyError:
            print('Missing Weapon Type')
            current_row_ams.append('N/A')
         
         #AMS name module
         try:
            if 'deprecated' in str(data['Description']['UIName']).lower():
               print('Deprecated in name, skipping')
               filtered_files.append(item)
               continue
            weapon_name = str(data['Description']['UIName'])
            print(weapon_name)
            current_row_ams.append(weapon_name)
         except KeyError:
            print('Missing Weapon Name')
            current_row_ams.append('N/A')

         #AMS Tonnage check module
         if hardpoint_type == 'Special':
            weapon_tonnage = data['Custom']['HandHeld']['Tonnage']
            current_row_ams.append(weapon_tonnage)
         elif hardpoint_type == 'SpecialMelee':
            weapon_tonnage = data['Custom']['HandHeld']['Tonnage']
            current_row_ams.append(weapon_tonnage)
         else:
            try:
               weapon_tonnage = data['Tonnage']
               print('Tons ' + str(weapon_tonnage))
               current_row_ams.append(weapon_tonnage)
               if weapon_tonnage > 50: #this filters deprecated weapons that are 100 to 6666 tons
                  print('Filtered out deprecated weapon by tonnage')
                  filtered_files.append(item)
                  continue
            except:
               print('Missing Tonnage')
               current_row_ams.append('N/A')

         #AMS slot size module
         try:
            weapon_slots = data['InventorySize']
            print('Slots ' + str(weapon_slots))
            current_row_ams.append(weapon_slots)
         except:
            print('Missing Weapon Slots')
            current_row_ams.append('N/A')

         #AMS multi attack module
         try:
            if data['AMSShootsEveryAttack']:
               current_row_ams.append('True')
            else:
               current_row_ams.append('False')               
         except KeyError:
            current_row_ams.append('False')

         #AMS modes everything module
         try:
            for i in range(len(data['Modes'])):
               print(i)
               is_AMS = False
               try:
                  if data['Modes'][i]['IsAMS'] or data['IsAMS']:
                     print('This mode or base is isAMS')
                     is_AMS = 'True'
               except KeyError:
                  print('Missing isAMS key in either modes or base, checking base now')
                  try:
                     if data['IsAMS']:
                        print('Base isAMS')
                        is_AMS = 'True'
                  except KeyError:
                     print('Missing isAMS key in both modes and base; either this is not an AMS or this mode is not an AMS')
                     continue
         #base mode check
               if is_AMS and data['Modes'][i]['isBaseMode'] and data['Modes'][i]['Id'] != 'Off' and data['Modes'][i]['Id'] != 'MG' and data['Modes'][i]['Id'] != 'Laser':
                  print('This is the AMS base mode')
                  basemode_ams_damage = 0
                  try:
                     basemode_ams_damage = data['Modes'][i]['AMSDamage'] + data['AMSDamage'] + 1
                     print('Basemode AMS damage is ',str(basemode_ams_damage))
                  except KeyError:
                     try:
                        basemode_ams_damage = data['Modes'][i]['AMSDamage'] + 1
                     except KeyError:                        
                        try:
                           print('No Mode AMS Damage, trying base')
                           basemode_ams_damage = data['AMSDamage'] + 1
                           print('Basemode AMS damage is ', str(basemode_ams_damage))
                        except KeyError:
                           print('No mode or base AMS Damage, defaulting to 1')
                           basemode_ams_damage = 1
                  
                  basemode_ams_hitchance = 0
                  try:
                     basemode_ams_hitchance = data['Modes'][i]['AMSHitChance']
                     print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
                  except KeyError:
                     print('No AMS Hitchance in mode, checking base')
                     try:
                        basemode_ams_hitchance = data['AMSHitChance']
                        print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
                     except KeyError:
                        print('No AMS Hitchance at all!?')

                  basemode_ams_shots = 0
                  try:
                     basemode_ams_shots = data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired']
                     print('Basemode AMS ShotsWhenFired is ', str(basemode_ams_shots))
                  except KeyError:
                     print('No ShotsWhenFired in mode or base, checking bas only')
                     try:
                        basemode_ams_shots = data['ShotsWhenFired']
                        print(' AMS ShotsWhenFired is ', str(basemode_ams_shots))
                     except KeyError:
                        print('No ShotsWhenFired at all?')

                  basemode_ams_avg_damage = 0
                  try:
                     basemode_ams_avg_damage = basemode_ams_damage * basemode_ams_shots * basemode_ams_hitchance
                     print('Basemode AMS average damage is ', str(basemode_ams_avg_damage))
                  except:
                     traceback.print_exc()
                     print('This should not be reachable! AMS avg damage error.')
                  
                  basemode_ams_heat = 0
                  try:
                     basemode_ams_heat = data['Modes'][i]['HeatGenerated'] + data['HeatGenerated']
                     print('Basemode AMS heat is ', str(basemode_ams_heat))
                  except KeyError:
                     print('No heat in modes or base, trying base.')
                     try:
                        basemode_ams_heat = data['HeatGenerated']
                        print('AMS heat is ', str(basemode_ams_heat))
                     except KeyError:
                        print('No heat on AMS, defaulting to 0')

                  basemode_ams_jam = 0
                  try:
                     basemode_ams_jam =  data['FlatJammingChance'] * 100
                     try:
                        basemode_ams_jam = (data['Modes'][i]['FlatJammingChance'] + data['FlatJammingChance']) * 100
                        print('Basemode AMS jam chance is ', str(basemode_ams_jam))
                     except KeyError:
                        print('No mode jam chance, using base')
                  except KeyError:
                     print('No base jam chance, checking modes')
                     try:
                        basemode_ams_jam = data['Modes'][i]['FlatJammingChance'] * 100
                        print('Basemode AMS jam chance is ', str(basemode_ams_jam))
                     except KeyError:
                        print('No jam chance on AMS, using zero')

                  basemode_ams_maxrange = 0   
                  try:
                     basemode_ams_maxrange = data['MaxRange'] + data['Modes'][i]['MaxRange']
                     print('Basemode AMS max range is ', str(basemode_ams_maxrange))
                  except KeyError:
                     print('No range boost in either base or mode, trying base value')
                     try:
                        basemode_ams_maxrange = data['MaxRange']
                        print('Basemode AMS max range is ', str(basemode_ams_maxrange))
                     except KeyError:
                        print('No range in base values, checking only mode')
                        basemode_ams_maxrange = data['Modes'][i]['MaxRange']
                        print('Basemode AMS max range is ', str(basemode_ams_maxrange))

                  basemode_aams = 'False'
                  try:
                     print(data['Modes'][i]['IsAAMS'])
                     if data['Modes'][i]['IsAAMS']:
                        print('This is an Advanced AMS and will protect allies')
                        basemode_aams = 'True'
                  except KeyError:
                     print('No isAAMS tag present in modes, trying base')
                     try:
                        print(data['IsAAMS'])
                        if data['IsAAMS']:
                           print('This is an Advanced AMS and will protect allies')
                           basemode_aams = 'True'
                     except KeyError:
                        print('This is not an advanced AMS and will not protect allies in this mode')
                        basemode_aams = 'False'
               elif is_AMS and data['Modes'][i]['Id'] == 'Overload': #Overload mode
                  print('This is Overload Mode')
                  olmode_ams_damage = 0
                  try:
                     olmode_ams_damage = data['Modes'][i]['AMSDamage'] + data['AMSDamage'] + 1
                     print('Overload AMS damage is ',str(olmode_ams_damage))
                  except KeyError:
                     try:
                        olmode_ams_damage = data['Modes'][i]['AMSDamage'] + 1
                     except KeyError:
                        try:
                           print('No Mode AMS Damage, trying base')
                           olmode_ams_damage = data['AMSDamage'] + 1
                           print('Overload AMS damage is ', str(olmode_ams_damage))
                        except KeyError:
                           print('No mode or base AMS Damage, defaulting to 1')
                           olmode_ams_damage = 1
                  
                  olmode_ams_hitchance = 0
                  try:
                     olmode_ams_hitchance = data['Modes'][i]['AMSHitChance']
                     print('Overload AMS hitchance is ', str(olmode_ams_hitchance))
                  except KeyError:
                     print('No AMS Hitchance in mode, checking base')
                     try:
                        olmode_ams_hitchance = data['AMSHitChance']
                        print('Overload AMS hitchance is ', str(olmode_ams_hitchance))
                     except KeyError:
                        print('No AMS Hitchance at all!?')

                  olmode_ams_shots = 0
                  try:
                     olmode_ams_shots = data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired']
                     print('Overload AMS ShotsWhenFired is ', str(olmode_ams_shots))
                  except KeyError:
                     print('No ShotsWhenFired in mode or base, checking bas only')
                     try:
                        olmode_ams_shots = data['ShotsWhenFired']
                        print('Overload AMS ShotsWhenFired is ', str(olmode_ams_shots))
                     except KeyError:
                        print('No ShotsWhenFired at all?')

                  olmode_ams_avg_damage = 0
                  try:
                     olmode_ams_avg_damage = olmode_ams_damage * olmode_ams_shots * olmode_ams_hitchance
                     print('Overload AMS average damage is ', str(olmode_ams_avg_damage))
                  except:
                     traceback.print_exc()
                     print('This should not be reachable! AMS avg damage error.')
                  
                  olmode_ams_heat = 0
                  try:
                     olmode_ams_heat = data['Modes'][i]['HeatGenerated'] + data['HeatGenerated']
                     print('Overload AMS heat is ', str(olmode_ams_heat))
                  except KeyError:
                     print('No heat in modes or base, trying base.')
                     try:
                        olmode_ams_heat = data['HeatGenerated']
                        print('Overload AMS heat is ', str(olmode_ams_heat))
                     except KeyError:
                        print('No heat on AMS, defaulting to 0')

                  olmode_ams_jam = 0
                  try:
                     olmode_ams_jam =  data['FlatJammingChance'] * 100
                     try:
                        olmode_ams_jam = (data['Modes'][i]['FlatJammingChance'] + data['FlatJammingChance']) * 100
                        print('Overload AMS jam chance is ', str(olmode_ams_jam))
                     except KeyError:
                        print('No mode jam chance, using base')
                  except KeyError:
                     print('No base jam chance, checking modes')
                     try:
                        olmode_ams_jam = data['Modes'][i]['FlatJammingChance'] * 100
                        print('Overload AMS jam chance is ', str(olmode_ams_jam))
                     except KeyError:
                        print('No jam chance on AMS, using zero')

                  olmode_ams_maxrange = 0   
                  try:
                     olmode_ams_maxrange = data['MaxRange'] + data['Modes'][i]['MaxRange']
                     print('Overload AMS max range is ', str(olmode_ams_maxrange))
                  except KeyError:
                     print('No range boost in either base or mode, trying base value')
                     try:
                        olmode_ams_maxrange = data['MaxRange']
                        print('Overload AMS max range is ', str(olmode_ams_maxrange))
                     except KeyError:
                        print('No range in base values, checking only mode')
                        olmode_ams_maxrange = data['Modes'][i]['MaxRange']
                        print('Overload AMS max range is ', str(olmode_ams_maxrange))

                  olmode_aams = 'False'
                  try:
                     print(data['Modes'][i]['IsAAMS'])
                     if data['Modes'][i]['IsAAMS']:
                        print('This is an Advanced AMS and will protect allies')
                        olmode_aams = 'True'
                  except KeyError:
                     print('No isAAMS tag present in modes, trying base')
                     try:
                        print(data['IsAAMS'])
                        if data['IsAAMS']:
                           print('This is an Advanced AMS and will protect allies')
                           olmode_aams = 'True'
                     except KeyError:
                        print('This is not an advanced AMS and will not protect allies in this mode')
                        olmode_aams = 'False'

               elif is_AMS and data['Modes'][i]['Id'] == 'FullPower': #FullPower mode for Clan Advanced LAMS only
                  print('This is FullPower Mode')
                  try:
                     fpmode_ams_damage = data['Modes'][i]['AMSDamage'] + data['AMSDamage'] + 1
                     print('FullPower AMS damage is ',str(fpmode_ams_damage))
                  except KeyError:
                     try:
                        fpmode_ams_damage = data['Modes'][i]['AMSDamage'] + 1
                     except KeyError:  
                        try:
                           print('No Mode AMS Damage, trying base')
                           fpmode_ams_damage = data['AMSDamage'] + 1
                           print('FullPower AMS damage is ', str(fpmode_ams_damage))
                        except KeyError:
                           print('No mode or base AMS Damage, defaulting to 1')
                           fpmode_ams_damage = 1
                  
                  fpmode_ams_hitchance = 0
                  try:
                     fpmode_ams_hitchance = data['Modes'][i]['AMSHitChance']
                     print('FullPower AMS hitchance is ', str(fpmode_ams_hitchance))
                  except KeyError:
                     print('No AMS Hitchance in mode, checking base')
                     try:
                        fpmode_ams_hitchance = data['AMSHitChance']
                        print('FullPower AMS hitchance is ', str(fpmode_ams_hitchance))
                     except KeyError:
                        print('No AMS Hitchance at all!?')

                  fpmode_ams_shots = 0
                  try:
                     fpmode_ams_shots = data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired']
                     print('FullPower AMS ShotsWhenFired is ', str(fpmode_ams_shots))
                  except KeyError:
                     print('No ShotsWhenFired in mode or base, checking bas only')
                     try:
                        fpmode_ams_shots = data['ShotsWhenFired']
                        print('FullPower AMS ShotsWhenFired is ', str(fpmode_ams_shots))
                     except KeyError:
                        print('No ShotsWhenFired at all?')

                  fpmode_ams_avg_damage = 0
                  try:
                     fpmode_ams_avg_damage = fpmode_ams_damage * fpmode_ams_shots * fpmode_ams_hitchance
                     print('FullPower AMS average damage is ', str(fpmode_ams_avg_damage))
                  except:
                     traceback.print_exc()
                     print('This should not be reachable! AMS avg damage error.')
                  
                  fpmode_ams_heat = 0
                  try:
                     fpmode_ams_heat = data['Modes'][i]['HeatGenerated'] + data['HeatGenerated']
                     print('FullPower AMS heat is ', str(fpmode_ams_heat))
                  except KeyError:
                     print('No heat in modes or base, trying base.')
                     try:
                        fpmode_ams_heat = data['HeatGenerated']
                        print('FullPower AMS heat is ', str(fpmode_ams_heat))
                     except KeyError:
                        print('No heat on AMS, defaulting to 0')

                  fpmode_ams_jam = 0
                  try:
                     fpmode_ams_jam =  data['FlatJammingChance'] * 100
                     try:
                        fpmode_ams_jam = (data['Modes'][i]['FlatJammingChance'] + data['FlatJammingChance']) * 100
                        print('FullPower AMS jam chance is ', str(fpmode_ams_jam))
                     except KeyError:
                        print('No mode jam chance, using base')
                  except KeyError:
                     print('No base jam chance, checking modes')
                     try:
                        fpmode_ams_jam = data['Modes'][i]['FlatJammingChance'] * 100
                        print('FullPower AMS jam chance is ', str(fpmode_ams_jam))
                     except KeyError:
                        print('No jam chance on AMS, using zero')

                  fpmode_ams_maxrange = 0   
                  try:
                     fpmode_ams_maxrange = data['MaxRange'] + data['Modes'][i]['MaxRange']
                     print('FullPower AMS max range is ', str(fpmode_ams_maxrange))
                  except KeyError:
                     print('No range boost in either base or mode, trying base value')
                     try:
                        fpmode_ams_maxrange = data['MaxRange']
                        print('FullPower AMS max range is ', str(fpmode_ams_maxrange))
                     except KeyError:
                        print('No range in base values, checking only mode')
                        fpmode_ams_maxrange = data['Modes'][i]['MaxRange']
                        print('Overload AMS max range is ', str(fpmode_ams_maxrange))

                  fpmode_aams = 'False'
                  try:
                     if data['Modes'][i]['IsAAMS']:
                        print('This is an Advanced AMS and will protect allies')
                        fpmode_aams = 'True'
                  except KeyError:
                     print('No isAAMS tag present in modes, trying base')
                     try:
                        if data['IsAAMS']:
                           print('This is an Advanced AMS and will protect allies')
                           fpmode_aams = 'True'
                     except KeyError:
                        print('This is not an advanced AMS and will not protect allies in this mode')
                        fpmode_aams = 'False'
               else:
                  print('Not an AMS mode, skipping')
                  continue
         except KeyError:
            print('AMS has no modes, trying base values')
            traceback.print_exc()
            basemode_ams_damage = 0
            try:
               print('No Mode AMS Damage, trying base')
               basemode_ams_damage = data['AMSDamage'] + 1
               print('Basemode AMS damage is ', str(basemode_ams_damage))
            except KeyError:
               print('No mode or base AMS Damage, defaulting to 1')
               basemode_ams_damage = 1
            
            basemode_ams_hitchance = 0
            try:
               basemode_ams_hitchance = data['AMSHitChance']
               print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
            except KeyError:
               print('No AMS Hitchance at all!?')

            basemode_ams_shots = 0
            try:
               basemode_ams_shots = data['ShotsWhenFired']
               print(' AMS ShotsWhenFired is ', str(basemode_ams_shots))
            except KeyError:
               print('No ShotsWhenFired at all?')

            basemode_ams_avg_damage = 0
            try:
               basemode_ams_avg_damage = basemode_ams_damage * basemode_ams_shots * basemode_ams_hitchance
               print('Basemode AMS average damage is ', str(basemode_ams_avg_damage))
            except:
               traceback.print_exc()
               print('This should not be reachable! AMS avg damage error.')
            
            basemode_ams_heat = 0
            try:
               basemode_ams_heat = data['HeatGenerated']
               print('AMS heat is ', str(basemode_ams_heat))
            except KeyError:
               print('No heat on AMS, defaulting to 0')

            basemode_ams_jam = 0
            try:
               basemode_ams_jam =  data['FlatJammingChance'] * 100
            except KeyError:
               print('No base jam chance, defaulting to zero')

            basemode_ams_maxrange = 0
            try:
               basemode_ams_maxrange = data['MaxRange']
               print('Basemode AMS max range is ', str(basemode_ams_maxrange))
            except KeyError:
               print('No range on AMS, this thing is useless?')
   
            basemode_aams = 'False'
            try:
               print(data['IsAAMS'])
               if data['IsAAMS']:
                  print('This is an Advanced AMS and will protect allies')
                  basemode_aams = 'True'
               else:
                  print('This is not an advanced AMS and will not protect allies in this mode')
                  basemode_aams = 'False'
            except KeyError:
               print('No isAAMS tag present, this is not an advanced AMS and will not protect allies in this mode')
               basemode_aams = 'False'

         current_row_ams.append(basemode_ams_damage)
         current_row_ams.append(basemode_ams_avg_damage)
         try:
            current_row_ams.append(basemode_ams_damage * basemode_ams_shots)
         except TypeError:
            current_row_ams.append('N/A')
         current_row_ams.append(basemode_ams_shots)
         current_row_ams.append(basemode_ams_hitchance)
         current_row_ams.append(basemode_ams_heat)
         current_row_ams.append(basemode_ams_jam)
         current_row_ams.append(basemode_ams_maxrange)
         current_row_ams.append(basemode_aams)
         current_row_ams.append(olmode_ams_damage)
         current_row_ams.append(olmode_ams_avg_damage)
         try:
            current_row_ams.append(olmode_ams_damage * olmode_ams_shots)
         except TypeError:
            current_row_ams.append('N/A')
         current_row_ams.append(olmode_ams_shots)
         current_row_ams.append(olmode_ams_hitchance)
         current_row_ams.append(olmode_ams_heat)
         current_row_ams.append(olmode_ams_jam)
         current_row_ams.append(olmode_ams_maxrange)
         current_row_ams.append(olmode_aams)
         current_row_ams.append(fpmode_ams_damage)
         current_row_ams.append(fpmode_ams_avg_damage)
         try:
            current_row_ams.append(fpmode_ams_damage * fpmode_ams_shots)
         except TypeError:
            current_row_ams.append('N/A')
         current_row_ams.append(fpmode_ams_shots)
         current_row_ams.append(fpmode_ams_hitchance)
         current_row_ams.append(fpmode_ams_heat)
         current_row_ams.append(fpmode_ams_jam)
         current_row_ams.append(fpmode_ams_maxrange)
         current_row_ams.append(fpmode_aams)

         if len(current_row_ams) < 33:
            for i in range(33 - len(current_row_ams)):
               current_row_ams.append('???')
         print(current_row_ams)
         ams_df2 = pandas.DataFrame([current_row_ams], columns=ams_columns_list)
         print(ams_df2)
         ams_df = ams_df.append(ams_df2)

      except UnicodeDecodeError:
         excepted_files.append(item)
         print('Possible invalid character in JSON')
      except json.decoder.JSONDecodeError:
         possible_invalid_jsons.append(item)
         print('Possible invalid JSON!')
##End of the JSON.load() try statement from line 242
      
#These are used to write filenames of different types of excepted files to separate text files for analyzation later
#For tracking all files filtered from exclusion list and other filter checks
with open("filtered files.txt", "w") as output:
   for item in filtered_files:
       output.write(str(item) + '\n')
#For items that return a UnicodeDecodeError, most likely due to odd characters in the file.
with open("excepted files.txt", "w") as output:
   for item in excepted_files:
       output.write(str(item) + '\n')
#For items that return a JSONDecodeError, these are almost certainly an invalid or incorrectly formatted JSON file.
with open("possible invalid JSON.txt", "w") as output:
   for item in possible_invalid_jsons:
       output.write(str(item) + '\n')
##

#Writes the fully formed Pandas DataFrames to their respective sheets of the final spreadsheet file
with pandas.ExcelWriter('RT Weaponlist.xlsx') as writer:
   df.to_excel(writer,sheet_name='Weapons',index=False)
   ams_df.to_excel(writer,sheet_name='AMS',index=False)
print('Parsed in', time.time() - time1, 'seconds')