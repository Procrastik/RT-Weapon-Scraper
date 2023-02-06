import os
import sys
import json
import traceback
import pandas
import time
import re
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Text

## TKinter stuff
# Create tk main window
root = tk.Tk()

# Set window label
root.title('RogueTech Weapon Scraper')

# set window size in pixels
window_width = 600
window_height = 400

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# sets window to the top layer, it will always be visible on screen when launched
root.attributes('-topmost', 1)

# Initialize the mod folder location for population in the select_directory def.
location = ''


def select_directory():
    global location
    location = filedialog.askdirectory(
        title='Select your RogueTech Mods folder',
        initialdir='./')
    path_text.delete('1.0', 'end')
    path_text.insert('1.0', location)
    # Set Go button values and command
    go_button = ttk.Button(
        text="Go!",
        command=get_to_work
    )
    go_button.pack()


# open button
open_button = ttk.Button(
    root,
    text='Select your RogueTech Mods folder',
    command=select_directory
)
open_button.pack(expand=True)

# Logging variable checkbox to vastly improve performance when troubleshooting is not needed
logging = False
logging_checkbutton = tk.BooleanVar()


def toggle_logging():
    global logging
    logging = logging_checkbutton.get()
    print(logging)

ttk.Checkbutton(root,
                text='Logging',
                command=toggle_logging,
                variable=logging_checkbutton,
                onvalue=True,
                offvalue=False).pack()

# Textbox for displaying initial message to select mod folder; displays selected folder path after selection
path_text = Text(root, height=1)
path_text.insert('1.0', 'Please use the button and select your RogueTech Mods folder.')
path_text.pack()

## End Tkinter stuff


def get_to_work():
    # This is simply to test time efficiency
    time1 = time.time()

    # Add anything you would like excluded here, but do not remove anything outside of Nuke or you will break the program
    # as these filter out some odd or generally unusable equipment.
    file_keyword_exclusion_list = ['Melee', 'FCS', 'Linked', 'Turret', 'Ambush', 'Infantry', 'deprecated', 'Quirk', 'quirk', 'Nuke']
    weapon_file_list = []
    ams_file_list = []
    filtered_files = []
    excepted_files = []
    possible_invalid_jsons = []
    columns_list = ['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Indirectfire',
                    'Clustering Capable (Weapon or with ammo)', 'Tonnage', 'Slots', 'Max Recoil', 'Base Direct Damage',
                    'Max Direct Damage', 'Max Bonus Ammo Damage',
                    'Highest Direct Damage Ammo (Comparing Damage Bonus/Multiplier)', 'AOE Damage', 'AOE Heat Damage', 'AOE Radius',
                    'Highest Bonus AOE Ammo', 'Damage Variance', 'Max Stability Damage', 'Max Heat Damage',
                    'Max Per Ammo Heat Damage', 'Highest Direct Heat Damage Ammo', 'Max Firing Heat', 'Max Jam Chance',
                    'Can Misfire', 'Damage Per Heat', 'Damage Per Slot', 'Damage Per Ton', 'Weapon Crit Multiplier',
                    'Weapon Base Crit Chance', 'Weapon TAC Chance (50% Max Thickness)', 'Max TAC Armor Thickness',
                    'Base Accuracy Bonus', 'Base Evasion Ignore', 'Min Range', 'Short Range', 'Medium Range', 'Long Range',
                    'Max Range', 'Damage Falloff %', 'Min Range Damage', 'Short Range Damage', 'Medium Range Damage',
                    'Long Range Damage', 'Max Range Damage', 'Weapon AAA Factor %']
    ams_columns_list = ['Hardpoint Type', 'Weapon Class', 'Weapon Name', 'Tonnage', 'Slots',
                        'Activations Per Round', 'Base Damage Per Shot', 'Base Average Damage',
                        'Base Max Damage Per Activation', 'Base Shots Per Activation', 'Base Hit Chance',
                        'Base Heat Per Activation', 'Base Jam Chance', 'Base Max Range', 'Base Protect Allies']
    df = pandas.DataFrame(columns=columns_list)
    ams_df = pandas.DataFrame(columns=ams_columns_list)
    ##

    ammo_file_list = []
    ammotype_dam_dict = {}
    ammotype_dam_best_dict = {}
    ammotype_heatdam_dict = {}
    ammotype_heatdam_best_dict = {}
    ammotype_heatdam_multi_dict = {}
    ammotype_heatdam_AOE_dict = {}
    ammotype_heatdam_AOE_best_dict = {}
    ammotype_doescluster_dict = {}
    ammotype_BallisticDamagePerPallet = {} # TODO this is currently captured but unused; may need to use it in the weapon damage module if it takes ammo into account as this should fix the absurd heat damage of some fringe heat values
    ammotype_dam_multi_dict = {}
    ammotype_dam_multi_best_dict = {}
    ammotype_dam_AOE_dict = {}
    ammotype_dam_AOE_best_dict = {}
    ammotype_radius_AOE_dict = {}
    ##

    # This iterates through the 'location' variable path from top directory down looking for listed criteria in the for loop and adds it to list ammo_file_list
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
        if logging:
            print(r)
        for item in f:
            file_in_exclusion_list = False
            if 'Ammunition_' in item:
                if logging:
                    print('File has Ammunition in name: ', item)
                if 'json' in item:
                    if logging:
                        print('File also has json in name: ', item)
                    for i in file_keyword_exclusion_list:
                        if logging:
                            print(i, file_in_exclusion_list)
                        if i in item:
                            file_in_exclusion_list = True
                            continue
                        elif i in r:
                            file_in_exclusion_list = True
                            continue
                    if not file_in_exclusion_list:
                        ammo_file_list.append(os.path.join(r, item))
                        if logging:
                            print('Passed ', item)
    ##

    # This iterates through the ammo_file_list, prints the filename and loads them with the json module so you can search them and finally checks if there is any loading errors and adds them to lists to help identify invalid JSONs or bad characters.
    # Do not combine this with the weapon_file_list because it is twice as fast this way than combined
    for item in ammo_file_list:
        with open(item) as f:
            if logging:
                print(item)
            try:
                data = json.load(f)
                try:
                    ammotype_ShotsWhenFired = 1
                    ammotype_ProjectilesWhenFired = 1
                    ammotype_dam_multiplier = 1.0
                    if data['Category'] not in ammotype_dam_multi_dict.keys():
                        # This if block handles building new keys in the dict for ammo types not already in the dict
                        #  TODO add BallisticDamagePerPallet
                        if logging:
                            print('New category, adding')
                        try:
                            ammotype_dam_multiplier = data['DamageMultiplier']
                            if logging:
                                print('Dam Multiplier ', ammotype_dam_multiplier)
                        except KeyError:
                            if logging:
                                print('No DamageMultiplier on ammo; Defaulting to 1.')

                        try:
                            if data['ShotsWhenFired'] > 1:
                                ammotype_ShotsWhenFired = data['ShotsWhenFired']
                            if logging:
                                print('Ammo ShotsWhenFired ', ammotype_ShotsWhenFired)
                        except KeyError:
                            if logging:
                                print('No ShotsWhenFired on ammo; Defaulting to 1.')

                        try:
                            if data['ProjectilesPerShot'] > 1:
                                ammotype_ProjectilesWhenFired = data['ProjectilesPerShot']
                            if logging:
                                print('Ammo ProjectilesPerShot ', ammotype_ProjectilesWhenFired)
                        except KeyError:
                            if logging:
                                print('No ProjectilesPerShot on ammo; Defaulting to 1.')

                        try:
                            ammo_DamagePerShot = data['DamagePerShot']
                            if data['BallisticDamagePerPallet']:
                                if logging:
                                    print('BallisticDamagePerPallet on ammo')
                                ammo_DamagePerShot /= ammotype_ProjectilesWhenFired
                            if float(ammo_DamagePerShot * ammotype_dam_multiplier * ammotype_ShotsWhenFired * ammotype_ProjectilesWhenFired) > 0:
                                ammotype_dam_dict[data['Category']] = ammo_DamagePerShot * ammotype_ShotsWhenFired * ammotype_ProjectilesWhenFired
                                ammotype_dam_best_dict[data['Category']] = f.name
                                ammotype_dam_multi_dict[data['Category']] = ammotype_dam_multiplier
                                if logging:
                                    print('Ammo salvo damage ', ammotype_dam_dict[data['Category']])
                            else:
                                if logging:
                                    print('No DamagePerShot on ammo; Defaulting to 0.')
                                ammotype_dam_dict[data['Category']] = 0
                                ammotype_dam_best_dict[data['Category']] = f.name
                                ammotype_dam_multi_dict[data['Category']] = ammotype_dam_multiplier
                                if logging:
                                    print('Dampershot ', ammotype_dam_dict[data['Category']])
                        except KeyError:
                            if logging:
                                print('No DamagePerShot on ammo; Defaulting to 0.')
                            ammotype_dam_dict[data['Category']] = 0
                            ammotype_dam_best_dict[data['Category']] = f.name
                            ammotype_dam_multi_dict[data['Category']] = ammotype_dam_multiplier
                            if logging:
                                print('Dampershot ', ammotype_dam_dict[data['Category']])

                        # Ammo heat damage module
                        # Checks for HeatDamage, HeatDamagePerShot, and AOEHeatDamage
                        try:
                            ammo_heatmultipler = data['HeatMultiplier']
                        except KeyError:
                            ammo_heatmultipler = 1  # If no HeatMultiplier on ammo, defaults to 1
                        if logging:
                            print('Ammo existing key comparison HeatMultiplier value is ', ammo_heatmultipler)
                        try:
                            ammo_heatdampershot = data['HeatDamagePerShot']
                        except KeyError:
                            ammo_heatdampershot = 0  # If no HeatDamagePerShot on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison HeatDamagePerShot value is ', ammo_heatdampershot)
                        try:
                            ammo_heatdam = data['HeatDamage']
                        except KeyError:
                            ammo_heatdam = 0  # If no HeatDamage on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison HeatDamage value is ', ammo_heatdam)
                        try:
                            ammo_AOEheatdam = data['AOEHeatDamage']
                        except KeyError:
                            ammo_AOEheatdam = 0  # If no AOEHeatDamage on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison AOEHeatDamage value is ', ammo_AOEheatdam)

                        try:
                            if ammo_heatdampershot + ammo_heatdam != 0:
                                ammotype_heatdam_dict[data['Category']] = ammo_heatdampershot + ammo_heatdam
                                ammotype_heatdam_best_dict[data['Category']] = f.name
                                ammotype_heatdam_multi_dict[data['Category']] = ammo_heatmultipler
                            else:
                                if logging:
                                    print('No HeatDamage, HeatDamagePerShot, or AOEHeatDamage on ammo. Adding key value but defaulting to zero HeatDamage')
                                ammotype_heatdam_dict[data['Category']] = 0
                                ammotype_heatdam_best_dict[data['Category']] = f.name
                                ammotype_heatdam_multi_dict[data['Category']] = 1
                                if logging:
                                    print('Ammo Heatdam ', ammotype_heatdam_dict[data['Category']])
                        except KeyError:
                            if logging:
                                print('Ammo has no category, not sure this is possible unless something is broken with the ammo?')

                        # Ammo clustering check module
                        try:
                            if data['HitGenerator'] == 'Cluster':
                                ammotype_doescluster_dict[data['Category']] = True
                                if logging:
                                    print(ammotype_doescluster_dict[data['Category']], ' does cluster!')
                            elif data['HitGenerator'] == 'Streak':
                                ammotype_doescluster_dict[data['Category']] = True
                                if logging:
                                    print(ammotype_doescluster_dict[data['Category']], ' does cluster!')
                            else:
                                ammotype_doescluster_dict[data['Category']] = False
                                if logging:
                                    print(ammotype_doescluster_dict[data['Category']], ' Ammo does not Cluster')
                        except KeyError:
                            if logging:
                                print('No HitGenerator trait on ammo, defaulting to False')
                            ammotype_doescluster_dict[data['Category']] = False
                            if logging:
                                print(ammotype_doescluster_dict[data['Category']], ' does not Cluster')

                        # BallisticDamagePerPallet is a CustomAmmoCategories (CAC) trait on weapons or ammo that causes the weapon or ammo damage to be divided by the ProjectilesPerShot trait
                        # TODO add this to the damage module to add a key value for the best ammo type for accurate damage calculations
                        try:
                            if data['BallisticDamagePerPallet']:
                                ammotype_BallisticDamagePerPallet[data['Category']] = True
                                if logging:
                                    print(ammotype_BallisticDamagePerPallet[data['Category']], ' BallisticDamagePerPallet detected on ammo, damage will be divided by ProjectilesPerShot')
                            else:
                                ammotype_BallisticDamagePerPallet[data['Category']] = False
                                if logging:
                                    print(ammotype_BallisticDamagePerPallet[data['Category']], ' BallisticDamagePerPallet false detected on ammo, damage will calculated normally')
                        except KeyError:
                            ammotype_BallisticDamagePerPallet[data['Category']] = False
                            if logging:
                                print(ammotype_BallisticDamagePerPallet[data['Category']], 'No BallisticDamagePerPallet detected on ammo, damage will be calculated normally')

                        try:
                            if data['AOEDamage'] > 0:
                                ammotype_dam_AOE_dict[data['Category']] = data['AOEDamage']
                                ammotype_dam_AOE_best_dict[data['Category']] = f.name
                                if logging:
                                    print('AOE heat damage ', ammotype_dam_AOE_dict[data['Category']])
                            else:
                                if logging:
                                    print('No AOE damage on ammo; Defaulting to 0.')
                                ammotype_dam_AOE_dict[data['Category']] = 0
                                ammotype_dam_AOE_best_dict[data['Category']] = f.name
                        except KeyError:
                            if logging:
                                print('No AOE heat damage on ammo; Defaulting to 0.')
                            ammotype_dam_AOE_dict[data['Category']] = 0
                            ammotype_dam_AOE_best_dict[data['Category']] = 'N/A'

                        try:
                            if ammo_AOEheatdam > 0:
                                ammotype_heatdam_AOE_dict[data['Category']] = ammo_AOEheatdam
                                ammotype_heatdam_AOE_best_dict[data['Category']] = f.name # TODO captured filename of best AOE Heat Damage but unused currently, might us this later
                                if logging:
                                    print('AOE heat damage ', ammotype_heatdam_AOE_dict[data['Category']])
                            else:
                                if logging:
                                    print('No AOE heat damage on ammo; Defaulting to 0.')
                                ammotype_heatdam_AOE_dict[data['Category']] = 0
                                ammotype_heatdam_AOE_best_dict[data['Category']] = f.name
                        except KeyError:
                            if logging:
                                print('No AOE damage on ammo; Defaulting to 0.')
                            ammotype_heatdam_AOE_dict[data['Category']] = 0
                            ammotype_heatdam_AOE_best_dict[data['Category']] = 'N/A'

                        try:
                            if data['AOERange'] > 0:
                                ammotype_radius_AOE_dict[data['Category']] = data['AOERange']
                        except KeyError:
                            if logging:
                                print('No AOE range on ammo; Defaulting to 0.')
                            ammotype_radius_AOE_dict[data['Category']] = 0

                    #  This block compares existing key values to the currently evaluated ammo type and replaces the best values as needed
                    #  TODO add BallisticDamagePerPallet check for ammo damage calculation to this block
                    elif data['Category'] in ammotype_dam_multi_dict.keys():
                        if logging:
                            print('Existing category, comparing')
                        try:
                            ammotype_dam_multiplier = data['DamageMultiplier']
                            if logging:
                                print('Dam Multiplier ', ammotype_dam_multiplier)
                        except KeyError:
                            if logging:
                                print('No DamageMultiplier on ammo; Defaulting to 1.')

                        try:
                            if float(data['DamagePerShot']) * ammotype_dam_multiplier > float(ammotype_dam_dict[data['Category']]) * ammotype_dam_multi_dict[data['Category']]:
                                ammotype_dam_dict[data['Category']] = data['DamagePerShot']
                                ammotype_dam_best_dict[data['Category']] = f.name
                                ammotype_dam_multi_dict[data['Category']] = ammotype_dam_multiplier
                                if logging:
                                    print('Dam ', ammotype_dam_dict[data['Category']])
                            elif float(data['DamagePerShot']) * ammotype_dam_multiplier == float(
                                    ammotype_dam_dict[data['Category']]) * ammotype_dam_multi_dict[data['Category']]:
                                if logging:
                                    print('Ammo DamagePerShot equal to existing best, setting best to multiple')
                                ammotype_dam_best_dict[data['Category']] = 'Multiple'
                        except KeyError:
                            if logging:
                                print('No DamagePerShot on ammo; Comparing to best in case they are the same')
                            if ammotype_dam_dict[data['Category']] == 0:
                                if ammotype_dam_multi_dict[data['Category']] < ammotype_dam_multiplier:
                                    if logging:
                                        print('Ammo DamagePerShot equal to 0 or existing best but ammo multiplier is higher. Changing best ammo and multiplier.')
                                    ammotype_dam_best_dict[data['Category']] = f.name
                                    ammotype_dam_multi_dict[data['Category']] = ammotype_dam_multiplier
                                elif ammotype_dam_multi_dict[data['Category']] == ammotype_dam_multiplier:
                                    ammotype_dam_best_dict[data['Category']] = 'Multiple'

                        # Ammo heat damage module, existing key comparison
                        # Checks for HeatDamage, HeatDamagePerShot, and AOEHeatDamage
                        try:
                            ammo_heatmultipler = data['HeatMultiplier']
                        except KeyError:
                            ammo_heatmultipler = 1  # If no HeatMultiplier on ammo, defaults to 1
                        if logging:
                            print('Ammo existing key comparison HeatMultiplier value is ', ammo_heatmultipler)
                        try:
                            ammo_heatdampershot = data['HeatDamagePerShot']
                        except KeyError:
                            ammo_heatdampershot = 0  # If no HeatDamagePerShot on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison HeatDamagePerShot value is ', ammo_heatdampershot)
                        try:
                            ammo_heatdam = data['HeatDamage']
                        except KeyError:
                            ammo_heatdam = 0  # If no HeatDamage on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison HeatDamage value is ', ammo_heatdam)
                        try:
                            ammo_AOEheatdam = data['AOEHeatDamage']
                        except KeyError:
                            ammo_AOEheatdam = 0  # If no AOEHeatDamage on ammo, defaults to 0
                        if logging:
                            print('Ammo existing key comparison AOEHeatDamage value is ', ammo_AOEheatdam)

                        try:
                            if ammo_heatdampershot + ammo_heatdam > ammotype_heatdam_dict[data['Category']]:
                                ammotype_heatdam_dict[data['Category']] = ammo_heatdampershot + ammo_heatdam
                                ammotype_heatdam_best_dict[data['Category']] = f.name
                                ammotype_heatdam_multi_dict[data['Category']] = ammo_heatmultipler
                                if logging:
                                    print('New best ammo Heatdam ', ammotype_heatdam_dict[data['Category']], ' with a HeatMultiplier of ', ammo_heatmultipler)
                            elif ammo_heatdampershot + ammo_heatdam == ammotype_heatdam_dict[data['Category']]:
                                ammotype_heatdam_best_dict[data['Category']] = 'Multiple'
                                if logging:
                                    print('Ties best ammo Heatdam ', ammotype_heatdam_dict[data['Category']], ' with a HeatMultiplier of ', ammo_heatmultipler)
                        except KeyError:
                            if logging:
                                print('No HeatDamagePerShot on ammo; Skipping as key already has an entry of 0 or above')

                        # Ammo Clustering check
                        try:
                            if ammotype_doescluster_dict[data['Category']] == False:
                                if data['HitGenerator'] == 'Cluster':
                                    ammotype_doescluster_dict[data['Category']] = True
                                    if logging:
                                        print(ammotype_doescluster_dict[data['Category']], ' does cluster!')
                        except KeyError:
                            if logging:
                                print('No HitGenerator trait on ammo, skipping.')

                        try:
                            if data['AOEDamage'] > ammotype_dam_AOE_dict[data['Category']]:
                                ammotype_dam_AOE_dict[data['Category']] = data['AOEDamage']
                                ammotype_dam_AOE_best_dict[data['Category']] = f.name
                                if logging:
                                    print('AOE dam ', ammotype_dam_AOE_dict[data['Category']])
                            elif data['AOEDamage'] == ammotype_dam_AOE_dict[data['Category']] and ammotype_dam_AOE_dict[data['Category']] != 0:
                                ammotype_dam_AOE_best_dict[data['Category']] = 'Multiple'
                        except KeyError:
                            if logging:
                                print('No AOE damage on ammo; Defaulting to 0.')

                        try:
                            if ammo_AOEheatdam > ammotype_heatdam_AOE_dict[data['Category']]:
                                ammotype_heatdam_AOE_dict[data['Category']] = ammo_AOEheatdam
                                ammotype_heatdam_AOE_best_dict[data['Category']] = f.name # TODO captured filename of best AOE Heat Damage but unused currently, might us this later
                                if logging:
                                    print('New ammo AOE heat damage ', ammotype_heatdam_AOE_dict[data['Category']])
                            elif ammo_AOEheatdam == ammotype_heatdam_AOE_dict[data['Category']] and ammotype_heatdam_AOE_dict[data['Category']] != 0:
                                ammotype_heatdam_AOE_dict[data['Category']] = 'Multiple'
                        except KeyError:
                            if logging:
                                print('No AOE heat damage on ammo; Defaulting to 0.')

                        try:
                            if data['AOERange'] > ammotype_radius_AOE_dict[data['Category']]:
                                ammotype_radius_AOE_dict[data['Category']] = data['AOERange']
                        except KeyError:
                            if logging:
                                print('No AOE range on ammo; Defaulting to 0.')

                except KeyError:
                    if logging:
                        traceback.print_exc()
                        print('No Category on ammo! Skipping.')
            except UnicodeDecodeError:
                excepted_files.append(item)
                if logging:
                    print('Possible invalid character in JSON')
            except json.decoder.JSONDecodeError:
                possible_invalid_jsons.append(item)
                if logging:
                    print('Possible invalid JSON!')
    if logging:
        print(ammotype_dam_multi_best_dict, ammotype_dam_multi_dict, ammotype_heatdam_best_dict, ammotype_heatdam_dict, ammotype_dam_best_dict, ammotype_dam_dict, ammotype_doescluster_dict)

    # This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list weapon_file_list
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
        if logging:
            print(r)
        for item in f:
            file_in_exclusion_list = False
            if 'Weapon_' in item:
                if logging:
                    print('File has weapon in name: ', item)
                if 'json' in item:
                    if logging:
                        print('File also has json in name: ', item)
                    if 'AMS' in item:
                        if logging:
                            print('AMS in weapon loop, skipping')
                        continue
                    for i in file_keyword_exclusion_list:
                        if logging:
                            print(i, file_in_exclusion_list)
                        if i in item:
                            file_in_exclusion_list = True
                            continue
                        elif i in r:
                            file_in_exclusion_list = True
                            continue
                    if not file_in_exclusion_list:
                        weapon_file_list.append(os.path.join(r, item))
                        if logging:
                            print('Passed ', item)
    ##

    # This iterates through all of the 'location' path from top directory down looking for listed criteria in the for loop and adds it to list ams_file_list
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
        if logging:
            print(r)
        for item in f:
            file_in_exclusion_list = False
            if 'AMS' in item:
                if logging:
                    print('File has weapon and AMS in name: ', item)
                if 'Weapon_' in item:
                    if logging:
                        print('File also has Weapon also in name')
                    if 'json' in item:
                        if logging:
                            print('File also has json in name: ', item)
                        for i in file_keyword_exclusion_list:
                            if logging:
                                print(i, file_in_exclusion_list)
                            if i in item:
                                file_in_exclusion_list = True
                                continue
                            elif i in r:
                                file_in_exclusion_list = True
                                continue
                        if not file_in_exclusion_list:
                            ams_file_list.append(os.path.join(r, item))
                            if logging:
                                print('Passed ', item)
    ##

    # This iterates through the weapon_file_list, prints the filename and loads them with the json module so you can search them and finally checks if there is any loading errors and adds them to lists to help identify invalid JSONs or bad characters.
    for item in weapon_file_list:
        with open(item) as f:
            if logging:
                print(item)
            try:
                data = json.load(f)
                current_row = []

                # Weapon hardpoint module
                try:
                    hardpoint_type = str(data['Category'])
                    if logging:
                        print(hardpoint_type)
                except KeyError:
                    if logging:
                        print('Missing Hardpoint Type')
                    try:
                        hardpoint_type = str(data['weaponCategoryID'])
                    except KeyError:
                        if logging:
                            print('Weapon has no Type?')
                        hardpoint_type = 'N/A'
                current_row.append(hardpoint_type)

                # Weapon type module
                try:
                    weapon_class = str(data['Type'])
                    if logging:
                        print(weapon_class)
                    current_row.append(weapon_class)
                except KeyError:
                    if logging:
                        print('Missing Weapon Type')
                    current_row.append('N/A')

                # Weapon name module
                try:
                    if 'deprecated' in str(data['Description']['UIName']).lower():
                        if logging:
                            print('Deprecated in name, skipping')
                        filtered_files.append(item)
                        continue
                    weapon_name = str(data['Description']['UIName'])
                    if logging:
                        print(weapon_name)
                    current_row.append(weapon_name)
                except KeyError:
                    # This will skip the file if it has no weapon UI name as this means it isn't valid or isn't used
                    if logging:
                        print('Missing Weapon Name')
                    filtered_files.append(item)
                    continue

                # weapon damage module - pulls the highest damage from base + any available modes and sets value to weapon_damage variable
                try:
                    max_mode_dam = 0  # set value of highest additional damage in modes
                    max_dam_mode = 0  # set value of highest additional damage mode
                    weapon_damage = 0  # Damage modes loop max damage value
                    for i in range(len(data['Modes'])):  # for loop to iterate over the number of Modes found
                        if logging:
                            print('Damage mode', i)
                        try:
                            if data['Modes'][i]['DamagePerShot'] > max_mode_dam:
                                max_mode_dam = data['Modes'][i]['DamagePerShot']
                                max_dam_mode = i
                            try:
                                if data['Modes'][i]['ShotsWhenFired']:  # check for ShotsWhenFired in mode
                                    weapon_damage = (data['Damage'] + max_mode_dam) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired'])
                            except KeyError:
                                weapon_damage = (data['Damage'] + max_mode_dam) * data['ProjectilesPerShot'] * data['ShotsWhenFired']
                        except KeyError:  # if no DamagePerShot in mode found
                            if logging:
                                print('No DamagePerShot in modes, reverting to base values')
                            weapon_damage = data['Damage'] * data['ProjectilesPerShot'] * data['ShotsWhenFired']
                except KeyError:  # This will catch errors when a weapon has no modes.
                    if logging:
                        print('No modes, reverting to base values')
                    weapon_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])  # damage = damage per shot * projectilespershot

                try:
                    max_shots_mode = 0  # set mode index of mode with highest shot count
                    max_mode_shots = 0  # set value of mode with most additional shots
                    weapon_damage2 = 0  # Shots modes loop max damage value
                    for i in range(len(data['Modes'])):
                        if logging:
                            print('Shots loop:', i)
                        try:  # if no damage in modes found then check modes for additional shots and calculate damage against base value
                            if data['Modes'][i]['ShotsWhenFired'] > max_mode_shots:
                                max_mode_shots = data['Modes'][i]['ShotsWhenFired']
                                max_shots_mode = i
                            try:
                                weapon_damage2 = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + max_mode_shots)  # damage = damage per shot + max damage mode extra damage * projectilespershot * (shotswhenfiredbase + shotswhenfired in modes + damage in modes)
                                if logging:
                                    print(max_mode_shots)
                            except:
                                if logging:
                                    print('can this be reached?')
                                    traceback.print_exc()
                        except:
                            if logging:
                                traceback.print_exc()
                                print('No additional ShotsWhenFired found in modes, reverting to base')
                except KeyError:  # removed indexerror as this should not throw one. This will catch errors when a weapon has no modes.
                    if logging:
                        print('No modes. Reverting to base values.')
                    weapon_damage2 = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])  # damage = damage per shot * projectilespershot
                if logging:
                    print('DMG Modes ' + str(weapon_damage), ' Shots Modes ', str(weapon_damage2))
                if weapon_damage2 > weapon_damage:  # checks the max damage mode and the max shots mode loop max damage values against each other and sets the highest
                    weapon_damage = weapon_damage2
                    max_dam_mode = max_shots_mode

                # Weapon damage multiplier module - This is used on the result of the damage module to calculate max damage value and is effectively part of the damage module
                try:
                    weapon_damage_multiplier = ammotype_dam_multi_dict[data['AmmoCategory']]
                    try:
                        weapon_damage_multiplier *= data['DamageMultiplier'] * data['Modes'][max_dam_mode]['DamageMultiplier']
                    except KeyError:
                        if logging:
                            print('Damage multiplier on ammo but not on mode, checking only base and ammo')
                        try:
                            weapon_damage_multiplier *= data['DamageMultiplier']
                        except KeyError:
                            if logging:
                                print('Damage multiplier only on ammo')
                except KeyError:
                    if logging:
                        print('No ammo key on this weapon, checking mode and base for damage multiplier')
                    try:
                        weapon_damage_multiplier = data['DamageMultiplier'] * data['Modes'][max_dam_mode]['DamageMultiplier']
                    except KeyError:
                        if logging:
                            print('No damage multiplier in ammo or in modes, checking only base')
                        try:
                            weapon_damage_multiplier = data['DamageMultiplier']
                        except KeyError:
                            if logging:
                                print('No damage multiplier, using 1 as default')
                            weapon_damage_multiplier = 1
                if logging:
                    print('Base max weapon damage is ', weapon_damage)
                weapon_damage *= weapon_damage_multiplier
                if logging:
                    print('Multiplier max weapon damage is ', weapon_damage)
                current_row.append(weapon_damage)

                # Indirectfire check module
                try:
                    for i in range(len(data['Modes'])):  # for loop to iterate over the number of Modes found
                        if logging:
                            print('Mode ', i)
                        try:
                            if data['Modes'][i]['IndirectFireCapable'] == True:
                                indirect_fire = 'True'
                                break
                        except KeyError:  # if no IndirectFireCapable in mode found
                            try:
                                indirect_fire = str(data['IndirectFireCapable'])
                            except KeyError:
                                if logging:
                                    print('Missing Indirect Fire boolean')
                                indirect_fire = 'False'
                except KeyError:
                    try:
                        indirect_fire = str(data['IndirectFireCapable'])
                    except KeyError:
                        if logging:
                            print('Missing Indirect Fire boolean')
                        indirect_fire = 'False'
                current_row.append(indirect_fire)

                # Weapon cluster module
                weapon_cluster = 'False'
                try:
                    if data['HitGenerator'] == 'Cluster':
                        weapon_cluster = 'True'
                        if logging:
                            print('HitGenerator cluster on weapon')
                    else:
                        try:
                            if 'wr-clustered_shots' in data['ComponentTags']['items']:
                                weapon_cluster = 'True'
                                if logging:
                                    print('wr-clustered_shots on weapon')
                            elif data['Type'] == 'LRM':
                                if logging:
                                    print('WeaponType is LRM')
                                try:
                                    if data['HitGenerator'] == 'Cluster':
                                        weapon_cluster = 'True'
                                except KeyError:
                                    if logging:
                                        print('Weapon is LRM and has no other HitGenerators, it does cluster.')
                                    weapon_cluster = 'True'
                        except KeyError:
                            if logging:
                                print('No wr-clustered_shots or Weapon Type, skipping')
                except KeyError:
                    if logging:
                        print('No HitGenerator trait on base weapon, checking other options')
                    try:
                        if 'wr-clustered_shots' in data['ComponentTags']['items']:
                            weapon_cluster = 'True'
                        elif data['Type'] == 'LRM':
                            if logging:
                                print('Weapon is LRM and has no other HitGenerators, it does cluster.')
                            weapon_cluster = 'True'
                    except KeyError:
                        if logging:
                            print('No wr-clustered_shots or Weapon Type, skipping')
                try:
                    if weapon_cluster == 'False':
                        for i in range(len(data['Modes'])):  # for loop to iterate over the number of Modes found
                            if logging:
                                print('Cluster check Mode ', i)
                            try:
                                if data['Modes'][i]['HitGenerator'] == 'Cluster':
                                    weapon_cluster = 'True in Mode'
                                    continue
                            except KeyError:
                                if logging:
                                    print('No clustering on this mode, trying next')
                except KeyError:
                    if logging:
                        print('No modes found on weapon for cluster check')
                try:
                    if ammotype_doescluster_dict[data['AmmoCategory']]:
                        weapon_cluster = 'True in Ammo'
                except KeyError:
                    if logging:
                        print('No ammo clustering for this weapon')

                current_row.append(weapon_cluster)

                # Tonnage check module
                if hardpoint_type == 'Special':
                    try:
                        weapon_tonnage = data['Custom']['CarryLeftOverUsage']
                        current_row.append(weapon_tonnage)
                    except KeyError:
                        try:
                            weapon_tonnage = data['Custom']['CarryHandUsage']
                            current_row.append(weapon_tonnage)
                        except KeyError:
                            weapon_tonnage = data['Tonnage']
                            if logging:
                                print('Tons ' + str(weapon_tonnage))
                            current_row.append(weapon_tonnage)
                            if weapon_tonnage > 50:  # this filters deprecated weapons that are 100 to 6666 tons
                                if logging:
                                    print('Filtered out deprecated weapon by tonnage')
                                filtered_files.append(item)
                                continue
                    except:
                        if logging:
                            print('Missing Tonnage')
                        current_row.append('N/A')
                elif hardpoint_type == 'SpecialHandHeld':
                    try:
                        weapon_tonnage = data['Custom']['CarryLeftOverUsage']
                        current_row.append(weapon_tonnage)
                    except KeyError:
                        try:
                            weapon_tonnage = data['Custom']['CarryHandUsage']
                            current_row.append(weapon_tonnage)
                        except KeyError:
                            weapon_tonnage = data['Tonnage']
                            if logging:
                                print('Tons ' + str(weapon_tonnage))
                            current_row.append(weapon_tonnage)
                            if weapon_tonnage > 50:  # this filters deprecated weapons that are 100 to 6666 tons
                                if logging:
                                    print('Filtered out deprecated weapon by tonnage')
                                filtered_files.append(item)
                                continue
                    except:
                        if logging:
                            print('Missing Tonnage')
                        current_row.append('N/A')
                else:
                    try:
                        weapon_tonnage = data['Tonnage']
                        if logging:
                            print('Tons ' + str(weapon_tonnage))
                        current_row.append(weapon_tonnage)
                        if weapon_tonnage > 50:  # this filters deprecated weapons that are 100 to 6666 tons
                            if logging:
                                print('Filtered out deprecated weapon by tonnage')
                            filtered_files.append(item)
                            continue
                    except:
                        if logging:
                            print('Missing Tonnage')
                        current_row.append('N/A')

                # Weapon slot size module
                try:
                    weapon_slots = data['InventorySize']
                    if logging:
                        print('Slots ' + str(weapon_slots))
                    current_row.append(weapon_slots)
                except:
                    if logging:
                        print('Missing Weapon Slots')
                    current_row.append('N/A')

                # Weapon refire module
                try:
                    if weapon_damage > weapon_damage2:
                        weapon_recoil = data['RefireModifier'] + data['Modes'][max_dam_mode]['RefireModifier']
                        if logging:
                            print('Recoil ' + str(weapon_recoil))
                        current_row.append(weapon_recoil)
                    elif weapon_damage2 >= weapon_damage:
                        weapon_recoil = data['RefireModifier'] + data['Modes'][max_shots_mode]['RefireModifier']
                        if logging:
                            print('Recoil ' + str(weapon_recoil))
                        current_row.append(weapon_recoil)
                except (KeyError, IndexError) as e:
                    try:
                        weapon_recoil = data['RefireModifier']
                        if logging:
                            print('No recoil in modes, defaulting to base', 'recoil ' + str(weapon_recoil))
                        current_row.append(weapon_recoil)
                    except KeyError:
                        if logging:
                            print('No RefireModifier on this weapon')
                        current_row.append(0)

                # Weapon base mode module
                try:
                    weapon_base_damage = 0
                    for i in range(len(data['Modes'])):  # For loop to iterate over the number of Modes found
                        if logging:
                            print('Base mode check', i)
                        try:
                            if data['Modes'][i]['isBaseMode']:
                                weapon_base_damage = (data['Damage'] + data['Modes'][i]['DamagePerShot']) * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired'])
                        except KeyError:  # if no DamagePerShot in mode found
                            if logging:
                                print('No DamagePerShot in modes, checking for extra shots in mode')
                            try:
                                weapon_base_damage = data['Damage'] * data['ProjectilesPerShot'] * (data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired'])
                            except KeyError:  # if no ShotsWhenFired in mode found
                                if logging:
                                    print('Weapon has no extra shots in modes, using base values')
                                weapon_base_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])
                except KeyError:  # This will catch errors when a weapon has no modes.
                    if logging:
                        print('No modes field exists on weapon, reverting to base values')
                    weapon_base_damage = data['Damage'] * (data['ProjectilesPerShot'] * data['ShotsWhenFired'])  # damage = damage per shot * projectilespershot
                if logging:
                    print("Base weapon damage ", weapon_base_damage)
                weapon_base_damage *= weapon_damage_multiplier
                current_row.append(weapon_base_damage)

                # Weapon most damaging ammotype damage value module
                try:
                    if ammotype_dam_dict[data['AmmoCategory']] == 0:
                        if logging:
                            print('Weapon ammo adds no bonus damage')
                        current_row.append(0)
                    else:
                        try:
                            current_row.append(ammotype_dam_dict[data['AmmoCategory']] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))
                            if logging:
                                print('Combined ammo salvo value is ', ammotype_dam_dict[data['AmmoCategory']] * (
                                            data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))
                        except KeyError:
                            if logging:
                                print('Weapon has no one of ammo, shotswhenfired, or modes. Checking other options')
                            try:
                                if data['ShotsWhenFired'] == 0:
                                    current_row.append(ammotype_dam_dict[data['AmmoCategory']])
                                    if logging:
                                        print('Weapon has no modes but combined ammo salvo value is ',
                                              ammotype_dam_dict[data['AmmoCategory']])
                                else:
                                    current_row.append(ammotype_dam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
                                    if logging:
                                        print('Weapon has no modes but combined ammo salvo value is ',
                                              ammotype_dam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
                            except KeyError:
                                try:
                                    current_row.append(ammotype_dam_dict[data['AmmoCategory']])
                                    if logging:
                                        print('Weapon has no modes or shots but combined ammo salvo value is ',
                                              ammotype_dam_dict[data['AmmoCategory']])
                                except KeyError:
                                    current_row.append(0)
                                    if logging:
                                        print('Weapon has no damage on ammo')
                except KeyError:
                    if logging:
                        print('Weapon has no ammo')
                    current_row.append('N/A')
                except IndexError:
                    if not data['Modes']: # Checks if Modes field exists but is empty
                        if logging:
                            print('Modes field exists on weapon but is empty, reverting to base values')
                        try:
                            if data['ShotsWhenFired'] == 0:
                                current_row.append(ammotype_dam_dict[data['AmmoCategory']])
                                if logging:
                                    print('Weapon has no modes but combined ammo salvo value is ',
                                          ammotype_dam_dict[data['AmmoCategory']])
                            else:
                                current_row.append(ammotype_dam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
                                if logging:
                                    print('Weapon has no modes but combined ammo salvo value is ',
                                          ammotype_dam_dict[data['AmmoCategory']] * data['ShotsWhenFired'])
                        except KeyError:
                            try:
                                current_row.append(ammotype_dam_dict[data['AmmoCategory']])
                                if logging:
                                    print('Weapon has no modes or shots but combined ammo salvo value is ',
                                          ammotype_dam_dict[data['AmmoCategory']])
                            except KeyError:
                                current_row.append(0)
                                if logging:
                                    print('Weapon has no damage on ammo and a Modes field on weapon that is empty')
                                    current_row.append('N/A')

                # Weapon most damaging ammotype module
                try:
                    pattern = '\w*.json'
                    match_var = re.search(pattern, ammotype_dam_best_dict[data['AmmoCategory']])
                    current_row.append(match_var.group()[:-5])
                    if logging:
                        print('Best ammo is ' + match_var.group()[:-5])
                except (KeyError, TypeError) as e:
                    current_row.append('N/A')
                    if logging:
                        traceback.print_exc()
                        print('Weapon has no ammo category')
                except AttributeError:
                    if logging:
                        traceback.print_exc()
                    current_row.append(ammotype_dam_best_dict[data['AmmoCategory']])

                # Weapon AOE damage and radius module
                if 'TAG' in weapon_name:
                    if logging:
                        print('TAG you are it!')
                        print(weapon_name)
                    try:
                        weapon_damage_AOE = data['deferredEffect']['AOEDamage']
                    except (KeyError, IndexError):
                        weapon_damage_AOE = 0
                    try:
                        weapon_heatdamage_AOE = data['deferredEffect']['AOEHeatDamage']
                    except (KeyError, IndexError):
                        weapon_heatdamage_AOE = 0
                    try:
                        weapon_AOE_radius = data['deferredEffect']['AOERange']
                    except (KeyError, IndexError):
                        weapon_AOE_radius = 0
                    current_row.append(weapon_damage_AOE)
                    current_row.append(weapon_heatdamage_AOE)
                    current_row.append(weapon_AOE_radius)
                else:
                    try: # TODO capture ammo AOE Heatdam in dict and use here
                        weapon_damage_AOE = (data['AOEDamage'] + ammotype_dam_AOE_dict[data['AmmoCategory']])
                    except KeyError:
                        try:
                            weapon_damage_AOE = ammotype_dam_AOE_dict[data['AmmoCategory']]
                        except KeyError:
                            weapon_damage_AOE = 0
                    try:
                        weapon_heatdamage_AOE = (data['AOEHeatDamage'] + ammotype_heatdam_AOE_dict[data['AmmoCategory']])
                    except KeyError:
                        try:
                            weapon_heatdamage_AOE = ammotype_heatdam_AOE_dict[data['AmmoCategory']]
                        except KeyError:
                            weapon_heatdamage_AOE = 0
                    try:
                        weapon_AOE_radius = data['AOERange']
                    except KeyError:
                        weapon_AOE_radius = 0
                        if logging:
                            print('No AOE in base, checking for modes or ammo')

                        try:
                            for i in range(len(data['Modes'])):
                                if data['Modes'][i]['AOECapable']:

                                    if logging:
                                        print('Weapon has AOE capability in Mode')
                                    weapon_damage_AOE = (data['Modes'][i]['AOEDamage'] + ammotype_dam_AOE_dict[data['AmmoCategory']]) * data['Modes'][i]['ShotsWhenFired']
                                    weapon_AOE_radius = data['Modes'][i]['AOERange']
                        except KeyError:
                            if logging:
                                print('No AOE in modes either, checking for ammo')
                            try:
                                if ammotype_dam_AOE_dict[data['AmmoCategory']] > 0:
                                    weapon_damage_AOE = ammotype_dam_AOE_dict[data['AmmoCategory']] * data['ShotsWhenFired']
                                    weapon_AOE_radius = ammotype_radius_AOE_dict[data['AmmoCategory']]
                            except KeyError:
                                weapon_damage_AOE = 0
                                weapon_AOE_radius = 0
                    current_row.append(weapon_damage_AOE)
                    current_row.append(weapon_heatdamage_AOE) # TODO this still doesn't check modes, is there any weapons with AOE HeatDamage in modes at all?
                    current_row.append(weapon_AOE_radius)

                try:
                    pattern = '\w*.json'
                    match_var = re.search(pattern, ammotype_dam_AOE_best_dict[data['AmmoCategory']])
                    current_row.append(match_var.group()[:-5])
                    if logging:
                        print('Best ammo is ' + match_var.group()[:-5])
                except (KeyError, TypeError) as e:
                    if logging:
                        traceback.print_exc()
                    current_row.append('N/A')
                    if logging:
                        print('Weapon has no ammo category')
                except AttributeError:
                    if logging:
                        traceback.print_exc()
                    current_row.append(ammotype_dam_AOE_best_dict[data['AmmoCategory']])

                # Damage variance module
                try:
                    weapon_damage_variance = data['DamageVariance']
                    if logging:
                        print('Dam Var ' + str(weapon_damage_variance))
                    current_row.append(weapon_damage_variance)
                except KeyError:
                    if logging:
                        print('No damage variance key!?')
                    current_row.append(0)

                # DamageNotDivided check on weapon
                weapon_DamageNotDivided = False
                try:
                    if data['DamageNotDivided'] and data['ImprovedBallistic'] and data['BallisticDamagePerPallet']:
                        weapon_DamageNotDivided = True
                        if logging:
                            print('Weapon DamageNotDivided, ImprovedBallistic, and BallisticDamagePerPallet are all true. This weapon will not have its heat and stability damage divided by ProjectilesPerShot.')
                except KeyError:
                    if logging:
                        print('Weapon will have normal DamageNotDivided and heat and stability damage will be divided by ProjectilesPerShot')

                # Weapon stability damage module
                if not weapon_DamageNotDivided:  # instability is divided among all projectiles per shot
                    if logging:
                        print('DamageNotDivided false')
                    try:
                        weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * data['InstabilityMultiplier'] * data['Modes']['InstabilityMultiplier'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))  # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                        if logging:
                            print('Stability dam ' + str(weapon_stability_damage))
                        current_row.append(weapon_stability_damage)
                    except (KeyError, IndexError, TypeError):
                        if logging:
                            print('No modes or no other mode related key, trying another combo (1st try)')
                        try:
                            weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * data['Modes']['InstabilityMultiplier'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))  # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                            if logging:
                                print('Stability dam ' + str(weapon_stability_damage))
                            current_row.append(weapon_stability_damage)
                        except (KeyError, IndexError, TypeError):
                            if logging:
                                print('No modes or no other mode related key, trying another combo (2nd try)')
                            try:
                                weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))  # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                                if logging:
                                    print('Stability dam ' + str(weapon_stability_damage))
                                current_row.append(weapon_stability_damage)
                            except (KeyError, IndexError, TypeError):
                                if logging:
                                    print('No modes or no other mode related key, trying another combo (3rd try)')
                                try:
                                    weapon_stability_damage = math.ceil(data['Instability'] * (data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']))  # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                                    if logging:
                                        print('Stability dam ' + str(weapon_stability_damage))
                                    current_row.append(weapon_stability_damage)
                                except (KeyError, IndexError):
                                    if logging:
                                        print('No modes, trying base values')
                                    try:
                                        weapon_stability_damage = math.ceil(data['Instability'] * data['ShotsWhenFired'])  # stability damage = stability damage per shot * shotswhenfired
                                        if logging:
                                            print('Stability dam ' + str(weapon_stability_damage))
                                        current_row.append(weapon_stability_damage)
                                    except KeyError:
                                        if logging:
                                            print('No Stability damage key on this weapon!?')
                                        current_row.append(0)

                elif weapon_DamageNotDivided:  # Instability is not divided up across projectiles per shot and is applied fully per projectile.
                    if logging:
                        print('DamageNotDivided true')
                    try: # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                        weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * data['InstabilityMultiplier'] * data['Modes']['InstabilityMultiplier'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']))
                        if logging:
                            print('Stability dam ', str(weapon_stability_damage))
                        current_row.append(weapon_stability_damage)
                    except (KeyError, IndexError, TypeError):
                        if logging:
                            print('No modes or no other mode related key, trying another combo (1st try)')
                        try: # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                            weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * data['Modes']['InstabilityMultiplier'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']))
                            if logging:
                                print('Stability dam ',  str(weapon_stability_damage))
                            current_row.append(weapon_stability_damage)
                        except (KeyError, IndexError, TypeError):
                            if logging:
                                print('No modes or no other mode related key, trying another combo (2nd try)')
                            try:
                                weapon_stability_damage = math.ceil((data['Instability'] + data['Modes']['Instability']) * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot']))  # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                                if logging:
                                    print('Stability dam ' + str(weapon_stability_damage))
                                current_row.append(weapon_stability_damage)
                            except (KeyError, IndexError, TypeError):
                                if logging:
                                    print('No modes or no other mode related key, trying another combo (3rd try)')
                                try:
                                    weapon_stability_damage = math.ceil(data['Instability'] * ((data['ShotsWhenFired'] + data['Modes'][max_dam_mode]['ShotsWhenFired']) * data['ProjectilesPerShot'])) # stability damage = stability damage per shot * (shotswhenfired + shotswhenfired in modes)
                                    if logging:
                                        print('Stability dam ' + str(weapon_stability_damage))
                                    current_row.append(weapon_stability_damage)
                                except (KeyError, IndexError):
                                    if logging:
                                        print('No modes, trying base values')
                                    try:
                                        weapon_stability_damage = math.ceil(data['Instability'] * (data['ShotsWhenFired'] * data['ProjectilesPerShot']))  # stability damage = stability damage per shot * shotswhenfired
                                        if logging:
                                            print('Stability dam ' + str(weapon_stability_damage))
                                        current_row.append(weapon_stability_damage)
                                    except KeyError:
                                        if logging:
                                            print('No Stability damage key on this weapon!?')
                                        current_row.append(0)


                # Weapon heat damage and multiplier module (includes ammo and modes)
                try:
                    weapon_basedam = data['Damage']
                    if logging:
                        print(data['Damage'], ' weapon BaseDamage')
                except KeyError:
                    if logging:
                        print('No BaseDamage on this weapon, weapon_basedam is zero')
                    weapon_basedam = 0
                try:
                    weapon_HeatDam = data['HeatDamage']
                    if logging:
                        print(data['HeatDamage'], ' weapon base HeatDamage')
                except KeyError:
                    if logging:
                        print('No HeatDamage on base weapon')
                    weapon_HeatDam = 0
                try:
                    weapon_dam_divided = weapon_basedam / weapon_HeatDam
                    if logging:
                        print(weapon_dam_divided, ' is the result of dividing weapon_basedam by weapon_Heatdam')
                except ZeroDivisionError:
                    if logging:
                        print('ZeroDivisionError dividing weapon_basedam by weapon_Heatdam, setting value to 1')
                    weapon_dam_divided = 1
                try:
                    weapon_HeatDamagePerShot = data['HeatDamagePerShot']
                    if logging:
                        print(data['HeatDamagePerShot'], ' base HeatDamagePerShot in base weapon')
                except KeyError:
                    if logging:
                        print('No HeatDamagePerShot on base weapon')
                    weapon_HeatDamagePerShot = 0
                try:
                    weapon_HeatMultiplier = data['HeatMultiplier']
                    if logging:
                        print(data['HeatMultiplier'], ' base HeatMultiplier in base weapon')
                except KeyError:
                    if logging:
                        print('No HeatMultiplier on base weapon')
                    weapon_HeatMultiplier = 1
                try:
                    weapon_ShotsWhenFired = data['ShotsWhenFired']
                    if logging:
                        print(data['ShotsWhenFired'], ' ShotsWhenFired on base weapon')
                except KeyError:
                    if logging:
                        print('No ShotsWhenFired on weapon base, ShotsWhenFired is 1 to avoid multiplying by zero')
                    weapon_ShotsWhenFired = 1 # TODO this may be an issue for weapons with shotwhenfired only in modes? Is that a thing?
                try:
                    weapon_ProjectilesPerShot = data['ProjectilesPerShot']
                    if logging:
                        print(data['ProjectilesPerShot'], ' ProjectilesPerShot on base weapon')
                except KeyError:
                    if logging:
                        print('No ProjectilesPerShot on weapon base, ProjectilesPerShot is 1 to avoid multiplying by zero')
                    weapon_ProjectilesPerShot = 1 # TODO this may be an issue for weapons with ProjectilesPerShot  only in modes? Is that a thing?
                try:  # this trait is to confirm which formula to use for heat calculation
                    weapon_AlternateHeatDamageCalc = data['AlternateHeatDamageCalc']
                    if logging:
                        print(data['AlternateHeatDamageCalc'], ' AlternateHeatDamageCalc in base weapon')
                except KeyError:
                    if logging:
                        print('No AlternateHeatDamageCalc in base weapon')
                    weapon_AlternateHeatDamageCalc = False
                try:
                    AmmoHeatDamagePerShot = ammotype_heatdam_dict[data['AmmoCategory']]
                except KeyError:
                    AmmoHeatDamagePerShot = 0
                    if logging:
                        print('No Ammo associated with this weapon, AmmoHeatDamagePerShot is zero')
                try:
                    AmmoHeatMultiplier = ammotype_heatdam_multi_dict[data['AmmoCategory']]
                except KeyError:
                    AmmoHeatMultiplier = 1
                    if logging:
                        print('No Ammo associated with this weapon, AmmoHeatMultiplier is zero')

                # Weapon heat damage module
                # TODO WIP weapon heatdamage update
                max_mode_heatdam = 0  # set value of highest additional heatdamage in modes
                try:
                    for i in range(len(data['Modes'])):  # for loop to iterate over the number of Modes found
                        ProjectilesPerShot = 0
                        ShotsWhenFired = 0
                        if logging:
                            print('Heatdamage mode', i)
                        # check for traits in mode
                        try:
                            mode_HeatDamagePerShot = data['Modes'][i]['HeatDamagePerShot']
                            if logging:
                                print(data['Modes'][i]['HeatDamagePerShot'], ' HeatDamagePerShot in this mode')
                        except KeyError:
                            if logging:
                                print('No HeatDamagePerShot on this mode, mode_HeatDamagePerShot is zero')
                            mode_HeatDamagePerShot = 0
                        try:
                            mode_HeatDamage = data['Modes'][i]['HeatDamage']
                            if logging:
                                print(data['Modes'][i]['HeatDamage'], ' HeatDamage in this mode')
                        except KeyError:
                            if logging:
                                print('No HeatDamage on this mode, mode_HeatDamage is zero')
                            mode_HeatDamage = 0
                        try:
                            mode_HeatDamageMultiplier = data['Modes'][i]['HeatMultiplier']
                            if logging:
                                print(data['Modes'][i]['HeatDamageMultiplier'], ' HeatDamageMultiplier in this mode')
                        except KeyError:
                            if logging:
                                print('No HeatDamageMultiplier on this mode, mode_HeatDamageMultiplier is one')
                            mode_HeatDamageMultiplier = 1
                        try:
                            mode_ProjectilesPerShot = data['Modes'][i]['ProjectilesPerShot']
                            if logging:
                                print(data['Modes'][i]['ProjectilesPerShot'], ' ProjectilesPerShot in this mode')
                        except KeyError:
                            if logging:
                                print('No ProjectilesPerShot on this mode, mode_ProjectilesPerShot is 0')
                            mode_ProjectilesPerShot = 0
                        ProjectilesPerShot = mode_ProjectilesPerShot + weapon_ProjectilesPerShot
                        try:
                            mode_ShotsWhenFired = data['Modes'][i]['ShotsWhenFired']
                            if logging:
                                print(mode_ShotsWhenFired, ' ShotsWhenFired on this mode')
                        except KeyError:
                            if logging:
                                print('No ShotsWhenFired on mode, mode_ShotsWhenFired is 0')
                            mode_ShotsWhenFired = 0
                        ShotsWhenFired = mode_ShotsWhenFired + weapon_ShotsWhenFired # TODO i think this is the problem somehow
                        try:  # this trait is to confirm which formula to use for heat calculation
                            mode_AlternateHeatDamageCalc = data['Modes'][i]['AlternateHeatDamageCalc']
                            if logging:
                                print(data['Modes'][i]['AlternateHeatDamageCalc'], ' AlternateHeatDamageCalc in this mode')
                        except KeyError:
                            if logging:
                                print('No AlternateHeatDamageCalc on this mode, AlternateHeatDamageCalc is False')
                            mode_AlternateHeatDamageCalc = False

                        if weapon_DamageNotDivided:
                            if logging:
                                print('Modes check, weapon includes DamageNotDivided, heat damage will be applied to all ProjectilesPerShot and not divided among them')
                            if mode_AlternateHeatDamageCalc or weapon_AlternateHeatDamageCalc:  # Uses heat damage formula one (WeaponBaseDamage + WeaponHeatDamage + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier
                                if logging:
                                    print('AlternateHeatDamageCalc is true in mode, using heatdamage formula one')
                                if ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier) * ProjectilesPerShot * ShotsWhenFired > max_mode_heatdam:
                                    max_mode_heatdam = ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier) * ProjectilesPerShot * ShotsWhenFired
                                    max_heatdam_mode = i
                                    if logging:
                                        print('The new best mode heatdamage is ', max_mode_heatdam, '. Found in mode, ', max_heatdam_mode)
                            else:  # Uses heat damage formula two this is by far the most common (WeaponHeatDam + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier * WeaponBaseDamage / WeaponHeatDamage
                                if logging:
                                    print('AlternateHeatDamageCalc is false, using heatdamage formula two')
                                if ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ProjectilesPerShot * ShotsWhenFired > max_mode_heatdam:
                                    max_mode_heatdam = ((weapon_HeatDam + AmmoHeatDamagePerShot + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ProjectilesPerShot * ShotsWhenFired
                                    max_heatdam_mode = i
                                    if logging:
                                        print('The new best mode heatdamage is ', max_mode_heatdam, '. Found in mode, ', max_heatdam_mode)
                        else:  # DamageNotDivided is false
                            if logging:
                                print('Modes check, weapon does not include DamageNotDivided, heat damage will be applied divided normally across all ProjectilesPerShot')
                            if mode_AlternateHeatDamageCalc or weapon_AlternateHeatDamageCalc:  # Uses heat damage formula one (WeaponBaseDamage + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier
                                if logging:
                                    print('AlternateHeatDamageCalc is true in mode or base weapon, using heatdamage formula one')
                                if ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier) * ShotsWhenFired > max_mode_heatdam:
                                    max_mode_heatdam = ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier) * ShotsWhenFired
                                    max_heatdam_mode = i
                                    if logging:
                                        print('The new best mode heatdamage is ', max_mode_heatdam, '. Found in mode, ', max_heatdam_mode)
                            else:  # Uses heat damage formula two this is by far the most common (WeaponHeatDam + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier * WeaponBaseDamage / WeaponHeatDamage
                                if logging:
                                    print('AlternateHeatDamageCalc is false in mode or base weapon, using heatdamage formula two')
                                if ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ShotsWhenFired > max_mode_heatdam:
                                    max_mode_heatdam = ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot + mode_HeatDamage + mode_HeatDamagePerShot) * AmmoHeatMultiplier * mode_HeatDamageMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ShotsWhenFired
                                    max_heatdam_mode = i
                                    if logging:
                                        print('The new best mode heatdamage is ', max_mode_heatdam, '. Found in mode, ', max_heatdam_mode)
                except KeyError:
                    if logging:
                        print('Weapon has no modes, using base values only')
                    # check for traits in base
                    try:
                        weapon_HeatMultiplier = data['HeatMultiplier']
                        if logging:
                            print(data['HeatMultiplier'], ' base HeatMultiplier in base weapon')
                    except KeyError:
                        if logging:
                            print('No HeatMultiplier on base weapon')
                        weapon_HeatMultiplier = 1
                    try:
                        weapon_HeatDamagePerShot = data['HeatDamagePerShot']
                        if logging:
                            print(data['HeatDamagePerShot'], ' base HeatDamagePerShot in base weapon')
                    except KeyError:
                        if logging:
                            print('No HeatDamagePerShot on base weapon')
                        weapon_HeatDamagePerShot = 0
                    try:
                        weapon_ProjectilesPerShot = data['ProjectilesPerShot']
                        if logging:
                            print(data['ProjectilesPerShot'], ' ProjectilesPerShot on base weapon')
                    except KeyError:
                        if logging:
                            print('No ProjectilesPerShot on weapon base, ProjectilesPerShot is 1 to avoid multiplying by zero')
                        weapon_ProjectilesPerShot = 0
                    ProjectilesPerShot = weapon_ProjectilesPerShot
                    if ProjectilesPerShot == 0:
                        ProjectilesPerShot = 1
                    try:
                        weapon_ShotsWhenFired = data['ShotsWhenFired']
                        if logging:
                            print(data['ShotsWhenFired'], ' ShotsWhenFired on base weapon')
                    except KeyError:
                        if logging:
                            print('No ShotsWhenFired on weapon base, ShotsWhenFired is 1 to avoid multiplying by zero')
                        weapon_ShotsWhenFired = 0
                    ShotsWhenFired = weapon_ShotsWhenFired
                    if ShotsWhenFired == 0:
                        ShotsWhenFired = 1
                    try:  # this trait is to confirm which formula to use for heat calculation
                        AlternateHeatDamageCalc = data['AlternateHeatDamageCalc']
                        if logging:
                            print(data['AlternateHeatDamageCalc'], ' AlternateHeatDamageCalc in base weapon')
                    except KeyError:
                        if logging:
                            print('No AlternateHeatDamageCalc in base weapon')
                        AlternateHeatDamageCalc = False
                    try:
                        AmmoHeatDamagePerShot = ammotype_heatdam_dict[data['AmmoCategory']]
                    except KeyError:
                        AmmoHeatDamagePerShot = 0
                        if logging:
                            print('No Ammo associated with this weapon, AmmoHeatDamagePerShot is zero')
                    try:
                        AmmoHeatMultiplier = ammotype_heatdam_multi_dict[data['AmmoCategory']]
                    except KeyError:
                        AmmoHeatMultiplier = 1
                        if logging:
                            print('No Ammo associated with this weapon, AmmoHeatMultiplier is zero')

                    if weapon_DamageNotDivided:
                        if logging:
                            print('Weapon includes DamageNotDivided, heat damage will be applied to all ProjectilesPerShot and not divided among them')
                        if AlternateHeatDamageCalc:  # Uses heat damage formula one (WeaponBaseDamage + WeaponHeatDamage + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier
                            if logging:
                                print('AlternateHeatDamageCalc is true in base weapon, using heatdamage formula one')
                            if ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * weapon_HeatMultiplier * AmmoHeatMultiplier) * ProjectilesPerShot * ShotsWhenFired > max_mode_heatdam:
                                max_mode_heatdam = ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * weapon_HeatMultiplier * AmmoHeatMultiplier) * ProjectilesPerShot * ShotsWhenFired
                                if logging:
                                    print('The new best heatdamage is ', max_mode_heatdam, '. Found in base weapon')
                        else:  # Uses heat damage formula two this is by far the most common (WeaponHeatDam + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier * WeaponBaseDamage / WeaponHeatDamage
                            if logging:
                                print('AlternateHeatDamageCalc is false in base weapon, using heatdamage formula two')
                            if ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * AmmoHeatMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ProjectilesPerShot * ShotsWhenFired > max_mode_heatdam:
                                max_mode_heatdam = ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * AmmoHeatMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ProjectilesPerShot * ShotsWhenFired
                                if logging:
                                    print('The new best heatdamage is ', max_mode_heatdam, '. Found in base weapon')
                    else:  # DamageNotDivided is false
                        if logging:
                            print('No modes base check weapon does not include DamageNotDivided, heat damage will be applied divided normally across all ProjectilesPerShot')
                        if AlternateHeatDamageCalc:  # Uses heat damage formula one (WeaponBaseDamage + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier
                            if logging:
                                print('AlternateHeatDamageCalc is true, using heatdamage formula one')
                            if ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * weapon_HeatMultiplier * AmmoHeatMultiplier) * ShotsWhenFired > max_mode_heatdam:
                                max_mode_heatdam = ((weapon_basedam + weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * weapon_HeatMultiplier * AmmoHeatMultiplier) * ShotsWhenFired
                                if logging:
                                    print('The new best heatdamage is ', max_mode_heatdam, '. Found in base weapon')
                        else:  # Uses heat damage formula two this is by far the most common (WeaponHeatDam + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier * WeaponBaseDamage / WeaponHeatDamage
                            if logging:
                                print('AlternateHeatDamageCalc is false, using heatdamage formula two')
                            if ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * AmmoHeatMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ShotsWhenFired > max_mode_heatdam:
                                max_mode_heatdam = ((weapon_HeatDam + weapon_HeatDamagePerShot + AmmoHeatDamagePerShot) * AmmoHeatMultiplier * weapon_HeatMultiplier * weapon_dam_divided) * ShotsWhenFired
                                if logging:
                                    print('The new best heatdamage is ', max_mode_heatdam, '. Found in base weapon')

                weapon_maxheat_damage = max_mode_heatdam
                current_row.append(weapon_maxheat_damage)

                # Weapon most heat damage ammotype damage value module
                try:
                    current_row.append(ammotype_heatdam_dict[data['AmmoCategory']] * AmmoHeatMultiplier)
                except KeyError:
                    if logging:
                        print('Weapon probably has no ammo')
                    current_row.append(0)


                # Weapon most heat damage ammotype module
                try:
                    if ammotype_heatdam_dict[data['AmmoCategory']] == 0:
                        current_row.append('N/A')
                        if logging:
                            print('Weapon ammo has no heat damage variant')
                    else:
                        pattern = '\w*.json'
                        match_var = re.search(pattern, ammotype_heatdam_best_dict[data['AmmoCategory']])
                        current_row.append(match_var.group()[:-5])
                        if logging:
                            print('Best heat ammo is ' + match_var.group()[:-5])
                except (KeyError, TypeError) as e:
                    if logging:
                        traceback.print_exc()
                    current_row.append('N/A')
                    if logging:
                        print('Weapon has no ammo category')
                except AttributeError:
                    if logging:
                        traceback.print_exc()
                    if ammotype_heatdam_dict[data['AmmoCategory']] == 0:
                        current_row.append('N/A')
                        if logging:
                            print('Weapon ammo has no heat damage variant')
                    else:
                        current_row.append(ammotype_heatdam_best_dict[data['AmmoCategory']])

                # Weapon firing heat module
                try:
                    weapon_firing_heat = data['HeatGenerated'] + data['Modes'][max_dam_mode]['HeatGenerated']
                    if logging:
                        print('HeatGenerated1 ' + str(weapon_firing_heat))
                    current_row.append(weapon_firing_heat)
                except (KeyError, IndexError) as e:
                    if logging:
                        print('No modes, using base values')
                    try:
                        weapon_firing_heat = data['HeatGenerated']
                        if logging:
                            print('No firing heat in modes, defaulting to base ', 'Firing Heat ' + str(weapon_firing_heat))
                        current_row.append(weapon_firing_heat)
                    except KeyError:
                        if logging:
                            print('No weapon firing heat key on this weapon')
                        current_row.append(0)

                # Weapon jamming chance module
                try:
                    weapon_flat_jam = 0
                    weapon_flat_jam = data['FlatJammingChance']
                    # FlatJammingChance is handled backwards to ShotsWhenFired. Most mode weapons don't have a
                    # base FlatJammingChance key and ONLY have them in the modes.
                    # Check for base FIRST then check for modes based on that.
                    try:
                        weapon_flat_jam = (data['FlatJammingChance'] + data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)
                        if logging:
                            print('Flat jamming chance ' + str(weapon_flat_jam))
                    except (KeyError, IndexError) as e:
                        weapon_flat_jam = (data['FlatJammingChance'] * 100)
                        if logging:
                            print('No modes, reverting to base jam chance ' + str(weapon_flat_jam) + '%')
                except KeyError:
                    try:
                        weapon_flat_jam = (data['Modes'][max_dam_mode]['FlatJammingChance'] * 100)
                        if logging:
                            print('No base flat jamming chance key, using modes ' + str(weapon_flat_jam) + '%')
                    except (KeyError, IndexError) as e:
                        try:
                            pattern = '^wr-jam_chance_multiplier-[0-9]+' # TODO this has been deprecated by 1.0.4 release can remove but will be replaced by 'RecoilJammingChance'
                            for i in data['ComponentTags']['items']:
                                try:
                                    multiplier = int(re.match(pattern, i).group()[-1])
                                    weapon_flat_jam = weapon_recoil * multiplier
                                except AttributeError:
                                    continue
                        except (KeyError, IndexError, TypeError) as e:
                            if logging:
                                traceback.print_exc()
                                print('No flat jamming chance on this weapon.')
                            weapon_flat_jam = 0
                if weapon_flat_jam > 100:
                    weapon_flat_jam = 100
                if logging:
                    print('Weapon jamming chance is ' + str(weapon_flat_jam))
                current_row.append(weapon_flat_jam)

                # weapon can misfire module
                try:
                    weapon_misfire = 'False'
                    if data['DamageOnJamming']:
                        weapon_misfire = 'True'
                    else:
                        try:
                            if data['Modes'][max_dam_mode]['DamageOnJamming']:
                                weapon_misfire = 'True in Mode'
                        except KeyError:
                            if logging:
                                print('Weapon has no modes, or no base, checking for modes')
                except KeyError:
                    try:
                        if data['Modes'][max_dam_mode]['DamageOnJamming']:
                            weapon_misfire = 'True in Mode'
                    except (KeyError, IndexError) as e:
                        if logging:
                            print('Weapon has no modes')
                try:
                    if 'wr-damage_when_jam' in data['ComponentTags']['items']:
                        weapon_misfire = 'True'
                except KeyError:
                    if logging:
                        print('No jamming on this weapon')
                if weapon_misfire == 'False':
                    try:
                        for i in data['Custom']['BonusDescriptions']:
                            if 'Explodium' in i:  # this verifies that the weapon descriptions do not list misfires when traits do not have them
                                excepted_files.append(item)
                                if logging:
                                    print('Explodium found in BonusDescriptions but weapon_misfire is False, adding to excepted_files list')
                    except KeyError:
                        if logging:
                            print('No Custom categories or BonusDescriptions')
                current_row.append(weapon_misfire)

                # damage compare modules
                try:
                    weapon_damage_per_heat = float("{:.2f}".format(float(weapon_damage + weapon_damage_AOE) / (float(weapon_firing_heat))))
                    if logging:
                        print(weapon_damage_per_heat)
                    current_row.append(weapon_damage_per_heat)
                except ZeroDivisionError:
                    if logging:
                        print('Divide by Zero!')
                    current_row.append(0)

                try:
                    weapon_damage_per_slot = float(
                        "{:.2f}".format(float(weapon_damage + weapon_damage_AOE) / (float(weapon_slots))))
                    if logging:
                        print(weapon_damage_per_slot)
                    current_row.append(weapon_damage_per_slot)
                except ZeroDivisionError:
                    if logging:
                        print('Divide by Zero!')
                    current_row.append(0)

                try:
                    weapon_damage_per_ton = float(
                        "{:.2f}".format(float(weapon_damage + weapon_damage_AOE) / (float(weapon_tonnage))))
                    if logging:
                        print(weapon_damage_per_ton)
                    current_row.append(weapon_damage_per_ton)
                except ZeroDivisionError:
                    if logging:
                        print('Divide by Zero!')
                    current_row.append(0)

                # Standard crit module against location
                # CritChanceMin crit from Core\GameConstants.json of 0.5 overwritten by Core\CustomAmmoCategories\AIM_settings.json to 0.56
                # (Crit chance minimum is 0.56) outside of this it can go higher depending on remaining structure left in the location hit.
                # CritChanceVar = CritChanceZeroStructure - CritChanceFullStructure or (CritChanceVar = 0.7 - -0.15) (CritChanceVar = 0.85)
                # CritChanceBase = CritChanceFullStructure or (CritChanceBase = -0.15)
                # Now that we have all the basic variables, here is how it is applied.
                # CritChance = CritChanceBase += 1.0 - currentStructure of target / maxStructure of target * CritChanceVar or (-0.15 += (1.0 - currentStructure of target / maxStructure of target * 0.85)) * Crit multiplier
                # Example with an average medium mech CT at 50% structure in location hit
                # CritChance = -0.15 + (1.0 - 40 / 80 * 0.85)
                # This would equal 0.42499999999999993 but since our minimum crit chance is 0.56 it would be overridden.
                # As structure remaining goes down your crit chance goes up, with a value of 10 structure remaining you would have 0.74375
                try:
                    weapon_base_crit = -0.15 + (1.0 - 0.5) * 0.85
                    # This is kinda unnecessary right now since I am only calculating based on half the structure remaining which will always work out to under the minimum and need to be boosted to meet minimum.
                    # In the future I may use the different structure % values, so I will leave it as is.
                    # TODO future include fields for different values of remaining structure?
                    if weapon_base_crit < 0.56:
                        weapon_base_crit = 0.56
                    weapon_final_crit = weapon_base_crit * data['CriticalChanceMultiplier']
                    weapon_final_crit = weapon_final_crit * 100
                    current_row.append(data['CriticalChanceMultiplier'])
                    current_row.append(weapon_final_crit)
                except KeyError:
                    if logging:
                        print('No CriticalChanceMultiplier on this weapon')
                    current_row.append(0)
                    current_row.append(0)

                # TAC module
                # to get a comparable baseline for all weapons we will compare (1 + (1 - half APMaxArmorThickness/APMaxArmorThickness) * (weapon APArmorShardsMod)) Add column for TAC and TAC max armor, TAC chance will be based on 50% of max AP armor for every weapon.
                # APShardsMod = (1 + (1 - half APMaxArmorThickness/APMaxArmorThickness) * (weapon APArmorShardsMod))
                # APThicknessMod = (1.0 - half APMaxArmorThickness/weapon APMaxArmorThickness) This will always be 0.5!
                # weapon ap crit mod = weapon.APCriticalChanceMultiplier (if weapon.APCriticalChanceMultiplier = 0, weapon ap crit mod set to 1.0)
                # final TAC chance = basic crit chance (0.1) * APShardsMod * APThicknessMod * weapon ap crit mod
                # NOTE: RT settings currently require a shot to do damage equal to or greater than 45% of max armor to even have a chance of TAC
                # Relevant AIM setting below
                """/* A weapon must deal this much total damage to a location for through armour crit to roll.  Default 9.  Set to 0 for no threshold.
                   * A number between 0 and 1 (exclusive) means a fraction of max armour, 0 and -1 means a fraction of current armour,
                   * while 1 and above means a fixed damage threshold. */
                
                  "ThroughArmorCritThreshold": 0.45,
                """
                try:
                    weapon_AP_crit_chance_multiplier = data['APCriticalChanceMultiplier']
                    weapon_max_AP_thickness = data['APMaxArmorThickness']
                    AP_shards_mod = (1 + (1 - 0.5)) * (data['APArmorShardsMod'])  # hard coded to equal armor value of half of APMaxArmorThickness
                    AP_thickness_mod = 0.5  # hard coded value to represent percentage of APMaxArmorThickness remaining on target, this checks at 50%
                    weapon_TAC = float("{:0.6f}".format(0.1 * AP_shards_mod * AP_thickness_mod * weapon_AP_crit_chance_multiplier))
                    if logging:
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
                    if logging:
                        print('TAC KeyError, checking using default APCriticalChanceMultiplier')
                    try:
                        weapon_AP_crit_chance_multiplier = 1.0
                        weapon_max_AP_thickness = data['APMaxArmorThickness']
                        AP_shards_mod = (1 + (1 - 0.5)) * (
                        data['APArmorShardsMod'])  # hard coded to equal armor value of half of APMaxArmorThickness
                        AP_thickness_mod = 0.5  # hard coded value to represent percentage of APMaxArmorThickness remaining on target, this checks at 50%
                        weapon_TAC = float("{:0.6f}".format(0.1 * AP_shards_mod * AP_thickness_mod * weapon_AP_crit_chance_multiplier))
                        if logging:
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
                        if logging:
                            print('No TAC on this weapon')
                        current_row.append(0)
                        current_row.append(0)

                # Accuracy bonus module, negative is better
                try:
                    weapon_accuracy_mod = data['AccuracyModifier']
                    if logging:
                        print(weapon_accuracy_mod)
                except KeyError:
                    if logging:
                        print('Missing Base Accuracy Type')
                    weapon_accuracy_mod = 0
                current_row.append(weapon_accuracy_mod)

                # Evasion ignore module, positive is better
                try:
                    weapon_evasion_ignore = data['EvasivePipsIgnored']
                    if logging:
                        print(weapon_evasion_ignore)
                except KeyError:
                    if logging:
                        print('Missing Base Accuracy Type')
                    weapon_evasion_ignore = 0
                current_row.append(weapon_evasion_ignore)

                # Weapon range module
                try:
                    weapon_range_min = data['MinRange']
                    current_row.append(weapon_range_min)
                except KeyError:
                    if logging:
                        print('No minimum range on this weapon')

                try:
                    weapon_range_short = data['RangeSplit'][0]
                    current_row.append(weapon_range_short)
                except KeyError:
                    if logging:
                        print('No short range on this weapon')

                try:
                    weapon_range_medium = data['RangeSplit'][1]
                    current_row.append(weapon_range_medium)
                except KeyError:
                    if logging:
                        print('No medium range on this weapon')

                try:
                    weapon_range_long = data['RangeSplit'][2]
                    current_row.append(weapon_range_long)
                except KeyError:
                    if logging:
                        print('No long range on this weapon')

                try:
                    weapon_range_max = data['MaxRange']
                    current_row.append(weapon_range_max)
                except KeyError:
                    if logging:
                        print('No max range on this weapon')
                if logging:
                    print('Min ' + str(weapon_range_min) + ' Short ' + str(weapon_range_short) + ' Medium ' + str(weapon_range_medium) + ' Long ' + str(weapon_range_long) + ' Max ' + str(weapon_range_max))

                # Damage variance field module
                try:
                    weapon_distance_variance = data['DistantVariance'] * 100
                except KeyError:
                    if logging:
                        print('No Distance Variance on weapon')
                    weapon_distance_variance = 0
                current_row.append(weapon_distance_variance)

                # damage variance calculation module
                range_list = [weapon_range_min, weapon_range_short, weapon_range_medium, weapon_range_long,weapon_range_max]
                range_falloff_ratio_list = [0, 0, 0, 0, 0]
                range_falloff_total_damage = [0, 0, 0, 0, 0]
                try:
                    if data['isDamageVariation']:  # verify weapon uses damage variance
                        try:
                            if data['DistantVarianceReversed'] == False:
                                if data['DistantVariance'] > 0:
                                    # INPUT PROTECTION
                                    try:
                                        if data['DamageFalloffStartDistance'] > 1 / 1000:
                                            falloff_start = data['DamageFalloffStartDistance']
                                        elif data['DamageFalloffStartDistance'] < 1 / 1000:
                                            if logging:
                                                print('Falloff start value is zero, using medium value')
                                            falloff_start = weapon_range_medium
                                    except KeyError:
                                        if logging:
                                            print('No falloff start distance key, using medium value')
                                        falloff_start = weapon_range_medium
                                    try:
                                        if data['DamageFalloffEndDistance'] < falloff_start:
                                            falloff_end = weapon_range_max
                                        elif data['DamageFalloffEndDistance'] > falloff_start:
                                            falloff_end = data['DamageFalloffEndDistance']
                                    except KeyError:
                                        if logging:
                                            print('No falloff end distance, using max value')
                                        falloff_end = weapon_range_max
                                # GET RATIO
                                j = 0
                                for i in range_list:
                                    if (falloff_end - falloff_start > 1 / 1000):
                                        range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start))
                                    # DEFAULT
                                    if i < falloff_start:
                                        if logging:
                                            print('Range has no damage falloff')
                                        current_row.append(weapon_damage)
                                    else:  # DO THE THING
                                        current_row.append(float("{:.2f}".format(weapon_damage * (1.0 - range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))))
                                        if logging:
                                            print('Adding damage')
                                    j += 1
                            # reversed tree
                            elif data['DistantVarianceReversed'] == True:
                                if logging:
                                    print('Reversed Distance Variance')
                                try:
                                    if data['DamageFalloffStartDistance'] > 1 / 1000:
                                        falloff_start = data['DamageFalloffStartDistance']
                                    else:
                                        if logging:
                                            print('Falloff start value is zero, using minimum value')
                                        falloff_start = weapon_range_min
                                except KeyError:
                                    if logging:
                                        print('No falloff start distance key, using minimum value')
                                    falloff_start = weapon_range_min
                                try:
                                    if data['DamageFalloffEndDistance'] < falloff_start:
                                        falloff_end = weapon_range_medium
                                    else:
                                        falloff_end = data['DamageFalloffEndDistance']
                                    if logging:
                                        print('Falloff start ', falloff_start, 'Falloff end ', falloff_end)
                                except KeyError:
                                    if logging:
                                        print('No falloff end distance, using max value')
                                    falloff_end = weapon_range_max
                                ##GET RATIO
                                j = 0
                                for i in range_list:
                                    if (i <= falloff_end and falloff_end - falloff_start > 1 / 1000):
                                        range_falloff_ratio_list[j] = ((i - falloff_start) / (falloff_end - falloff_start))
                                    ##DEFAULT
                                    if i < falloff_start:
                                        if logging:
                                            print('Range has no damage falloff')
                                        current_row.append(weapon_damage)
                                    else:  # DO THE THING
                                        current_row.append(float("{:.2f}".format(weapon_damage * (data['DistantVariance'] + range_falloff_ratio_list[j] * (1.0 - data['DistantVariance'])))))
                                        if logging:
                                            print('Adding reversed damage')
                                    j += 1
                        except KeyError:
                            if logging:
                                print('No DistantVarianceReversed key on weapon!')
                            for i in range(5):
                                current_row.append(weapon_damage)
                except KeyError:
                    if logging:
                        print('No damage variance, using normal values')
                    for i in range(5):
                        current_row.append(weapon_damage)

                # AA Factor Module
                weapon_AAA_factor = 0.0
                try:
                    for i in data['statusEffects']:
                        for j in i:
                            if 'statisticData' in j:
                                if i[j]['statName'] == 'AAAFactor':
                                    weapon_AAA_factor = float(i[j]['modValue']) * 100
                except:
                    if logging:
                        print('No statusEffects?')
                current_row.append(weapon_AAA_factor)


                current_row.insert(9, current_row.pop(3))  #TODO this rearranges the current_row list to properly format it for the excel sheet; this should go bye bye in next version, just use variables and append them all at the end man!

                df2 = pandas.DataFrame([current_row], columns=columns_list)
                if logging:
                    print(df2)
                df = pandas.concat([df, df2])
            except UnicodeDecodeError:
                excepted_files.append(item)
                if logging:
                    print('Possible invalid character in JSON')
            except json.decoder.JSONDecodeError:
                possible_invalid_jsons.append(item)
                if logging:
                    print('Possible invalid JSON!')

    # AMS Modules
    for item in ams_file_list:
        with open(item) as f:
            if logging:
                print(item)
            try:
                data = json.load(f)
                current_row_ams = []
                # Initializing all loop variables in so any unused do not throw off row alignment by being empty
                basemode_ams_damage = 'N/A'
                basemode_ams_hitchance = 'N/A'
                basemode_ams_shots = 'N/A'
                basemode_ams_avg_damage = 'N/A'
                basemode_ams_heat = 'N/A'
                basemode_ams_jam = 'N/A'
                basemode_ams_maxrange = 'N/A'
                basemode_aams = 'N/A'

                # AMS hardpoint module
                try:
                    hardpoint_type = str(data['Category'])
                    if logging:
                        print(hardpoint_type)
                except KeyError:
                    if logging:
                        print('Missing Hardpoint Type')
                    try:
                        hardpoint_type = str(data['weaponCategoryID'])
                    except KeyError:
                        if logging:
                            print('Weapon has no Type?')
                        hardpoint_type = 'N/A'
                current_row_ams.append(hardpoint_type)

                # AMS type module
                try:
                    weapon_class = str(data['Type'])
                    if logging:
                        print(weapon_class)
                    current_row_ams.append(weapon_class)
                except KeyError:
                    if logging:
                        print('Missing Weapon Type')
                    current_row_ams.append('N/A')

                # AMS name module
                try:
                    if 'deprecated' in str(data['Description']['UIName']).lower():
                        if logging:
                            print('Deprecated in name, skipping')
                        filtered_files.append(item)
                        continue
                    weapon_name = str(data['Description']['UIName'])
                    if logging:
                        print(weapon_name)
                    current_row_ams.append(weapon_name)
                except KeyError:
                    # This will skip the file if it has no weapon UI name as this means it isn't valid or isn't used
                    if logging:
                        print('Missing AMS Name')
                    filtered_files.append(item)
                    continue

                # AMS Tonnage check module
                if hardpoint_type == 'Special':
                    try:
                        weapon_tonnage = data['Custom']['CarryLeftOverUsage']
                        current_row_ams.append(weapon_tonnage)
                    except KeyError:
                        weapon_tonnage = data['Tonnage']
                        if logging:
                            print('Tons ' + str(weapon_tonnage))
                elif hardpoint_type == 'SpecialMelee':
                    weapon_tonnage = data['Custom']['HandHeld']['Tonnage']
                    current_row_ams.append(weapon_tonnage)
                else:
                    try:
                        weapon_tonnage = data['Tonnage']
                        if logging:
                            print('Tons ' + str(weapon_tonnage))
                        current_row_ams.append(weapon_tonnage)
                        if weapon_tonnage > 50:  # this filters deprecated weapons that are 100 to 6666 tons
                            if logging:
                                print('Filtered out deprecated weapon by tonnage')
                            filtered_files.append(item)
                            continue
                    except:
                        if logging:
                            print('Missing Tonnage')
                        current_row_ams.append('N/A')

                # AMS slot size module
                try:
                    weapon_slots = data['InventorySize']
                    if logging:
                        print('Slots ' + str(weapon_slots))
                    current_row_ams.append(weapon_slots)
                except:
                    if logging:
                        print('Missing Weapon Slots')
                    current_row_ams.append('N/A')

                # AMS multi attack module
                ams_multi_attack = 1
                try:
                    ams_multi_attack = data['AMSActivationsPerTurn']
                except KeyError:
                    print('No ActivationsPerTurn on AMS, defaulting to 1')
                current_row_ams.append(ams_multi_attack)

                # AMS modes everything module
                try:
                    for i in range(len(data['Modes'])):
                        if logging:
                            print(i)
                        is_AMS = False
                        try:
                            if data['Modes'][i]['IsAMS'] or data['IsAMS']:
                                if logging:
                                    print('This mode or base is isAMS')
                                is_AMS = True
                        except KeyError:
                            if logging:
                                print('Missing isAMS key in either modes or base, checking base now')
                            try:
                                if data['IsAMS']:
                                    if logging:
                                        print('Base isAMS')
                                    is_AMS = True
                            except KeyError:
                                if logging:
                                    print('Missing isAMS key in both modes and base; either this is not an AMS or this mode is not an AMS')
                                continue
                        # base mode check
                        if is_AMS and data['Modes'][i]['isBaseMode'] and data['Modes'][i]['Id'] != 'Off' and data['Modes'][i]['Id'] != 'MG' and data['Modes'][i]['Id'] != 'Laser':
                            if logging:
                                print('This is the AMS base mode')
                            basemode_ams_damage = 0
                            try:
                                basemode_ams_damage = data['Modes'][i]['AMSDamage'] + data['AMSDamage'] + 1
                                if logging:
                                    print('Basemode AMS damage is ', str(basemode_ams_damage))
                            except KeyError:
                                try:
                                    basemode_ams_damage = data['Modes'][i]['AMSDamage'] + 1
                                except KeyError:
                                    try:
                                        if logging:
                                            print('No Mode AMS Damage, trying base')
                                        basemode_ams_damage = data['AMSDamage'] + 1
                                        if logging:
                                            print('Basemode AMS damage is ', str(basemode_ams_damage))
                                    except KeyError:
                                        if logging:
                                            print('No mode or base AMS Damage, defaulting to 1')
                                        basemode_ams_damage = 1

                            basemode_ams_hitchance = 0
                            try:
                                basemode_ams_hitchance = data['Modes'][i]['AMSHitChance']
                                if logging:
                                    print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
                            except KeyError:
                                if logging:
                                    print('No AMS Hitchance in mode, checking base')
                                try:
                                    basemode_ams_hitchance = data['AMSHitChance']
                                    if logging:
                                        print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
                                except KeyError:
                                    if logging:
                                        print('No AMS Hitchance at all!?')

                            basemode_ams_shots = 0
                            try:
                                basemode_ams_shots = data['ShotsWhenFired'] + data['Modes'][i]['ShotsWhenFired']
                                if logging:
                                    print('Basemode AMS ShotsWhenFired is ', str(basemode_ams_shots))
                            except KeyError:
                                if logging:
                                    print('No ShotsWhenFired in mode or base, checking bas only')
                                try:
                                    basemode_ams_shots = data['ShotsWhenFired']
                                    if logging:
                                        print(' AMS ShotsWhenFired is ', str(basemode_ams_shots))
                                except KeyError:
                                    if logging:
                                        print('No ShotsWhenFired at all?')

                            basemode_ams_avg_damage = 0
                            try:
                                basemode_ams_avg_damage = basemode_ams_damage * basemode_ams_shots * basemode_ams_hitchance
                                if logging:
                                    print('Basemode AMS average damage is ', str(basemode_ams_avg_damage))
                            except:
                                if logging:
                                    traceback.print_exc()
                                    print('This should not be reachable! AMS avg damage error.')

                            basemode_ams_heat = 0
                            try:
                                basemode_ams_heat = data['Modes'][i]['HeatGenerated'] + data['HeatGenerated']
                                if logging:
                                    print('Basemode AMS heat is ', str(basemode_ams_heat))
                            except KeyError:
                                if logging:
                                    print('No heat in modes or base, trying base.')
                                try:
                                    basemode_ams_heat = data['HeatGenerated']
                                    if logging:
                                        print('AMS heat is ', str(basemode_ams_heat))
                                except KeyError:
                                    if logging:
                                        print('No heat on AMS, defaulting to 0')

                            basemode_ams_jam = 0
                            try:
                                basemode_ams_jam = data['FlatJammingChance'] * 100
                                try:
                                    basemode_ams_jam = (data['Modes'][i]['FlatJammingChance'] + data['FlatJammingChance']) * 100
                                    if logging:
                                        print('Basemode AMS jam chance is ', str(basemode_ams_jam))
                                except KeyError:
                                    if logging:
                                        print('No mode jam chance, using base')
                            except KeyError:
                                if logging:
                                    print('No base jam chance, checking modes')
                                try:
                                    basemode_ams_jam = data['Modes'][i]['FlatJammingChance'] * 100
                                    if logging:
                                        print('Basemode AMS jam chance is ', str(basemode_ams_jam))
                                except KeyError:
                                    if logging:
                                        print('No jam chance on AMS, using zero')

                            try:
                                basemode_ams_maxrange = data['MaxRange'] + data['Modes'][i]['MaxRange']
                                if logging:
                                    print('Basemode AMS max range is ', str(basemode_ams_maxrange))
                            except KeyError:
                                if logging:
                                    print('No range boost in either base or mode, trying base value')
                                try:
                                    basemode_ams_maxrange = data['MaxRange']
                                    if logging:
                                        print('Basemode AMS max range is ', str(basemode_ams_maxrange))
                                except KeyError:
                                    if logging:
                                        print('No range in base values, checking only mode')
                                    basemode_ams_maxrange = data['Modes'][i]['MaxRange']
                                    if logging:
                                        print('Basemode AMS max range is ', str(basemode_ams_maxrange))

                            basemode_aams = 'False'
                            try:
                                if logging:
                                    print(data['Modes'][i]['IsAAMS'])
                                if data['Modes'][i]['IsAAMS']:
                                    if logging:
                                        print('This is an Advanced AMS and will protect allies')
                                    basemode_aams = 'True'
                            except KeyError:
                                if logging:
                                    print('No isAAMS tag present in modes, trying base')
                                try:
                                    if logging:
                                        print(data['IsAAMS'])
                                    if data['IsAAMS']:
                                        if logging:
                                            print('This is an Advanced AMS and will protect allies')
                                        basemode_aams = 'True'
                                except KeyError:
                                    if logging:
                                        print('This is not an advanced AMS and will not protect allies in this mode')
                                    basemode_aams = 'False'
                        else:
                            if logging:
                                print('Not an AMS mode, skipping')
                            continue
                except KeyError:
                    if logging:
                        print('AMS has no modes, trying base values')
                        traceback.print_exc()

                    try:
                        if logging:
                            print('No Mode AMS Damage, trying base')
                        basemode_ams_damage = data['AMSDamage'] + 1
                        if logging:
                            print('Basemode AMS damage is ', str(basemode_ams_damage))
                    except KeyError:
                        if logging:
                            print('No mode or base AMS Damage, defaulting to 1')
                        basemode_ams_damage = 1

                    basemode_ams_hitchance = 0
                    try:
                        basemode_ams_hitchance = data['AMSHitChance']
                        if logging:
                            print('Basemode AMS hitchance is ', str(basemode_ams_hitchance))
                    except KeyError:
                        if logging:
                            print('No AMS Hitchance at all!?')

                    basemode_ams_shots = 0
                    try:
                        basemode_ams_shots = data['ShotsWhenFired']
                        if logging:
                            print(' AMS ShotsWhenFired is ', str(basemode_ams_shots))
                    except KeyError:
                        if logging:
                            print('No ShotsWhenFired at all?')

                    basemode_ams_avg_damage = 0
                    try:
                        basemode_ams_avg_damage = basemode_ams_damage * basemode_ams_shots * basemode_ams_hitchance
                        if logging:
                            print('Basemode AMS average damage is ', str(basemode_ams_avg_damage))
                    except:
                        if logging:
                            traceback.print_exc()
                            print('This should not be reachable! AMS avg damage error.')

                    basemode_ams_heat = 0
                    try:
                        basemode_ams_heat = data['HeatGenerated']
                        if logging:
                            print('AMS heat is ', str(basemode_ams_heat))
                    except KeyError:
                        if logging:
                            print('No heat on AMS, defaulting to 0')

                    basemode_ams_jam = 0
                    try:
                        basemode_ams_jam = data['FlatJammingChance'] * 100
                    except KeyError:
                        if logging:
                            print('No base jam chance, defaulting to zero')

                    basemode_ams_maxrange = 0
                    try:
                        basemode_ams_maxrange = data['MaxRange']
                        if logging:
                            print('Basemode AMS max range is ', str(basemode_ams_maxrange))
                    except KeyError:
                        if logging:
                            print('No range on AMS, this thing is useless?')

                    try:
                        if logging:
                            print(data['IsAAMS'])
                        if data['IsAAMS']:
                            if logging:
                                print('This is an Advanced AMS and will protect allies')
                            basemode_aams = 'True'
                        else:
                            if logging:
                                print('This is not an advanced AMS and will not protect allies in this mode')
                            basemode_aams = 'False'
                    except KeyError:
                        if logging:
                            print(
                                'No isAAMS tag present, this is not an advanced AMS and will not protect allies in this mode')
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

                if logging:
                    print(current_row_ams)
                ams_df2 = pandas.DataFrame([current_row_ams], columns=ams_columns_list)
                if logging:
                    print(ams_df2)
                ams_df = pandas.concat([ams_df, ams_df2])

            except UnicodeDecodeError:
                excepted_files.append(item)
                if logging:
                    print('Possible invalid character in JSON')
            except json.decoder.JSONDecodeError:
                possible_invalid_jsons.append(item)
                if logging:
                    print('Possible invalid JSON!')
    ##End of the JSON.load() try statement

    # These are used to write filenames of different types of excepted files to separate text files for analyzation later
    # For tracking all files filtered from exclusion list and other filter checks
    with open("filtered files.txt", "w") as output:
        for item in filtered_files:
            output.write(str(item) + '\n')
    # For items that return a UnicodeDecodeError, most likely due to odd characters in the file.
    with open("excepted files.txt", "w") as output:
        for item in excepted_files:
            output.write(str(item) + '\n')
    # For items that return a JSONDecodeError, these are almost certainly an invalid or incorrectly formatted JSON file.
    with open("possible invalid JSON.txt", "w") as output:
        for item in possible_invalid_jsons:
            output.write(str(item) + '\n')
    ##

    # Writes the fully formed Pandas DataFrames to their respective sheets of the final spreadsheet file
    with pandas.ExcelWriter('RT Weaponlist.xlsx') as writer:
        df.to_excel(writer, sheet_name='Weapons', index=False)
        ams_df.to_excel(writer, sheet_name='AMS', index=False)

    tk.messagebox.showinfo('Successfully generated sheet in ' + "{:.2f}".format(time.time() - time1) + ' seconds',
                           'Data saved to external spreadsheet file RT Weaponlist.xlsx within this program directory')

    sys.exit()

root.mainloop()