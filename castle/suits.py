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
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    covers["foot"] = True
    armor = 2
    level = 3
    descends = 0

class Bracer(i.Item):
    name = "bracer"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["arm"] = True
    covers["arm"] = True
    armor = 1
    level = 3
    descends = 0

class Chainmail(i.Item):
    name = "chainmail"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    armor = 6
    level = 3
    descends = 0

class Gauntlet(i.Item):
    name = "gauntlet"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["right hand"] = True
    canwear["left hand"] = True
    covers["right hand"] = True
    covers["left hand"] = True
    covers["finger"] = True
    covers["thumb"] = True
    armor = 2
    level = 3
    descends = 1

class Greave(i.Item):
    name = "greave"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    covers["leg"] = True
    armor = 2
    level = 3
    descends = 0

class Helm(i.Item):
    name = "helm"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    covers["head"] = True
    covers["eye"] = True
    covers["ear"] = True
    covers["nose"] = True
    covers["mouth"] = True
    covers["teeth"] = True
    armor = 4
    level = 3
    descends = 2

class Shield(i.Item):
    name = "shield"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["back"] = True
    canwear["left hand"] = True
    covers["back"] = True
    covers["left hand"] = True
    covers["finger"] = True
    covers["thumb"] = True
    armor = 4
    level = 3
    descends = 1

# Clothing
class Apron(i.Item):
    name = "apron"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    covers["leg"] = True
    level = 2
    descends = 1

class ChefHat(i.Item):
    name = "chef hat"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    covers["head"] = True
    level = 2
    descends = 0

class Hose(i.Item):
    name = "hose"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    covers["leg"] = True
    level = 1
    descends = 0

class Shoe(i.Item):
    name = "shoe"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    covers["foot"] = True
    level = 1
    descends = 0

class Slipper(i.Item):
    name = "slipper"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    covers["foot"] = True
    level = 1
    descends = 0

class Tunic(i.Item):
    name = "tunic"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    level = 1
    descends = 0

class Clout(i.Item):
    name = "clout"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    level = 1
    descends = 0


# Jewelry
class Bracelet(i.Item):
    name = "bracelet"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["hand"] = True
    covers["hand"] = True
    canwear["right hand"] = True
    covers["right hand"] = True
    canwear["left hand"] = True
    covers["left hand"] = True
    canwear["foot"] = True
    covers["foot"] = True
    level = 2

class Necklace(i.Item):
    name = "necklace"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    level = 2

class Ring(i.Item):
    name = "ring"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["finger"] = True
    covers["finger"] = True
    level = 2

# Weapons
class Axe(i.Item):
    name = "axe"
    # canwear = i.Item.canwear.copy()
    # canwear["right hand"] = True
    damage = 20
    # requires = ("grasp", 1)
    # level = 3

class Cleaver(i.Item):
    name = "cleaver"
    # canwear = i.Item.canwear.copy()
    # canwear["right hand"] = True
    # canwear["left hand"] = True
    damage = 10
    # requires = ("grasp", 1)
    # level = 3

class Shank(i.Item):
    name = "prison shank"
    # canwear = i.Item.canwear.copy()
    # canwear["right hand"] = True
    damage = 5
    # requires = ("grasp", 1)
    # level = 3

class Spear(i.Item):
    name = "spear"
    # canwear = i.Item.canwear.copy()
    # canwear["right hand"] = True
    damage = 20
    # requires = ("grasp", 1)
    # level = 3

class Sword(i.Item):
    name = "sword"
    # canwear = i.Item.canwear.copy()
    # canwear["right hand"] = True
    damage = 20
    # requires = ("grasp", 1)
    # level = 3

# Special
class Blindfold(i.Item):
    name = "blindfold"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    covers["head"] = True
    covers["eye"] = True
    see = -2
    level = 1
    descends = 1

class SkinMask(i.Item):
    name = "human face"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    covers["head"] = True
    covers["ear"] = True
    covers["eye"] = True
    covers["nose"] = True
    covers["mouth"] = True
    covers["teeth"] = True
    level = 1
    descends = 3

# TODO-DONE add third _scheme option- more than distinct, give each element a unique scheme
#  (distinct for matching gloves, unique for separate rings)
# Suits
jewelry = {
    "wears": {
        "body": Necklace,
        "right hand": Bracelet,
        "left hand": Bracelet,
        "finger": Ring,
        "foot": Bracelet},
    "grasps": {},
    "color": ["sapphire", "emerald", "turquoise"],
    "color_scheme": "unique",
    "texture": ["in silver", "in gold", "in platinum"],
    "texture_scheme": "unique",
    "full": False,
}

cookery = {
    "grasps": {
        "right hand": Cleaver,
        "left hand": Cleaver},
    "wears": {},
    "color": ["grimy", "bloody", "rusty"],
    "color_scheme": "same",
    "texture": ["iron"],
    "texture_scheme": "same",
    "full": True,
}

chefface = {
    "wears": {
        "head": SkinMask},
    "grasps": {},
    "color": ["bloody", "stretched", "stitched", "pale"],
    "color_scheme": "same",
    "texture": ["skin"],
    "texture_scheme": "same",
    "full": True,
}

chefsuit = {
    "wears": {
        "head": ChefHat,
        "body": Apron,
        "leg": Hose,
        "foot": (Shoe, Slipper)},
    "grasps": {},
    "color": ["white", "stained", "greasy"],
    "color_scheme": "distinct",
    "texture": ["linen"],
    "texture_scheme": "same",
    "full": True,
    }

plainsuit = {
    "wears": {
        "body": Tunic,
        "leg": Hose,
        "foot": (Shoe, Slipper)},
    "grasps": {},
    "color": ["red", "blue", "green", "yellow", "striped"],
    "color_scheme": "distinct",
    "texture": ["silk", "cotton", "wool"],
    "texture_scheme": "same",
    "full": True,
    }

prisonersuit = {
    "wears": {
        "body": Clout},
    "grasps": {},
    "color": ["gray", "dirty", "brown"],
    "color_scheme": "distinct",
    "texture": ["linen"],
    "texture_scheme": "distinct",
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
    "grasps": {},
    "color": ["shiny", "rusty", "matte"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
    }

weapons = {
    "wears":{},
    "grasps": {
        "right hand": (Sword, Spear, Axe)},
    "color": ["gray"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}

# TODO-DONE current attack-block cycle is boring with shields- but blocking with arms only makes sense in Castle. Think about how to improve shields. Blocking miss chance?
# TODO more potions (add temporary effects- stoneskin?)
