import engine.creature as cr
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class MetalFrame(cr.Limb):
    name = "frame"
    subelement_classes = [cl.MetalArm, cl.MetalEye, cl.MetalTreads, cl.MetalTreads]
    isSurface = True
    can_bleed = False
    can_heal = False
    can_burn = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 40
    size = 3
    _armor = 2

class DwarvenSnatcher(cr.creature):
    """A small mechanoid that can wield a weapon."""
    classname = "dwarven snatcher"
    team = "dwarven"
    namelist = ["dwarven snatcher"]
    baseElem = MetalFrame
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
