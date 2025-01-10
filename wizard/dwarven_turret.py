import engine.creature as cr

import assets.commonlimbs as cl


class Gun(cl.MetalWeapon):
    name = "gun"
    appendageRange = (1, 2)
    subelement_classes = []
    blockable = False
    base_hp = 10
    _damage = 10
    size = 2


class Turret(cl.MetalLimb):
    name = "turret"
    appendageRange = (1, 2)
    subelement_classes = [Gun]
    base_hp = 15
    size = 2


class MetalFrame(cl.MetalLimb):
    name = "frame"
    appendageRange = (1, 2)
    subelement_classes = [Turret, cl.MetalEye, cl.MetalSpiderLeg]
    base_hp = 25
    size = 3


class DwarvenTurret(cr.Mechanoid):
    classname = "dwarven turret"
    team = "dwarven"
    namelist = ["dwarven turret"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
