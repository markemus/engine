import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nl

import wizard.suits as wsu


class Tentacle(cl.Tentacle):
    base_hp = 15
    size = 3
    appendageRange = (8, 9)
    amble = 1
    _damage = 10
    strength = 1.5


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Eye, Tentacle]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = "head"
    base_hp = 45
    size = 3
    flight = 1
    passive_effects = [eff.SquirtInk]


class CaveOctopus(cr.Fish):
    classname = "cave octopus"
    team = "squids"
    namelist = nl.names["octopus"]
    baseElem = Head
    colors = ["red", "yellow", "magenta", "blue", "cyan", "green"]
    textures = ["glowing"]
    suits = [wsu.octopus_gear]
