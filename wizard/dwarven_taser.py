import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Taser(cl.MetalWeapon):
    name = "taser"
    appendageRange = (1, 2)
    subelement_classes = []
    blockable = False
    base_hp = 10
    _damage = 5
    size = 2


class Turret(cl.MetalLimb):
    name = "turret"
    appendageRange = (1, 2)
    subelement_classes = [Taser]
    base_hp = 15
    size = 2


class MetalFrame(cl.MetalLimb):
    name = "frame"
    appendageRange = (1, 2)
    subelement_classes = [Turret, cl.MetalEye, cl.MetalSpiderLeg]
    base_hp = 25
    size = 3


class DwarvenTaser(cr.Mechanoid):
    classname = "dwarven taser"
    team = "dwarven"
    namelist = ["dwarven taser"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Lightning(eff.Lightning):
            caster = self

        self.subelements[0].subelements[0].subelements[0].weapon_effects = [Lightning]
