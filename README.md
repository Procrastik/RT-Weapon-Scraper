# RT Weapon Scraper
Note: I am working on this project alone and as such, have a very limited ability to verify data aside from spot checks and code research. If you enjoy this tool, please help me out by pointing out any innaccuracies you may find so that I may address them. I am active on the RogueTech discord server as Procrastk if you wish to reach out to me.

**RT Weapon Scraper**
This tool is a weapon spreadsheetizer that pulls all weapons and pertinent data for them in the entire mod directory into a spreadsheet for comparisons.
This tool also does JSON and Unicode verification. This tool is written with Python 3 and utilizes the libraries os, sys, json, traceback, pandas, time, re, and tkinter.

The weapon scraper recursively checks the directory tree it is pointed at and returns an .xlsx spreadsheet with all found weapons minus any that are in its excluded list. It also returns separate files for possible invalid JSON files, possible Unicode or text compatibility errors, and a list of any excepted files that were skipped due to filtering.

**How to use the tool**
The recent GUI and onefile executable update has drastically simplified the process for using the tool. If you just want the spreadsheet I generally run it periodically and post the updated sheet in this repository but the crew changes things often so this could be out of date.

Operating the tool is as simple as clicking the button in the middle of the window and selecting your RogueTech Mods folder. Once you have selected this folder a go button will appear at the bottom of the window that you can use to run the program. The logging checkbox is only used to peek under the hood or troubleshooting and is not recommended as it will turn a 4 second process into 500+ seconds.

Once the program is run several files will be saved in the directory the program was run including the weapon spreadsheet. It will be badly formatted when it is initally saved so for convenience I do include a template spreadsheet you can use to copy formatting for the whole sheet using the format painter tool.

That's it, you are done and can sort and view stats of every weapon in the game. 

To run the tool there are three options.

**Run the Python file as is using your own IDE** - This will require that you also ensure you have a compatible version of Python 3, plus all the required dependencies.

**The no console executable** - This is the most convenient option. The no console executable is a self-contained executable file that runs without opening a console window and without needing Python or any of its dependencies installed.

**The standard console executable** - The console executable is also a self-contained executable file that runs with a console window and without needing Python or any of its dependencies installed. The difference being that it includes the standard console that will launch when the program is run. If you are interested in logging you would utilize this one but be advised that logging trashes the program's runtime.

Currently the tool returns a large list of metrics about each weapon and AMS System:

_**Hardpoint Type**_ - Returns the type of hardpoint this weapon uses.

_**Weapon Class**_ - Returns the weapon subtype.

_**Weapon Name**_ - Returns the weapon UI or common name used in game.

_**Indirectfire**_ - A boolean returning either True or False whether the weapon is cabable of indirect fire; This check captures weapons with an indirect mode as well.

_**Clustering Capable**_ - A semi-boolean value returned that shows if a weapon is capable of clustering hits. True (always capable), True in Mode (Capable in a mode), True in Ammo (Capable with certain ammo type).

_**Tonnage**_ - Tonnage of the weapon, this does not include ammo tonnage for weapons that use ammo.

_**Slots**_ - Critical slots taken by the weapon, this does not include ammo slots for weapons that use ammo.

_**Max Recoil**_ - The recoil value the weapon has in its highest damaging mode. I chose to focus on the maximum damaging mode for this check if applicable so on super odd weapons this may not always be the highest recoil possible on the weapon.

_**Base Direct Damage**_ - The base direct damage of the weapon in its default mode. This is mostly to help compare weapons that have nearly unusable max damage modes due to incredible misfire/jam rates or other detrimental effects. Does not account for ammo bonuses.

_**Max Direct Damage**_ - Dakka Dakka. The absolute maximum possible direct damage the weapon can do in its highest damaging mode using its most damaging ammotype.

_**Max Ammo Damage**_ - The direct damage value (not including AOE) of the most damaging ammo type if applicable. This checks for ammo damagepershot as well as damagemultiplier.

_**Highest Direct Damage Ammo**_ - The name of the highest direct damaging ammo. This checks for ammo damagepershot as well as damagemultiplier.

_**AOE Damage**_ - AOE damage provided by the weapon and its most damaging AOE ammo. This also captures TAG weapons that have a deferredEffect such as TAG Arrow IV. Does not account for AOE falloff as you get farther from the impact point.

_**AOE Heat Damage**_ - AOE Heat damage provided by the weapon and its most damaging AOE Heat ammo. This also captures TAG weapons that have a deferredEffect such as TAG Barrage. Does not account for AOE falloff as you get farther from the impact point.

_**AOE Radius**_ - Radius in meters from impact that AOE Damage will impact including ammo. This also captures TAG weapons that have a deferredEffect such as TAG Arrow IV.

_**Damage Variance**_ - The damage variance value (+ or -) of the weapon.

_**Max Stability Damage**_ - The absolute maximum possible stability damage the weapon can do in its highest damaging mode (as this is likely always the most destabilizing mode as well). Does not account for ammo bonuses at this time.

_**Max Heat Damage**_ - The absolute maximum possible heat damage the weapon can do in its spiciest mode or base including the best heat ammo if applicable. (Includes everything, weapon base values, best mode values, ammo values and bonuses as as well as number of shots fired)

_**Max Per Ammo Heat Damage**_ - The per shot direct heat damage value of the spiciest ammo type. (Includes ammo damage and multipliers only; Does not account for weapon modifiers.)

_**Highest Direct Heat Damage Ammo**_ - The name of the spiciest ammo type.

_**Max Firing Heat**_ - The firing heat generated in the most damaging mode (which is also nearly always the hottest mode).

_**Max Jam Chance**_ - The jam chance of the weapon in the most damaging mode (Out of 100%). Does not account for pilot and gear modifiers.

_**Can Misfire**_ - A semi-boolean value to show if the weapon is capable of misfiring (damaging self on jam). Boolean will differentiate between the misfire being on all attacks with the weapons or specifically in a firing mode.

_**Damage Per Heat**_ - (Max Damage + AOE Damage)/Max Firing Heat (Includes ammo bonuses and multipliers)

_**Damage Per Slot**_ - (Max Damage + AOE Damage)/Slots (Includes ammo bonuses and multipliers)

_**Damage Per Ton**_ - (Max Damage + AOE Damage)/Tonnage (Includes ammo bonuses and multipliers)

_**Weapon Crit Multiplier**_ - The standard crit multiplier on the weapon which is used to give weapon base crit chance.

_**Weapon Base Crit Chance**_ - The adjusted crit chance for each shot of the weapon when hitting open structure. Does not account for ammo bonuses or penalties, gear bonuses, or enemy gear penalties.

_**Weapon TAC Chance (50% Max Thickness)**_ - The Through Armor Critical chance of the weapon at half its maximum possible armor penetration value, this chance will increase as armor gets thinner. Does not account for ammo bonuses/penalties. (TAC is used in all scenarios when the target still has armor in a location, even with tandem ammo, etc.) 

_**Max TAC Armor Thickness**_ - The maximum target armor location thickness that a TAC is possible at with this weapon.

_**Base Accuracy Bonus**_ - Bonus or malus to accuracy on this weapon, negative means better accuracy. At present this does not check in modes or ammo because it gets complicated with some weapons.

_**Base Evasion Ignore**_ - Bonus evasion ignore provided by the weapon, positive is better. At present this does not check in modes or ammo because it gets complicated with some weapons.

_**Minimum Range**_ - The minimum range of the weapon. Does not account for mode or ammo range changes.

_**Short Range**_ - Short range start of the weapon. Does not account for mode or ammo range changes.

_**Medium Range**_ - Medium range start of the weapon. Does not account for mode or ammo range changes.

_**Long Range**_ - Long range start of the weapon. Does not account for mode or ammo range changes.

_**Max Range**_ - Max range of the weapon. Does not account for mode or ammo range changes.

_**Damage Falloff %**_ - Percentage of max damage that falloff will reduce to for this weapon. Damage falloff could either be reversed (starting close at max falloff and lowering at range) or normal, starting close at full damage and reducing at longer ranges.

_**Min Range Damage**_ - Damage expected at minimum range including falloff in applicable.

_**Short Range Damage**_ - Damage expected at short range including falloff in applicable.

_**Medium Range Damage**_ - Damage expected at medium range including falloff in applicable.

_**Long Range Damage**_ - Damage expected at long range including falloff in applicable.

_**Max Range Damage**_ - Damage expected at max range including falloff in applicable.

_**Weapon AAA Factor %**_ - Percentage bonus to mech AAA factor provided by this weapon. I do not know know much about this mechanic so can't say how this interacts with the AAA factor beyond the bonus.

____________________________________________________________________________________________________________________________________________________________________

_**AMS Sheet**_ - The separate AMS sheet contains basic info about most AMS systems. Due to the culling of most of the many modes that previous versions contained I now only check for the base mode stats and there are not any secondary AMS modes that would get much regular use. Currently this tool excludes special and unique equipment due to their oft complexity and general non-standard setups so many or all of the chassis fixed AMS systems will not be included.

_**AMS Hardpoint Type**_ - Returns the type of hardpoint this AMS system uses.

_**AMS Weapon Class**_ - Returns the AMS system subtype.

_**AMS Weapon Name**_ - Returns the weapon UI or common name used in game for this AMS system.

_**AMS Tonnage**_ - Tonnage of the AMS system, this does not include ammo tonnage for systems that use ammo.

_**AMS Slots**_ - Critical slots taken by the AMS system, this does not include ammo slots for systems that use ammo.

_**AMS Activations Per Round**_ - The maximum number of separate activations this AMS system can have in a round. Each activation the system can fire its Shots Per Activation.

_**AMS Base Damage Per Shot**_ - The amount of damage each shot in an activation can do to an incoming missile in the base mode. Higher numbers means you will use less ammo to destroy missiles.

_**AMS Base Average Damage**_ - The average damage you can expect from this AMS system in the base mode. Average damage is calculated as such (AMS Base Damage Per Shot * AMS Base Shots Per Activation * AMS Base Hit Chance)

_**AMS Base Shots Per Activation**_ - The maximum number of individual shots each activation of this AMS system will fire in the base mode. If all missiles are destroyed before this is reached the remaining shots are not fired and any ammo remaining for this activation is retained.

_**AMS Base Hit Chance**_ - The hit chance for each shot fired by this AMS system in the base mode.

_**AMS Base Heat Per Activation**_ - The heat generated by this AMS system for each activation in the base mode. The full value of this is applied each activation, there is no partial value applied if the activation shot limit is not reached.

_**AMS Base Jam Chance**_ - The jam chance of this AMS system in its base mode (Out of 100%). Does not account for pilot and gear modifiers.

_**AMS Base Max Range**_ - The max range this AMS system can fire in its base mode.

_**AMS Base Protect Allies**_ - A boolean value to show whether this AMS system can protect allies within range in its base mode.
