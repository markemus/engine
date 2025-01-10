import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Nozzle(cl.MetalWeapon):
    name = "nozzle"
    appendageRange = (1, 2)
    subelement_classes = []
    blockable = False
    base_hp = 7
    _damage = 5
    size = 1
    weapon_effects = [eff.FireDOT]


class Hose(cl.MetalLimb):
    name = "hose"
    appendageRange = (1, 2)
    subelement_classes = [Nozzle]
    base_hp = 15
    size = 2


class MetalTank(cl.MetalLimb):
    name = "tank"
    appendageRange = (1, 2)
    subelement_classes = [cl.MetalEye, Hose, cl.MetalTreads]
    base_hp = 25
    size = 3


class DwarvenFlamethrower(cr.Mechanoid):
    classname = "dwarven flamethrower"
    team = "dwarven"
    namelist = ["dwarven flamethrower"]
    baseElem = MetalTank
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
