"""Suits are used to equip creatures during generation."""
import engine.item as i


# Armor
class Boot(i.Item):
    name = "boot"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True
    armor = 2

class Bracer(i.Item):
    name = "bracer"
    canwear = i.Item.canwear.copy()
    canwear["arm"] = True
    armor = 1

class Chainmail(i.Item):
    name = "chainmail"
    canwear = i.Item.canwear.copy()
    canwear["body"] = True
    armor = 2

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

class Helm(i.Item):
    name = "helm"
    canwear = i.Item.canwear.copy()
    canwear["head"] = True
    armor = 1

class Shield(i.Item):
    name = "shield"
    canwear = i.Item.canwear.copy()
    canwear["back"] = True
    canwear["arm"] = True
    armor = 3

# Clothing
class Tunic(i.Item):
    name = "tunic"
    canwear = i.Item.canwear.copy()
    canwear["torso"] = True

class Hose(i.Item):
    name = "hose"
    canwear = i.Item.canwear.copy()
    canwear["leg"] = True

class Shoe(i.Item):
    name = "boot"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True

# Weapons
class Axe(i.Item):
    name = "axe"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 7

class Spear(i.Item):
    name = "spear"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 8

class Sword(i.Item):
    name = "sword"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 9


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

plainsuit = {
    "body": Tunic,
    "leg": Hose,
    "foot": Shoe,
}

weapons = {
    "hand": (Sword, Spear, Axe)
}
