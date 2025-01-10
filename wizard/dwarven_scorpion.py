import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Stinger(cl.MetalWeapon):
    name = "stinger"
    appendageRange = (1, 2)
    subelement_classes = []
    base_hp = 10
    _damage = 20
    size = 2
    weapon_effects = [eff.Poison]


class Tail(cl.MetalLimb):
    name = "tail"
    appendageRange = (1, 2)
    wears = "tail"
    subelement_classes = [Stinger]
    blocker = True
    base_hp = 30
    size = 2


class MetalFrame(cl.MetalLimb):
    name = "frame"
    subelement_classes = [cl.MetalEye, cl.MetalSpiderLeg, Tail]
    appendageRange = (1, 2)
    base_hp = 40
    size = 3


class DwarvenScorpion(cr.Mechanoid):
    classname = "dwarven scorpion"
    team = "dwarven"
    namelist = ["dwarven scorpion"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
    mastery = 2
