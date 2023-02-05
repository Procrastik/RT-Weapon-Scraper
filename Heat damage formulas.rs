If weapon has AlternateHeatDamageCalc: true, use formula 1
formula one baseDamage + extAmmunitionDef.HeatDamagePerShot + weaponMode.HeatDamagePerShot) * extAmmunitionDef.HeatMultiplier * weaponMode.HeatMultiplier;

Everything else use this formula
formula two (weapon.get_weaponDef().get_HeatDamage() + extAmmunitionDef.HeatDamagePerShot + weaponMode.HeatDamagePerShot) * extAmmunitionDef.HeatMultiplier * weaponMode.HeatMultiplier * baseDamage / weapon.get_weaponDef().get_HeatDamage();

f1  (WeaponBaseDamage + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier
    (20 + 40 + 0) * 1 * 0.2
        60 * 1 * 0.2
        60 * 0.2

f2  (WeaponHeatDam + AmmoHeatDamagePerShot + WeaponModeHeatDamagePerShot) * AmmoHeatMultiplier * WeaponModeHeatMultiplier * WeaponBaseDamage / WeaponHeatDamage
    (0 + 40 + 0) * 1 * 0.2 * 20 / 0
        40 * 1 * 0.2 * 20 / 0

Note: These are modified by evasion pips with CAC hexesMovedMod trait somehow
Overall formula value = [base value] * ([moved hexes]^[mod value]). Example base damage = 35, moved hexes = 7, mod value = -1
                          damage = 35 * (7^-1) = 35 * 0.142857(142857) = 5.