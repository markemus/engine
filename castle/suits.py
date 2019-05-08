"""Suits are used to equip creatures during generation."""
import engine.item as i


# Armor
class Helm(i.Item):
    name = "helm"
    canwear = i.Item.canwear.copy()
    canwear["head"] = True
    armor = 1

class Chainmail(i.Item):
    name = "chainmail"
    canwear = i.Item.canwear.copy()
    canwear["body"] = True
    armor = 2

class Shield(i.Item):
    name = "shield"
    canwear = i.Item.canwear.copy()
    canwear["back"] = True
    canwear["arm"] = True
    armor = 3

class Bracer(i.Item):
    name = "bracer"
    canwear = i.Item.canwear.copy()
    canwear["arm"] = True
    armor = 1

class Gauntlet(i.Item):
    name = "gauntlet"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    armor = 1

class Greave(i.Item):
    name = "greave"
    canwear = i.Item.canwear.copy()
    canwear["leg"] = True
    armor = 1

class Boot(i.Item):
    name = "boot"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True
    armor = 2

# Weapons
class Sword(i.Item):
    name = "sword"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 9

class Spear(i.Item):
    name = "spear"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 8

class Axe(i.Item):
    name = "axe"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 7

# Suits
testsuit = {
    "head": Helm,
    "body": Chainmail,
    "back": Shield,
    "arm": Bracer,
    "hand": Gauntlet,
    "leg": Greave,
    "foot": Boot
    }

weapons = {
    "hand": (Sword, Spear, Axe)
}

testcolor = {
    "hair": "red",
    "skin": "white",
    "eye": "green",
    "teeth": "white"
}
