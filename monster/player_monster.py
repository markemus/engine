import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu

import monster.suits as msu

class PoisonJaw(cl.Jaw):
    subelement_classes = [cl.PoisonFangs, cl.Tongue]

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, PoisonJaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 15
    size = 2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 35
    size = 3

class SpiderLeg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (8, 9)
    wears = "spider_leg"
    base_hp = 10
    size = 2
    amble = 1/4

class Spinneret(cr.Weapon):
    name = "spinneret"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    blockable = False
    _damage = 0
    base_hp = 5
    weapon_effects = [eff.Webbed]

class Abdomen(cr.Limb):
    name = "abdomen"
    subelement_classes = [Spinneret]
    isSurface = True
    appendageRange = (1, 2)
    wears = "spider_abdomen"
    base_hp = 20
    size = 3

class Thorax(cr.Limb):
    name = "thorax"
    subelement_classes = [Torso, SpiderLeg, Abdomen]
    isSurface = True
    appendageRange = (1, 2)
    wears = "spider_body"
    base_hp = 30
    size = 3

class PlayerMonster(cr.creature):
    classname = "monster"
    team = "escapee"
    namelist = nm.names["human"]
    baseElem = Thorax
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["furred"]
    suits = [asu.backpack, msu.starter_weapon]


# TODO separate color for human torso and sublimbs