import engine.creature as cr
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class MetalBody(cr.Limb):
    name = "drum"
    subelement_classes = [cl.MetalEye, cl.MetalTreads, cl.MetalTreads]
    isSurface = True
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 40
    size = 3
    _armor = 2

class DwarvenCleaner(cr.creature):
    """A small neutral mechanoid."""
    classname = "dwarven cleaner"
    team = "neutral"
    namelist = ["dwarven cleaner"]
    baseElem = MetalBody
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
    can_fear = False
    can_rest = False
    can_stun = False
    can_poison = False
    can_breathe = False
    # This creature cannot be enthralled or possessed
    strong_will = True
