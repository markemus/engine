import item as i

#armor
class helm(i.thing):
    name = "helm"
    canwear = i.thing.canwear.copy()
    armor = 1
    canwear["head"] = True

class chainmail(i.thing):
    name = "chainmail"
    canwear = i.thing.canwear.copy()
    armor = 2
    canwear["body"] = True

class shield(i.thing):
    name = "shield"
    canwear = i.thing.canwear.copy()
    armor = 3
    canwear["back"] = True
    canwear["arm"] = True

class bracer(i.thing):
    name = "bracer"
    canwear = i.thing.canwear.copy()
    armor = 1
    canwear["arm"] = True

class gauntlet(i.thing):
    name = "gauntlet"
    canwear = i.thing.canwear.copy()
    armor = 1
    canwear["hand"] = True

class greave(i.thing):
    name = "greave"
    canwear = i.thing.canwear.copy()
    armor = 1
    canwear["leg"] = True

class boot(i.thing):
    name = "boot"
    canwear = i.thing.canwear.copy()
    armor = 2
    canwear["foot"] = True



#weapons
class sword(i.thing):
    name = "sword"
    canwear = i.thing.canwear.copy()
    canwear["hand"] = True
    damage = 9

class spear(i.thing):
    name = "spear"
    canwear = i.thing.canwear.copy()
    canwear["hand"] = True
    damage = 8

class axe(i.thing):
    name = "axe"
    canwear = i.thing.canwear.copy()
    canwear["hand"] = True
    damage = 7



testsuit = {
    "head": helm,
    "body": chainmail,
    "back": shield,
    "arm": bracer,
    "hand": gauntlet,
    "leg": greave,
    "foot": boot
    }

weapons = {
    "hand": (sword, spear, axe)
}

testcolor = {
    "hair": "red",
    "skin": "white",
    "eye": "green",
    "teeth": "white"
}