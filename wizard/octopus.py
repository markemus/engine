import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nl


class Tentacle(cl.Tentacle):
    _damage = 20
    base_hp = 15
    size = 3
    appendageRange = (1, 2)
    amble = 1/2
    can_bleed = False
    # TODO entangle effect
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class Entangled(eff.Entangled):
            entangling_limb = self
        self.weapon_effects = [Entangled]


class Eye(cl.Eye):
    can_bleed = False


class Head(cr.Limb):
    name = "head"
    subelement_classes = [Eye, Tentacle]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 45
    size = 3
    flight = 1
    can_bleed = False
    passive_effects = [eff.SquirtInk]


class CaveOctopus(cr.creature):
    classname = "cave octopus"
    team = "fish"
    namelist = nl.names["octopus"]
    baseElem = Head
    colors = ["red", "yellow", "magenta", "blue", "cyan", "green"]
    textures = ["glowing"]
    # TODO suits for octopus (rock, shell)
    suits = []
