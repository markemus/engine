import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Cannon(cl.MetalWeapon):
    name = "cannon"
    appendageRange = (1, 2)
    subelement_classes = []
    blockable = False
    base_hp = 10
    _damage = 10
    size = 2
    weapon_effects = [eff.Explosive]


class Turret(cl.MetalLimb):
    name = "turret"
    appendageRange = (1, 2)
    subelement_classes = [Cannon]
    base_hp = 15
    size = 2


class MetalFrame(cl.MetalLimb):
    name = "frame"
    appendageRange = (1, 2)
    subelement_classes = [Turret, cl.MetalEye, cl.MetalTreads]
    base_hp = 25
    size = 3


class DwarvenTank(cr.Mechanoid):
    classname = "dwarven tank"
    team = "dwarven"
    namelist = ["dwarven tank"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
