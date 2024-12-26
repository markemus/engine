"""Suits are used to equip Creatures during game generation. They can also be converted to collections,
which are used to fill Furniture.

# A suit is a dictionary of parameters
suit = {

    # Which body part is equipped with which item.
    "wears": {
        "head": Helm,
        "body": Chainmail,
        "back": Shield,
        "arm": Bracer,
        "left hand": Gauntlet,
        "right hand": Gauntlet,
        "leg": Greave,
        "foot": Boot},
    "grasps": {same as wears, but for weapons}

    # Color and texture are used to customize the items. Scheme options are "same", "distinct", and "unique".
    # "same" means all items share the same color and texture.
    # "distinct" makes items of the same type share a color scheme.
    # "unique" means each item gets a separate color and texture.
    "color": ["shiny", "rusty", "matte"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",

    # Whether the creature gets the full item set, or a random subset
    "full": True,
    }

Items are objects used by creatures or just stored in rooms to add character.
    class Gauntlet(i.Item):
    name = "gauntlet"
    # canwear- which limbs types can wear the item (specified by limb.wears).
    # covers- which limbs are covered by the item (for armor, gives armor bonus to these limbs).
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["right hand"] = True
    canwear["left hand"] = True
    covers["right hand"] = True
    covers["left hand"] = True
    covers["finger"] = True
    covers["thumb"] = True
    armor = 2
    # level- only one Item per level can be worn by a creature on a given Limb. So socks and shoes are okay, but slippers and shoes are not.
    level = 3
    # How far down the Limb hierarchy to check for the Limbs in self.covers .
    descends = 1
"""
import copy

import engine.item as i


# Armor
class IronBoot(i.Item):
    name = "boot"
    # canwear[limb_type] governs where the item can be worn by a creature
    # covers[limb_type] governs which limbs will be protected by the worn item.
    # descends tells the engine how far down the limb hierarchy to look for the covers limb types.
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    covers["foot"] = True
    armor = 2
    level = 3
    descends = 0

class IronBracer(i.Item):
    name = "bracer"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["arm"] = True
    covers["arm"] = True
    armor = 2
    level = 3
    descends = 0

class IronChainmail(i.Item):
    name = "chainmail"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    armor = 2
    level = 3
    descends = 0

class IronGauntlet(i.Item):
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

class IronGreave(i.Item):
    name = "greave"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    covers["leg"] = True
    armor = 2
    level = 3
    descends = 0

class IronHelm(i.Item):
    name = "helm"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    covers["head"] = True
    covers["eye"] = True
    covers["ear"] = True
    covers["nose"] = True
    covers["mouth"] = True
    covers["tongue"] = True
    covers["teeth"] = True
    armor = 2
    level = 3
    descends = 2

class IronShield(i.Item):
    name = "shield"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["back"] = True
    canwear["left hand"] = True
    covers["back"] = True
    covers["left hand"] = True
    covers["finger"] = True
    covers["thumb"] = True
    armor = 2
    level = 4
    descends = 1

class BronzeBoot(IronBoot):
    armor = 1

class BronzeBracer(IronBracer):
    armor = 1

class BronzePlatemail(IronChainmail):
    name = "platemail"
    armor = 1

class BronzeGauntlet(IronGauntlet):
    armor = 1

class BronzeGreave(IronGreave):
    armor = 1

class BronzeHelm(IronHelm):
    armor = 1

class BronzeShield(IronShield):
    armor = 1

# Clothing
class Backpack(i.Holder):
    name = "backpack"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    level = 4
    descends = 0

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
    covers["arm"] = True
    level = 1
    descends = 1

class Dress(i.Item):
    name = "dress"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    covers["arm"] = True
    covers["leg"] = True
    level = 1
    descends = 1

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
    damage = 15

class CopperAxe(Axe):
    damage = 5

class Cleaver(i.Item):
    name = "cleaver"
    damage = 30

class Shiv(i.Item):
    name = "prison shiv"
    damage = 5

class Spear(i.Item):
    name = "spear"
    damage = 10

class CopperSpear(Spear):
    damage = 4

class IronSword(i.Item):
    name = "sword"
    damage = 20

class CopperSword(IronSword):
    damage = 7

class BronzeSword(IronSword):
    damage = 14

class Quarterstaff(i.Item):
    name = "quarterstaff"
    damage = 10

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
        "foot": (Slipper, Shoe)},
    "grasps": {},
    "color": ["red", "blue", "green", "yellow", "striped"],
    "color_scheme": "distinct",
    "texture": ["silk", "cotton", "wool"],
    "texture_scheme": "same",
    "full": True,
    }

backpack = {
    "wears": {
        "body": Backpack,
        },
    "grasps": {},
    "color": ["black", "brown"],
    "color_scheme": "distinct",
    "texture": ["leather", "cloth"],
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

armorsuit = {
    "wears": {
        "head": IronHelm,
        "body": IronChainmail,
        "arm": IronBracer,
        "left hand": [IronGauntlet, IronShield],
        "right hand": IronGauntlet,
        "leg": IronGreave,
        "foot": IronBoot},
    "grasps": {},
    "color": ["shiny", "rusty", "matte"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
    }

partial_armorsuit = copy.deepcopy(armorsuit)
partial_armorsuit["full"] = False

bronze_armorsuit = {
    "wears": {
        "head": BronzeHelm,
        "body": BronzePlatemail,
        "arm": BronzeBracer,
        "left hand": [BronzeGauntlet, BronzeShield],
        "right hand": BronzeGauntlet,
        "leg": BronzeGreave,
        "foot": BronzeBoot},
    "grasps": {},
    "color": ["shiny", "polished", "green"],
    "color_scheme": "same",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

partial_bronze_armorsuit = copy.deepcopy(bronze_armorsuit)
partial_bronze_armorsuit["full"] = False

# for creatures with two swords- remove shield
bronze_duelists_armorsuit = copy.deepcopy(bronze_armorsuit)
del bronze_duelists_armorsuit["wears"]["left hand"][1]

weapons = {
    "wears": {},
    "grasps": {
        "right hand": (IronSword, Spear, Axe)},
    "color": ["gray"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}

copper_weapons = {
    "wears": {},
    "grasps": {
        "right hand": (CopperSword, CopperSpear, CopperAxe)},
    "color": ["shiny", "polished", "gleaming"],
    "color_scheme": "same",
    "texture": ["copper"],
    "texture_scheme": "same",
    "full": True,
}

basic_weapons = {
    "wears": {},
    "grasps": {
        "right hand": Quarterstaff},
    "color": ["gray"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}
