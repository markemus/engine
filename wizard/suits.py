import engine.item as i

import assets.suits as su

import engine.effectsbook as eff


# Light suit
class LightBoot(i.Item):
    name = "boot of light"
    # canwear[limb_type] governs where the item can be worn by a creature
    # covers[limb_type] governs which limbs will be protected by the worn item.
    # descends tells the engine how far down the limb hierarchy to look for the covers limb types.
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    canwear["paw"] = True
    covers["foot"] = True
    covers["paw"] = True
    covers["claw"] = True
    armor = 2
    level = 3
    descends = 1
    cannot_remove = True

class LightBracer(i.Item):
    name = "bracer of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["arm"] = True
    covers["arm"] = True
    armor = 2
    level = 3
    descends = 0
    cannot_remove = True

class LightBreastplate(i.Item):
    name = "breastplate of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    canwear["animal_body"] = True
    covers["animal_body"] = True
    canwear["spider_body"] = True
    covers["spider_body"] = True
    armor = 2
    level = 3
    descends = 0
    cannot_remove = True

class LightGauntlet(i.Item):
    name = "gauntlet of light"
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
    cannot_remove = True

class LightGreave(i.Item):
    name = "greave of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    covers["leg"] = True
    canwear["animal_leg"] = True
    covers["animal_leg"] = True
    canwear["spider_leg"] = True
    covers["spider_leg"] = True
    armor = 2
    level = 3
    descends = 0
    cannot_remove = True

class LightHelm(i.Item):
    name = "helm of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    canwear["animal_head"] = True
    canwear["spider_head"] = True
    covers["head"] = True
    covers["eye"] = True
    covers["ear"] = True
    covers["nose"] = True
    covers["mouth"] = True
    covers["teeth"] = True
    covers["tongue"] = True
    covers["animal_head"] = True
    covers["spider_head"] = True
    covers["snout"] = True
    covers["fangs"] = True
    armor = 2
    level = 3
    descends = 2
    cannot_remove = True

# Spider armor for dark elf companions
class SpiderBronzeBreastplate(i.Item):
    name = "spider breastplate"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["spider_body"] = True
    covers["spider_body"] = True
    descends = 0
    level = 3
    armor = 1

class SpiderBronzeHelm(i.Item):
    name = "spider helm"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["spider_head"] = True
    covers["spider_head"] = True
    covers["spider_head"] = True
    covers["eye"] = True
    covers["mouth"] = True
    covers["fangs"] = True
    descends = 2
    level = 3
    armor = 1

class SpiderBronzeGreave(i.Item):
    name = "spider greave"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["spider_leg"] = True
    covers["spider_leg"] = True
    descends = 0
    level = 3
    armor = 1


# Mana gear
class RingOfMana(i.Item):
    """A ring that stores a small amount of mana."""
    name = "ring of mana"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["finger"] = True
    covers["finger"] = True
    level = 2
    base_mana = 5
    mana = base_mana
    colors = ["sapphire", "ruby", "emerald", "diamond"]
    textures = ["in silver", "in gold", "in platinum"]

class ManaLocket(i.Item):
    """A locket that stores a moderate amount of mana."""
    name = "locket of mana"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    level = 2
    base_mana = 30
    mana = base_mana
    colors = ["sapphire", "ruby", "emerald", "diamond"]
    textures = ["in silver", "in gold", "in platinum"]


# Magic weapons
class BronzeSwordOfFire(su.BronzeSword):
    effects = [eff.FireDOT]

class BronzeSwordOfLight(su.BronzeSword):
    effects = [eff.Light]

class BronzePoisonedScimitar(su.BronzeSword):
    effects = [eff.Poison]

class IronSwordOfFire(su.IronSword):
    effects = [eff.FireDOT]

class IronSwordOfLight(su.IronSword):
    effects = [eff.Light]

class IronPoisonedScimitar(su.IronSword):
    effects = [eff.Poison]


class BronzeFlail(i.Item):
    name = "flail"
    damage = 12
    effects = [eff.Bleed]

class IronFlail(i.Item):
    name = "flail"
    damage = 17
    effects = [eff.Bleed]

# Suits
darkelfsuit = {
"wears": {
        "body": su.Tunic,
        "leg": su.Hose,
        "foot": (su.Slipper, su.Shoe)},
    "grasps": {},
    "color": ["black"],
    "color_scheme": "distinct",
    "texture": ["spider silk"],
    "texture_scheme": "same",
    "full": True,
}


lightsuit = {
    "wears": {
        "head": LightHelm,
        "body": LightBreastplate,
        "arm": LightBracer,
        "left hand": LightGauntlet,
        "right hand": LightGauntlet,
        "leg": LightGreave,
        "foot": LightBoot,
        "animal_head": LightHelm,
        "animal_body": LightBreastplate,
        "animal_leg": LightGreave,
        "paw": LightBoot
    },
    "grasps": {},
    "color": ["blue", "white", "gold"],
    "color_scheme": "same",
    "texture": ["glowing", "shining"],
    "texture_scheme": "same",
    "full": True,
    }

spider_bronze_suit = {
    "wears": {
        "spider_head": SpiderBronzeHelm,
        "spider_body": SpiderBronzeBreastplate,
        "spider_leg": SpiderBronzeGreave,
    },
    "grasps": {},
    "color": ["burnished", "shiny", "orange", "greenish"],
    "color_scheme": "unique",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

lightsword_ethereal = {
    "grasps": {
        "right hand": BronzeSwordOfLight,
    },
    "wears": {},
    "color": ["glowing"],
    "color_scheme": "same",
    "texture": ["ethereal"],
    "texture_scheme": "same",
    "full": True,
}

bronze_lightsword = {
    "grasps": {
        "right hand": BronzeSwordOfLight,
    },
    "wears": {},
    "color": ["glowing"],
    "color_scheme": "same",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

bronze_firesword = {
    "grasps": {
        "right hand": BronzeSwordOfFire,
    },
    "wears": {},
    "color": ["firey"],
    "color_scheme": "same",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

bronze_poisonsword = {
    "grasps": {
        "right hand": BronzePoisonedScimitar,
    },
    "wears": {},
    "color": ["burnished", "shiny", "orange", "greenish"],
    "color_scheme": "same",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

bleedflail = {
    "grasps": {
        "right hand": BronzeFlail,
    },
    "wears": {},
    "color": ["burnished", "shiny", "orange", "greenish"],
    "color_scheme": "same",
    "texture": ["bronze"],
    "texture_scheme": "same",
    "full": True,
}

double_iron_poisonsword = {
    "grasps": {
        "right hand": IronPoisonedScimitar,
        "left hand": IronPoisonedScimitar,
    },
    "wears": {},
    "color": ["burnished", "shiny", "orange", "greenish"],
    "color_scheme": "unique",
    "texture": ["iron"],
    "texture_scheme": "same",
    "full": True,
}