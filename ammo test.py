import os
import json
import traceback
import time
time1 = time.time()#this is simply to test time efficiency

#change location variable to point to root of install location you want to analyze.
location = 'E:\Roguetech\RogueTech'
file_keyword_exclusion_list = []
ammo_file_list = []
excepted_files = []
possible_invalid_jsons = []
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
for item in ammo_file_list:
   with open(item) as f:
        print(item)
        try: 
            data = json.load(f)
            try:
               if data['Category'] not in ammotype_dam_multi_dict.keys():
                  print('New category, adding')
                  try:
                     if data['DamageMultiplier'] > 1:
                        ammotype_dam_multi_dict[data['Category']] = data['DamageMultiplier']
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam Multiplier', ammotype_dam_multi_dict[data['Category']])
                     else:
                        print('No DamageMultiplier on ammo; Defaulting to 1.')
                        ammotype_dam_multi_dict[data['Category']] = 1
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam Multiplier', ammotype_dam_multi_dict[data['Category']])
                  except KeyError:
                     print('No DamageMultiplier on ammo; Defaulting to 1.')
                     ammotype_dam_multi_dict[data['Category']] = 1
                     #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                     ammotype_dam_multi_best_dict[data['Category']] = f.name
                     print('Dam Multiplier ', ammotype_dam_multi_dict[data['Category']])

                  try:
                     if data['DamagePerShot'] > 1:
                        ammotype_dam_dict[data['Category']] = data['DamagePerShot']
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dampershot', ammotype_dam_dict[data['Category']])
                     else:
                        print('No DamagePerShot on ammo; Defaulting to 0.')
                        ammotype_dam_dict[data['Category']] = 1
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dampershot ', ammotype_dam_multi_dict[data['Category']])
                  except KeyError:
                     print('No DamagePerShot on ammo; Defaulting to 0.')
                     ammotype_dam_dict[data['Category']] = 0
                     #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                     ammotype_dam_best_dict[data['Category']] = f.name
                     print('Dampershot ', ammotype_dam_dict[data['Category']])

                  try:
                     if data['HeatDamagePerShot'] > 0:
                        ammotype_heatdam_dict[data['Category']] = data['HeatDamagePerShot']
                        #ammotype_heatdam_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                     else:
                        print('No HeatDamagePerShot on ammo; Defaulting to 0.')
                        ammotype_heatdam_dict[data['Category']] = 0
                        #ammotype_heatdam_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                  except KeyError:
                     print('No HeatDamagePerShot on ammo; Defaulting to 0.')
                     ammotype_heatdam_dict[data['Category']] = 0
                     #ammotype_heatdam_best_dict[data['Category']] = data['Description']['Name']
                     ammotype_heatdam_best_dict[data['Category']] = f.name
                     print('Heatdam ', ammotype_heatdam_dict[data['Category']])

                  try:
                     if data['HitGenerator'] == 'Cluster':
                        ammotype_doescluster_dict[data['Category']] = True
                        print(ammotype_heatdam_dict[data['Category']], ' does cluster!')
                     else:
                        ammotype_doescluster_dict[data['Category']] = False
                        print(ammotype_doescluster_dict[data['Category']], ' Ammo does not Cluster')
                  except KeyError:
                     print('No HitGenerator trait on ammo, defaulting to False')
                     ammotype_doescluster_dict[data['Category']] = False
                     print(ammotype_doescluster_dict[data['Category']], ' does not Cluster')
                  
               elif data['Category'] in ammotype_dam_multi_dict.keys():
                  print('Existing category, comparing')
                  try:
                     if data['DamageMultiplier'] > ammotype_dam_multi_dict[data['Category']]:
                        ammotype_dam_multi_dict[data['Category']] = data['DamageMultiplier']
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_multi_best_dict[data['Category']] = f.name
                        print('Dam ', ammotype_dam_multi_dict[data['Category']])
                  except KeyError:
                     print('No DamageMultiplier on ammo; Skipping as key already has an entry value higher than this')
                  
                  try:
                     if data['DamagePerShot'] > ammotype_dam_dict[data['Category']]:
                        ammotype_dam_dict[data['Category']] = data['DamagePerShot']
                        #ammotype_dam_multi_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_dam_best_dict[data['Category']] = f.name
                        print('Dam ', ammotype_dam_dict[data['Category']])
                  except KeyError:
                     print('No DamagePerShot on ammo; Skipping as key already has an entry value higher than this.')

                  try:
                     if data['HeatDamagePerShot'] > ammotype_heatdam_dict[data['Category']]:
                        ammotype_heatdam_dict[data['Category']] = data['HeatDamagePerShot']
                        #ammotype_heatdam_best_dict[data['Category']] = data['Description']['Name']
                        ammotype_heatdam_best_dict[data['Category']] = f.name
                        print('Heatdam ', ammotype_heatdam_dict[data['Category']])
                  except KeyError:
                     print('No HeatDamagePerShot on ammo; Skipping as key already has an entry of 0 or above')
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
print(ammotype_dam_multi_best_dict, ammotype_dam_dict, ammotype_heatdam_best_dict, ammotype_heatdam_dict, ammotype_dam_best_dict, ammotype_dam_dict, ammotype_doescluster_dict)

    
