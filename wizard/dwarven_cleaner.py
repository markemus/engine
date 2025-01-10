import engine.creature as cr
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class MetalBody(cl.MetalLimb):
    name = "drum"
    subelement_classes = [cl.MetalEye, cl.MetalTreads, cl.MetalTreads]
    appendageRange = (1, 2)
    base_hp = 40
    size = 3


class DwarvenCleaner(cr.Mechanoid):
    """A small neutral mechanoid."""
    classname = "dwarven cleaner"
    team = "neutral"
    namelist = ["dwarven cleaner"]
    baseElem = MetalBody
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
