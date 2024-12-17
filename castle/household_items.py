"""These collections are used to populate rooms. The texture and color options define the strategy for
how the items are themed.
linens = {
    # Items that will be spawned in Furniture
    "contains": [Pillow, Blanket, Sheet],
    # Color and texture info tells the generator how to color the created items
    # color_ and texture_ scheme can be either "same", "distinct", or "unique".
    # same: all items get the same color and texture.
    # distinct: items of the same type (eg shoes) will be the same color and texture.
    # unique: all items get their own color and texture.
    "color": ["blue", "green", "silver", "brown"],
    "color_scheme": "distinct",
    "texture": ["quilted", "patterned", "wool", "linen"],
    "texture_scheme": "same",
    # Whether the full set will be placed in each piece of Furniture, or only a subset.
    "full": True,
}"""
from engine import item as it
from engine import suits_and_collections as sc

from castle import castle_collections as cst
from castle import commonlimbs as cl
from castle import human
from castle import potions


class Blanket(it.Item):
    name = "blanket"
    canwear = it.Item.canwear.copy()
    covers = it.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    covers["head"] = True
    armor = 1
    descends = 1
    level = 2

class CandleStick(it.Item):
    name = "candlestick"
    damage = 3

class Goblet(it.Item):
    name = "goblet"

class Hammer(it.Item):
    name = "hammer"
    damage = 10

class Pillow(it.Item):
    name = "pillow"
    canwear = it.Item.canwear.copy()
    covers = it.Item.covers.copy()
    canwear["arm"] = True
    covers["arm"] = True
    armor = 1
    descends = 0
    level = 2

class Plate(it.Item):
    name = "plate"

class Pliers(it.Item):
    name = "pliers"

class Screwdriver(it.Item):
    name = "screwdriver"
    damage = 3

class Sheet(it.Item):
    name = "sheet"

class Utensils(it.Item):
    name = "utensils"

class Pillowcase(it.Holder):
    name = "pillowcase"


# Collections
candles = {
    "contains": [CandleStick],
    "color": ["shiny", "tarnished"],
    "color_scheme": "same",
    "texture": ["copper", "silver", "gold"],
    "texture_scheme": "same",
    "full": True,
}

linens = {
    "contains": [Pillow, Blanket, Sheet],
    "color": ["blue", "green", "silver", "brown"],
    "color_scheme": "distinct",
    "texture": ["quilted", "patterned", "wool", "linen"],
    "texture_scheme": "same",
    "full": True,
}

prison_linens = {
    "contains": [Pillow, Blanket],
    "color": ["gray", "dingy", "brown"],
    "color_scheme": "same",
    "texture": ["wool", "linen"],
    "texture_scheme": "same",
    "full": True,
}

silver = {
    "contains": [Plate, Utensils, Goblet],
    "color": ["shiny", "tarnished"],
    "color_scheme": "same",
    "texture": ["copper", "silver", "gold"],
    "texture_scheme": "same",
    "full": True,
}
tools = {
    "contains": [Hammer, Pliers, Screwdriver],
    "color": ["black", "gray"],
    "color_scheme": "distinct",
    "texture": ["metal", "iron"],
    "texture_scheme": "distinct",
    "full": False,
}

# TODO-DECIDE collections should have a no color option so objects can keep their default colors?
medicine = {
    "contains": [potions.ArmGrowthPotion, potions.LegGrowthPotion, potions.PotionOfHealing],
    "color": ["gray"],
    "color_scheme": "distinct",
    "texture": ["murky"],
    "texture_scheme": "distinct",
    "full": False,
}

# Goblins will carry some of this stuff around to feed to prisoner
potions_suit = {
    "wears": {},
    "grasps": {
        "left hand": (potions.ArmGrowthPotion, potions.LegGrowthPotion, potions.TentacleGrowthPotion),
    },
    "color": ["gray"],
    "color_scheme": "distinct",
    "texture": ["murky"],
    "texture_scheme": "distinct",
    "full": False,
}

# Kitchen
arms_and_legs = sc.limbs_to_collection(limbs=[(cl.RArm, cl.LArm, cl.Leg, cl.Tentacle)], model=human.Human)

class KitchenKnife(it.Item):
    name = "kitchen knife"
    _damage = 3

class CuttingBoard(it.Holder):
    name = "cutting board"
    vis_collections = [(arms_and_legs, (1, 2))]

class Pan(it.Holder):
    name = "pan"
    vis_collections = [(arms_and_legs, (1, 2))]

class Pot(it.Holder):
    name = "pot"
    vis_collections = [(arms_and_legs, (1, 2))]

class Stew(it.Potion):
    name = "meat stew"

food = {
    "contains": [Stew],
    "color": ["red", "brown"],
    "color_scheme": "same",
    "texture": ["meaty", "chunky"],
    "texture_scheme": "same",
    "full": True,
}

class ServingBowl(it.Holder):
    name = "serving dish"
    vis_collections = [(food, (1, 2))]

cookery = {
    "contains": [Pot, Pan],
    "color": ["black", "gray", "grimy", "sooty"],
    "color_scheme": "same",
    "texture": ["iron", "stainless steel", "steel"],
    "texture_scheme": "distinct",
    "full": False,
}

cooking_utensils = {
    "contains": [KitchenKnife],
    "color": ["gray", "black", "white"],
    "color_scheme": "same",
    "texture": ["steel", "ceramic"],
    "texture_scheme": "same",
    "full": True,
}

cooking_tools = {
    "contains": [CuttingBoard],
    "color": ["brown"],
    "color_scheme": "same",
    "texture": ["wood"],
    "texture_scheme": "same",
    "full": True,
}

# TODO-DECIDE we need a way to coordinate chairs, place settings, and serving utensils. Right? A meta random roll.
serving_utensils = {
    "contains": [ServingBowl],
    "color": ["shiny"],
    "color_scheme": "same",
    "texture": ["silver"],
    "texture_scheme": "same",
    "full": True,
}