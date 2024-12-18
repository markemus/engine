import engine.item as i


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

class LightBracer(i.Item):
    name = "bracer of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["arm"] = True
    covers["arm"] = True
    armor = 2
    level = 3
    descends = 0

class LightBreastplate(i.Item):
    name = "breastplate of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["body"] = True
    canwear["animal_body"] = True
    covers["animal_body"] = True
    armor = 2
    level = 3
    descends = 0

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

class LightGreave(i.Item):
    name = "greave of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["leg"] = True
    covers["leg"] = True
    canwear["animal_leg"] = True
    covers["animal_leg"] = True
    armor = 2
    level = 3
    descends = 0

class LightHelm(i.Item):
    name = "helm of light"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["head"] = True
    canwear["animal_head"] = True
    covers["head"] = True
    covers["eye"] = True
    covers["ear"] = True
    covers["nose"] = True
    covers["mouth"] = True
    covers["teeth"] = True
    covers["tongue"] = True
    covers["animal_head"] = True
    covers["snout"] = True
    covers["fangs"] = True
    armor = 2
    level = 3
    descends = 2


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
