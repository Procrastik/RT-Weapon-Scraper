##ToDo List
#add conditions and logging to capture all relevant metrics for weapons - Mostly Done - and it even verifies JSONS/invalid characters as a side effect!
#add logic to iterate over modes to check for highest value of each - Done for weapons (maybe should just capture the highest damage mode value of others because frankly we only care about damage, right!??)
#add checks in modes to indirectfire - DONE
#add checks for accuracy and evasion ignore (EvasivePipsIgnored and  AccuracyModifier)
#add max range damage falloff, or even better add damage expected at each range bracket (Weapon Heat/Damage/Stability falls off to {0} of starting value at long range)
#add mode accuracy bonuses/maluses


 #"DamageFalloffStartDistance": 0, - distance where damage starts to change, additive per ammo/mode/weapon.
 # "DamageFalloffEndDistance": 0, - distance where damage stops to change, additive per ammo/mode/weapon.
 # "DistantVariance": 0.3, - Distance damage variance addiditve per ammo/mode/weapon
 # "DistantVarianceReversed": false, - Set is distance damage variance is reversed (mode have priority, than ammo, than weapon)
 #"DistantVariance": 0.3, - Distance damage variance addiditve per ammo/mode/weapon
 # "DistantVarianceReversed": false, - Set is distance damage variance is reversed (mode have priority, than ammo, than weapon)
	
   #Distance variance logic:
	#1. If DistantVarianceReversed false
	#  a) if DistantVariance > 1.0 - (0 <= distance <= DamageFalloffStartDistance) damage coeff = DistantVariance
	#                       (DamageFalloffStartDistance < distance < DamageFalloffEndDistance)
#						   damage coeff decrease from DistantVariance(at DamageFalloffStartDistance) to 1(at DamageFalloffEndDistance)
#	  b) if DistantVariance < 1.0 - (0 <= distance <= DamageFalloffStartDistance) damage coeff = 1
#	                       (DamageFalloffStartDistance < distance < DamageFalloffEndDistance)
#						   damage coeff decrease from 1(at DamageFalloffStartDistance) to DistantVariance(at DamageFalloffEndDistance)
#						   if DamageFalloffStartDistance is 0 assumed to be MediumRange
#						   if DamageFalloffEndDistance is less than DamageFalloffStartDistance assumed to be MaxRange
#	2. If DistantVarianceReversed true
#	  a) if DistantVariance > 1.0 - (0 <= distance <= DamageFalloffStartDistance) damage coeff = 1
#	                       (DamageFalloffStartDistance < distance < DamageFalloffEndDistance) 
#						   damage coeff grow from 1(at DamageFalloffStartDistance) to DistantVariance(at DamageFalloffEndDistance)
#						   (DamageFalloffEndDistance <= distance < MaxRange) damage coeff = DistantVariance
#	  b) if DistantVariance < 1.0 - (0 <= distance <= DamageFalloffStartDistance) damage coeff = DistantVariance
#	                       (DamageFalloffStartDistance < distance < DamageFalloffEndDistance) 
#						   damage coeff grow from DistantVariance(at DamageFalloffStartDistance) to 1(at DamageFalloffEndDistance)
#						   (DamageFalloffEndDistance <= distance < MaxRange) damage coeff = 1
#						   if DamageFalloffStartDistance is 0 assumed to be MinRange
#						   if DamageFalloffEndDistance is less than DamageFalloffStartDistance assumed to be MediumRange	

 #"DistantVariance": 0.1,
 # "DistantVarianceReversed": true,
 # "isHeatVariation": true,
 # "isStabilityVariation": true,
 # "isDamageVariation": true,
 # "RangedDmgFalloffType": "Linear",
 # "DamageFalloffStartDistance": 30,
#  "DamageFalloffEndDistance": 600,

#public static float DistanceDamageMod(
 #     this Weapon weapon,
  #    Vector3 attackPos,
   #   ICombatant target,
    #  bool log = true)
    #{
    #  float num1 = weapon.DistantVariance();
     # float num2 = 1f;
     # float num3 = Vector3.Distance(attackPos, target.get_TargetPosition());
     # float num4 = weapon.DamageFalloffStartDistance();
     # if ((double) num4 < (double) CustomAmmoCategories.Epsilon)
     #   num4 = weapon.get_MediumRange(); #this sets medium range as default if nothing set.
     # float num5 = weapon.DamageFalloffEndDistance();
     # if ((double) num5 < (double) num4)
     #   num5 = weapon.get_MaxRange(); #if nothing set use max range
     # float num6 = 1f;
     # if ((double) num5 - (double) num4 > (double) CustomAmmoCategories.Epsilon)
     #   num6 = (float) (((double) num3 - (double) num4) / ((double) num5 - (double) num4));
     # if ((double) num1 > 1.0)
     #   num2 = (double) num3 > (double) num4 ? num1 - weapon.RangedDmgFalloffType(num6) * (num1 - 1f) : num1;
     # else if ((double) num1 < 1.0) # if in falloff range bracket
     #   num2 = (double) num3 > (double) num4 ? (float) (1.0 - (double) weapon.RangedDmgFalloffType(num6) * (1.0 - (double) num1)) : 1f;
     # float num7 = num2;
     # if (log)
     #   CustomAmmoCategoriesLog.Log.M.TWL(0, "defId: " + ((MechComponent) weapon).get_defId() + "\n" + string.Format("baseMultiplier: {0}\n", (object) num1) + string.Format("distance: {0}\n", (object) num3) + string.Format("start distance: {0}\n", (object) num4) + string.Format("end distance {0}\n", (object) num5) + string.Format("distanceRatio: {0}\n", (object) num6) + string.Format("result: {0}\n", (object) num7));
    #  return num7;

#if "DistantVarianceReversed" == False

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
            current_row.append(hardpoint_type)
         except KeyError:
            print('Missing Hardpoint Type')
            current_row.append('Handheld')

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
            weapon_heat_damage = data['HeatDamage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][-1]['ShotsWhenFired']) #heat damage = heat damage per shot * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes)
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
            weapon_firing_heat = data['HeatGenerated'] + data['Modes'][-1]['HeatGenerated']
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
               weapon_flat_jam = (data['FlatJammingChance'] + data['Modes'][-1]['FlatJammingChance'] * 100)  
               print('Flat jamming chance ' + str(weapon_flat_jam))
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               weapon_flat_jam = (data['FlatJammingChance'] * 100)
               print('No modes, reverting to base jam chance ' + str(weapon_flat_jam) + '%')
               current_row.append(weapon_flat_jam)
         except KeyError:
            try:
               weapon_flat_jam = (data['Modes'][-1]['FlatJammingChance'] * 100)
               print('No base flat jamming chance key, using modes ' + str(weapon_flat_jam) + '%')
               current_row.append(weapon_flat_jam)
            except (KeyError, IndexError) as e:
               print('No flat jamming chance on this weapon.')
               current_row.append(0)

         try:
            weapon_damage_per_heat = "{:.2f}".format(float(weapon_damage)/(float(weapon_firing_heat)))       
            print(weapon_damage_per_heat)
            current_row.append(weapon_damage_per_heat)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_slot = "{:.2f}".format(float(weapon_damage)/(float(weapon_slots)))
            print(weapon_damage_per_slot)
            current_row.append(weapon_damage_per_slot)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

         try:
            weapon_damage_per_ton = "{:.2f}".format(float(weapon_damage)/(float(weapon_tonnage)))
            print(weapon_damage_per_ton)
            current_row.append(weapon_damage_per_ton)
         except ZeroDivisionError:
            print('Divide by Zero!')
            current_row.append(0)

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
         #l.insert(newindex, l.pop(oldindex))
         current_row.insert(7,current_row.pop(3)) #this rearranges the current_row list to properly format it for the excel sheet
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
df.to_excel('RT Weaponlist.xlsx',sheet_name='Weapons')

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