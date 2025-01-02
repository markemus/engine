import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nl


class Tentacle(cl.Tentacle):
    _damage = 20
    base_hp = 15
    size = 3
    appendageRange = (8, 9)
    amble = 1
    # TODO-DONE entangle effect

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Eye, Tentacle]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 45
    size = 3
    flight = 1
    passive_effects = [eff.SquirtInk]


class CaveOctopus(cr.creature):
    classname = "cave octopus"
    team = "prey"
    namelist = nl.names["octopus"]
    baseElem = Head
    colors = ["red", "yellow", "magenta", "blue", "cyan", "green"]
    textures = ["glowing"]
    # TODO suits for octopus (rock, shell)
    suits = []
