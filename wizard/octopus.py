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
    vital = True
    base_hp = 45
    size = 3
    flight = 1
    passive_effects = [eff.SquirtInk]


# TODO octopi (and other fish) should die if they go on land (look for location.wet tag)
class CaveOctopus(cr.Fish):
    classname = "cave octopus"
    team = "squids"
    namelist = nl.names["octopus"]
    baseElem = Head
    colors = ["red", "yellow", "magenta", "blue", "cyan", "green"]
    textures = ["glowing"]
    # TODO-DONE suits for octopus (rock, shell)
    suits = [wsu.octopus_gear]
