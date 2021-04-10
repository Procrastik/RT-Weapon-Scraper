##ToDo List
#add conditions and logging to capture all relevant metrics for weapons and verify JSONS/characters as a side effect
#add logic to iterate over modes to check for highest value of each 


import os
import json
import traceback
import pandas

#change location variable to point to root of install location you want to analize.
location = 'E:\Roguetech\RogueTech'
file_keyword_exclusion_list = ['Quirks', 'Melee', 'Special', 'Turret', 'Ambush']
weapon_file_list = []
excepted_files = []
possible_invalid_jsons = []
df = pandas.DataFrame(columns=['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire', 'Tonnage', 'Slots', 'Max Recoil', 'Max Damage', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage', 'Max Firing Heat', 'Max Jam Chance', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Minimum Range', 'Short Range', 'Medium Range', 'Long Range', 'Max Range'])
##

#This iterates through all of the 'location' path from top directory down looking for listed criteria in thr for loop and adds it to list weapon_file_list
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
               if i in item: #list any exclusions here?  Find a better way to do this against a list of exclusions?
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
         
         #output string
         try:
            hardpoint_type = data['Category']
            print(hardpoint_type)
            current_row.append(hardpoint_type)
         except KeyError:
            print('Missing Hardpoint Type')
            current_row.append('N/A')

         #output string
         try:
            weapon_class = data['Type']
            print(weapon_class)
            current_row.append(weapon_class)
         except KeyError:
            print('Missing Weapon Type')
            current_row.append('N/A')
         
         #output string
         try:
            weapon_name = data['Description']['UIName']
            print(weapon_name)
            current_row.append(weapon_name)
         except KeyError:
            print('Missing Weapon Name')
            current_row.append('N/A')

         #output string
         try:
            indirect_fire = str(data['IndirectFireCapable'])
            print('Can Indirectfire ' + ' ' + indirect_fire)
            current_row.append(indirect_fire)
         except KeyError:
            print('Missing Indirect Fire boolean')
            current_row.append('N/A')

         #output float
         try:
            weapon_tonnage = str(data['Tonnage'])
            print('Tons ' + weapon_tonnage)
            current_row.append(weapon_tonnage)
         except:
            print('Missing Tonnage')
            current_row.append('N/A')

         #output int
         try:
            weapon_slots = str(data['InventorySize'])
            print('Slots ' + weapon_slots)
            current_row.append(weapon_slots)
         except:
            print('Missing Weapon Slots')
            current_row.append('N/A')

         ##add logic to test which mode is has the highest refire! Output int
         try:
            weapon_recoil = str(data['RefireModifier'] + data['Modes'][-1]['RefireModifier'])
            print('Recoil ' + weapon_recoil)
            current_row.append(weapon_recoil)
         except (KeyError, IndexError) as e:
            try:
               weapon_recoil = str(data['RefireModifier'])
               print('No recoil in modes, defaulting to base', 'Recoil ' + weapon_recoil)
               current_row.append(weapon_recoil)
            except KeyError:
               print('No Refire Modifier on this weapon')
               current_row.append('N/A')

         ##add logic here to test which mode has the highest damage! output int
         try:
            weapon_damage = str(data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired'])) #damage = damage per shot * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes)
            print('Dam ' + weapon_damage)
            current_row.append(weapon_damage)
         except (KeyError, IndexError) as e:
            try:
               weapon_damage = str(data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])) #damage = damage per shot * projectilespershot
               print('No damage in modes, defaulting to base', 'Dam ' + weapon_damage)
               current_row.append(weapon_damage)
            except KeyError:
               print('No damage on this weapon!?')
               current_row.append('N/A')

         #output int
         try:
            weapon_damage_variance = str(data['DamageVariance'])
            print('Dam Var ' + weapon_damage_variance)
            current_row.append(weapon_damage_variance)
         except KeyError:
            print('No damage variance key!?')
            current_row.append('N/A')

         #output float
         try:
            weapon_stability_damage = str(data['Instability'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired'])) #stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
            print('Stability dam ' + weapon_stability_damage)
            current_row.append(weapon_stability_damage)
         except (KeyError, IndexError) as e:   
            try:
               weapon_stability_damage = str(data['Instability'] * data['ShotsWhenFired']) #stability damage = stability damage per shot * shotswhenfired
               print('Stability dam ' + weapon_stability_damage)
               current_row.append(weapon_stability_damage)
            except KeyError:
               print('No Stability damage key on this weapon!?')
               current_row.append('N/A')

         ##add logic here to test which mode has the highest heat damage! output int
         try:
            weapon_heat_damage = str(data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired'])) #heat damage = heat damage per shot * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes)
            print('Heat dam ' + weapon_heat_damage)
            current_row.append(weapon_heat_damage)
         except (KeyError, IndexError) as e:   
            try:
               weapon_heat_damage = str(data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'])) #heat damage = heat damage per shot * projectilespershot
               print('Heat dam' + weapon_heat_damage)
               current_row.append(weapon_heat_damage)
            except KeyError:
               print('No heat damage key on this weapon!?')
               current_row.append('N/A')

         ##add logic here to test which mode has the highest firing heat! output int
         try:
            weapon_firing_heat = str(data['HeatGenerated'] + data['Modes'][-1]['HeatGenerated'])
            print('Firing Heat ' + weapon_firing_heat)
            current_row.append(weapon_firing_heat)
         except (KeyError, IndexError) as e:
            try:
               weapon_firing_heat = str(data['HeatGenerated'])
               print('No firing heat in modes, defaulting to base ', 'Firing Heat ' + weapon_firing_heat)
               current_row.append(weapon_firing_heat)
            except KeyError:
               print('No weapon firing heat key on this weapon')
               current_row.append('N/A')

         ##add logic here to test which mode has the highest jamming chance! output float
         try:
            weapon_flat_jam = str(data['FlatJammingChance']) #FlatJammingChance is handled backwards to ShotsWhenFired. Most mode weapons don't have a base FlatJammingChance key and ONLY have them in the modes. Check for base FIRST then check for modes based on that.
            try:
               weapon_flat_jam = str((data['FlatJammingChance'] + data['Modes'][-1]['FlatJammingChance'] * 100))  
               print('Flat jamming chance ' + weapon_flat_jam)
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               weapon_flat_jam = str((data['FlatJammingChance'] * 100))
               print('No modes, reverting to base jam chance ' + weapon_flat_jam + '%')
               current_row.append(weapon_flat_jam)
         except KeyError:
            try:
               weapon_flat_jam = str((data['Modes'][-1]['FlatJammingChance'] * 100))
               print('No base flat jamming chance key, using modes ' + weapon_flat_jam + '%')
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               print('No flat jamming chance on this weapon.')
               current_row.append(0)

         try:
            weapon_damage_per_heat = str("{:.2f}".format(float(weapon_damage)/(float(weapon_firing_heat))))        
            print(weapon_damage_per_heat)
            current_row.append(weapon_damage_per_heat)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_slot = str("{:.2f}".format(float(weapon_damage)/(float(weapon_slots))))
            print(weapon_damage_per_slot)
            current_row.append(weapon_damage_per_slot)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_ton = str("{:.2f}".format(float(weapon_damage)/(float(weapon_tonnage))))
            print(weapon_damage_per_ton)
            current_row.append(weapon_damage_per_ton)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         #output int
         try:
            weapon_range_min = str(data['MinRange'])
            current_row.append(weapon_range_min)
         except KeyError:
            traceback.print_exc()
         
         try:
            weapon_range_short = str(data['RangeSplit'][0])
            current_row.append(weapon_range_short)
         except KeyError:
            traceback.print_exc()
         
         try:
            weapon_range_medium = str(data['RangeSplit'][1])
            current_row.append(weapon_range_medium)
         except KeyError:
            traceback.print_exc()

         try:
            weapon_range_long = str(data['RangeSplit'][2])
            current_row.append(weapon_range_long)
         except KeyError:
            traceback.print_exc()

         try:
            weapon_range_max = str(data['MaxRange'])
            current_row.append(weapon_range_max)
         except KeyError:
            traceback.print_exc()
         
         print('Min ' + weapon_range_min  + ' Short ' + weapon_range_short + ' Medium ' + weapon_range_medium + ' Long ' + weapon_range_long + ' Max ' + weapon_range_max)

         df2 = pandas.DataFrame([current_row], columns=(['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire', 'Tonnage', 'Slots', 'Max Recoil', 'Max Damage', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage', 'Max Firing Heat', 'Max Jam Chance', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Minimum Range', 'Short Range', 'Medium Range', 'Long Range', 'Max Range']))
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
df.to_excel('RT Weaponlist.xlsx',sheet_name='Weapons',float_format=':.2f')
# try:
         #   bonus_descriptions = ''
         #   for i in data['Custom']['BonusDescriptions']['Bonuses']:
         #      bonus_descriptions += i
         #   print(bonus_descriptions)
         #   bonus_descriptions = bonus_descriptions.join(bonus_descriptions)
         #   current_row.append(bonus_descriptions)
        # except (KeyError, IndexError) as e:
         #   print('No BonusDescriptions found.')   
         #   current_row.append('N/A')    

      #start of data frame constructor
      #print(current_row)

#use this to write to json without unicode errors? future use?
#with open('s1Results/map.json', 'wb') as f:
 #   jdata = json.dumps(r.json(), indent=4, ensure_ascii=False)
  #  f.write(jdata.encode())

# class pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)[source]¶

 #   Two-dimensional, size-mutable, potentially heterogeneous tabular data.

  #  Data structure also contains labeled axes (rows and columns). Arithmetic operations align on both row and column labels. Can be thought of as a dict-like container for Series objects. The primary pandas data structure.

   # Parameters

    #    datandarray (structured or homogeneous), Iterable, dict, or DataFrame

     #       Dict can contain Series, arrays, constants, dataclass or list-like objects. If data is a dict, column order follows insertion-order.

      #      Changed in version 0.25.0: If data is a list of dicts, column order follows insertion-order.
       # indexIndex or array-like
#
 #           Index to use for resulting frame. Will default to RangeIndex if no indexing information part of input data and no index provided.
  #      columnsIndex or array-like
#
 #           Column labels to use for resulting frame. Will default to RangeIndex (0, 1, 2, …, n) if no column labels are provided.
  #      dtypedtype, default None
#
 #           Data type to force. Only a single dtype is allowed. If None, infer.
  #      copybool, default False
#
 #           Copy data from inputs. Only affects DataFrame / 2d ndarray input.

#example df creation
#>>> df = pandas.DataFrame(data=None,index=['Medium Laser','Small Laser'],columns=['one','five'],dtype=None,copy=False)
#>>> print(df)
#              one five
#Medium Laser  NaN  NaN
#Small Laser   NaN  NaN
