"""A small creature that doesn't fight but can heal friendly creatures."""
import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm

import wizard.suits as wsu



class PointyEar(cr.Limb):
    name = "pointy ear"
    subelement_classes = []
    appendageRange = (2, 3)
    base_hp = 3
    size = 1

class FairyWing(cr.Limb):
    name = "wing"
    subelement_classes = []
    appendageRange = (2, 3)
    base_hp = 5
    size = 1
    flight = 1/2
    colors = ["translucent", "white"]
    textures = ["lacy", "airy", "light"]

class TinyHead(cr.Limb):
    name = "head"
    subelement_classes = [PointyEar, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 7
    size = 1

class FairyTorso(cr.Limb):
    name = "torso"
    subelement_classes = [TinyHead, FairyWing, cl.TinyRArm, cl.TinyLArm, cl.TinyLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 15
    size = 2
    passive_effects = [eff.HealAllies]

class Fairy(cr.creature):
    classname = "fairy"
    team = "neutral"
    aggressive = False
    namelist = nm.names["elf"]
    baseElem = FairyTorso
    colors = ["pale"]
    textures = ["skinned"]
    suits = [wsu.summoned_fairysuit]

class DarkElfFairy(Fairy):
    team = "dark elf"
    suits = [wsu.darkelf_fairysuit]
