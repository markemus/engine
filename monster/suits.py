import engine.item as i

import engine.effectsbook as eff


class Labcoat(i.Item):
    name = "lab coat"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["leg"] = True
    covers["arm"] = True
    level = 2
    descends = 1

# Guard uniform
class GuardHat(i.Item):
    name = "guard hat"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    level = 2
    descends = 0

class Slacks(i.Item):
    name = "slacks"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    level = 1
    descends = 0

class Shoe(i.Item):
    name = "shoe"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["foot"] = True
    level = 1
    descends = 0

class UniformShirt(i.Item):
    name = "uniform shirt"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["arm"] = True
    level = 1
    descends = 1


class CagePole(i.Item):
    name = "cage pole"
    damage = 5

class Taser(i.Item):
    name = "taser"
    damage = 3.5
    weapon_effects = [eff.StunIfUnarmored]

class Club(i.Item):
    name = "club"
    damage = 15
    weapon_effects = [eff.Stun]


lab_coat = {
    "grasps": {},
    "wears": {
        "body": Labcoat,
    },
    "color": ["white"],
    "color_scheme": "same",
    "texture": ["cloth"],
    "texture_scheme": "same",
    "full": True,
}

guardsuit = {
    "wears": {
        "head": GuardHat,
        "body": UniformShirt,
        "leg": Slacks,
        "foot": Shoe},
    "grasps": {},
    "color": ["blue", "black", "gray"],
    "color_scheme": "same",
    "texture": ["linen"],
    "texture_scheme": "same",
    "full": True,
    }


starter_weapon = {
    "grasps": {
        "right hand": CagePole,
    },
    "wears": {},
    "color": ["black"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}

taser = {
    "grasps": {
        "right hand": Taser,
    },
    "wears": {},
    "color": ["black", "blue", "orange", "yellow"],
    "color_scheme": "same",
    "texture": ["plastic"],
    "texture_scheme": "same",
    "full": True,
}

club = {
    "grasps": {
        "right hand": Club,
    },
    "wears": {},
    "color": ["stained", "cracked", "rustic", "splintery"],
    "color_scheme": "same",
    "texture": ["wooden"],
    "texture_scheme": "same",
    "full": True,
}