import engine.creature as cr
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class MetalWheel(cr.Limb):
    name = "wheel"
    appendageRange = (1, 2)
    wears = "foot"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    base_hp = 10
    _armor = 2
    size = 2
    amble = 1 / 2

class MetalBody(cr.Limb):
    name = "body"
    subelement_classes = [cl.MetalArm, MetalWheel, MetalWheel]
    isSurface = True
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3
    _armor = 2

class DwarvenSnatcher(cr.creature):
    """A small mechanoid that can wield a weapon."""
    classname = "dwarven snatcher"
    team = "dwarven"
    namelist = ["dwarven snatcher"]
    baseElem = MetalBody
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = [asu.iron_weapons]
    can_fear = False
    can_rest = False
    can_stun = False
    can_poison = False
    can_breathe = False
    # This creature cannot be enthralled or possessed
    strong_will = True
