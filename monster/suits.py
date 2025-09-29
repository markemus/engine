import engine.item as i


class Labcoat(i.Item):
    name = "lab coat"
    canwear = i.Item.canwear.copy()
    covers = i.Item.covers.copy()
    canwear["body"] = True
    covers["leg"] = True
    covers["arm"] = True
    level = 2
    descends = 1

class CagePole(i.Item):
    name = "cage pole"
    damage = 7



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
