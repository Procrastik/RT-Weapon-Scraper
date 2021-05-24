# RT-Analyzation
Roguetech Tools

This is a personal project to create my own tools for analyzation of files for the Hare Brained Studios Battletech game mod RogueTech. At this time all tools are written in Python.

**RT Weapon Scraper**
The first tool is a weapon spreadsheetizer that pulls all weapons and pertinent data for them in the entire mod directory into a spreadsheet for comparisons.
This tool also does JSON and Unicode verification.

The weapon scraper recursively checks the directory tree it is pointed at and returns a .xlsx spreadsheet with all found weapons minus any that are in its excluded list. It also returns separate files for possible invalid JSON files, possible Unicode or text compatibility errors, and a list of any excepted files that were skipped due to filtering.

Currently the tool returns a large list of metrics about each weapon:

_Hardpoint Type_ - Returns the type of hardpoint this weapon uses.
_Weapon Class_ - Returns the weapon subtype.
_Weapon Name_ - Returns the weapon UI or common name used in game.
_Indirectfire_ - A boolean returning either True or False whether the weapon is cabable of indirect fire; This check captures weapons with an indirect mode as well.
_Clustering Capable_ - A semi-boolean value returned that shows if a weapon is capable of clustering hits. True (always capable), True in Mode (Capable in a mode), True in Ammo (Capable with certain ammo type).
_Tonnage_ - Tonnage of the weapon, this does not include ammo tonnage for weapons that use ammo.
_Slots_ - Critical slots taken by the weapon, this does not include ammo slots for weapons that use ammo.
_Max Recoil_ - The maximum recoil value the weapon has in its highest damaging mode. I chose to focus on the maximum damaging mode for this check if applicable so on super odd weapons this may not always be the highest recoil possible on the weapon.
_Base Damage_ - The base direct damage of the weapon in its default mode. This is mostly to help compare weapons that have nearly unusable max damage modes due to incredible misfire/jam rates or other detrimental effects. Does not account for ammo bonuses.
_Max Damage_ - Dakka Dakka. The absolute maximum possible direct damage the weapon can do in its highest damaging mode. Does not account for ammo bonuses.
_Max Ammo Damage_ - The direct damage value of the most damaging ammo type if applicable. Currently this only evaluates 'DamagePerShot' so ammo types that do additional damage multipliers could potentially be better and missed at this time.
_Highest Direct Damage Ammo_ - The name of the highest direct damaging ammo. Currently this only evaluates 'DamagePerShot' so ammo types that do additional damage multipliers could potentially be better and missed at this time.
_AOE Damage_ - AOE damage provided by the weapon itself. Currently this does not account for ammo bonuses.
_AOE Radius_ - Radius in meters from impact that AOE Damage will impact. Currently this does not account for ammo bonuses.
_Damage Variance_ - The damage variance value (+ or -) of the weapon.
_Max Stability Damage_ - The absolute maximum possible stability damage the weapon can do in its highest damaging mode (as this is likely always the most destabilizing mode as well). Does not account for ammo bonuses.
_Max Heat Damage_ - The absolute maximum possible heat damage the weapon can do in its spiciest mode. Does not account for ammo bonuses.
_Max Ammo Heat Damage_ - The direct heat damage value of the spiciest ammo type.
_Highest Direct Heat Damage Ammo_ - The name of the spiciest ammo type.
_Max Firing Heat_ - The firing heat generated in the most damaging mode (which is also nearly always the hottest mode).
_Max Jam Chance_ - The jam chance of the weapon in the most damaging mode (Out of 100%). Does not account for pilot and gear modifiers.
_Can Misfire_ - Boolean to show if the weapon is capable of misfiring (damaging self on jam). Boolean accounts for modes so weapons that can misfire only in certain modes are counted as True.
_Damage Per Heat_ - (Max Damage + AOE Damage)/Max Firing Heat (Does not account for ammo bonuses)
_Damage Per Slot_ - (Max Damage + AOE Damage)/Slots (Does not account for ammo bonuses)
_Damage Per Ton_ - (Max Damage + AOE Damage)/Tonnage (Does not account for ammo bonuses)
_Weapon Crit Multiplier_ - The standard crit multiplier on the weapon which is used to give weapon base crit chance.
_Weapon Base Crit Chance_ - The adjusted crit chance for each shot of the weapon when hitting open structure. Does not account for ammo bonuses or penalties, gear bonuses, or enemy gear penalties.
_Weapon TAC Chance (50% Max Thickness)_ - The Through Armor Critical chance of the weapon at half its maximum possible armor penetration value, this chance will increase as armor gets thinner. Does not account for ammo bonuses/penalties. (TAC is used in all scenarios when the target still has armor in a location, even with tandem ammo, etc.) 
_Max TAC Armor Thickness_ - The maximum target armor location thickness that a TAC is possible at with this weapon.
_Base Accuracy Bonus_ - Bonus or malus to accuracy on this weapon. At present this does not check in modes because it gets complicated with some weapons.
_Base Evasion Ignore_ - Bonus evasion ignore provided by the weapon.
_Minimum Range_ - The minimum range of the weapon. Does not account for mode range changes.
_Short Range_ - Short range start of the weapon. Does not account for mode range changes.
_Medium Range_ - Medium range start of the weapon. Does not account for mode range changes.
_Long Range_ - Long range start of the weapon. Does not account for mode range changes.
_Max Range_ - Max range of the weapon. Does not account for mode range changes.
_Damage Falloff %_ - Maximum percentage of damage falloff for this weapon. Damage falloff could either be reversed (starting close at max falloff and lowering at range) or normal, starting close at full damage and reducing at longer ranges.
_Min Range Damage_ - Damage expected at minimum range.
_Short Range Damage_ - Damage expected at short range.
_Medium Range Damage_ - Damage expected at medium range.
_Long Range Damage_ - Damage expected at long range.
_Max Range Damage_ - Damage expected at max range.
