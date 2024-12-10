"""Suits are used to equip creatures during generation.

# A suit is a dictionary of parameters
suit = {

    # Which body part is equipped with which item.
    "wears": {
        "head": Helm,
        "body": Chainmail,
        "back": Shield,
        "arm": Bracer,
        "hand": Gauntlet,
        "leg": Greave,
        "foot": Boot},

    # Color and texture are used to customize the items
    "color": ["shiny", "rusty", "matte"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",

    # Whether the creature gets the full item set, or a random subset
    "full": True,
    }
"""
import engine.item as i
import engine.suits_and_collections as sc


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
    armor = 6

class Gauntlet(i.Item):
    name = "gauntlet"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    armor = 2

class Greave(i.Item):
    name = "greave"
    canwear = i.Item.canwear.copy()
    canwear["leg"] = True
    armor = 2

class Helm(i.Item):
    name = "helm"
    canwear = i.Item.canwear.copy()
    canwear["head"] = True
    armor = 4

class Shield(i.Item):
    name = "shield"
    canwear = i.Item.canwear.copy()
    canwear["back"] = True
    canwear["left hand"] = True
    armor = 4

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

class Slipper(i.Item):
    name = "slipper"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True

# Jewelry
class Bracelet(i.Item):
    name = "bracelet"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    canwear["foot"] = True

class Necklace(i.Item):
    name = "necklace"
    canwear = i.Item.canwear.copy()
    canwear["body"] = True

class Ring(i.Item):
    name = "ring"
    canwear = i.Item.canwear.copy()
    canwear["finger"] = True

# Weapons
class Axe(i.Item):
    name = "axe"
    canwear = i.Item.canwear.copy()
    canwear["right hand"] = True
    damage = 20

class Spear(i.Item):
    name = "spear"
    canwear = i.Item.canwear.copy()
    canwear["right hand"] = True
    damage = 20

class Sword(i.Item):
    name = "sword"
    canwear = i.Item.canwear.copy()
    canwear["right hand"] = True
    damage = 20

# Special
class Blindfold(i.Item):
    name = "blindfold"
    canwear = i.Item.canwear.copy()
    canwear["head"] = True
    see = -2

# TODO add third _scheme option- more than distinct, give each element a unique scheme
#  (distinct for matching gloves, unique for separate rings)
# Suits
jewelry = {
    "wears": {
        "body": Necklace,
        "right hand": Bracelet,
        "left hand": Bracelet,
        "finger": Ring,
        "foot": Bracelet},
    "color": ["sapphire", "emerald", "turquoise"],
    "color_scheme": "distinct",
    "texture": ["in silver", "in gold", "in platinum"],
    "texture_scheme": "distinct",
    "full": False,
}

plainsuit = {
    "wears": {
        "body": Tunic,
        "leg": Hose,
        "foot": (Shoe, Slipper)},
    "color": ["red", "blue", "green", "yellow", "striped"],
    "color_scheme": "distinct",
    "texture": ["silk", "cotton", "wool"],
    "texture_scheme": "same",
    "full": True,
    }

testsuit = {
    "wears": {
        "head": Helm,
        "body": Chainmail,
        "arm": Bracer,
        "left hand": Gauntlet,
        "right hand": Gauntlet,
        "leg": Greave,
        "foot": Boot},
    "color": ["shiny", "rusty", "matte"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
    }

weapons = {
    "wears": {
        "right hand": (Sword, Spear, Axe),
        "left hand": Shield},
    "color": ["gray"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}
