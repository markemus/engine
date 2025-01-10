import engine.creature as cr
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class MetalFrame(cl.MetalLimb):
    name = "frame"
    subelement_classes = [cl.MetalArm, cl.MetalEye, cl.MetalTreads, cl.MetalTreads]
    appendageRange = (1, 2)
    base_hp = 40
    size = 3


class DwarvenSnatcher(cr.Mechanoid):
    """A small mechanoid that can wield a weapon."""
    classname = "dwarven snatcher"
    team = "dwarven"
    namelist = ["dwarven snatcher"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = [asu.steel_weapons]
    mastery = 2
