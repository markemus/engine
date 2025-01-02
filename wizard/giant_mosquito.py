import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Proboscis(cr.Weapon):
    name = "proboscis"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_mouth"
    base_hp = 10
    size = 1
    eats = 1
    strength = 1
    _damage = 0
    weapon_effects = [eff.SuckBlood]

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Eye, Proboscis]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 15
    size = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (6, 7)
    wears = "animal_leg"
    base_hp = 20
    size = 3
    amble = 1/3

class Wing(cr.Limb):
    name = "wing"
    subelement_classes = []
    appendageRange = (2, 3)
    base_hp = 5
    size = 1
    flight = 1/2
    colors = ["translucent", "white"]
    textures = ["filmy", "delicate"]

class Abdomen(cr.Limb):
    name = "abdomen"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 3
    wears = "animal_abdomen"

class Thorax(cr.Limb):
    name = "thorax"
    subelement_classes = [Head, Leg, Wing, Abdomen]
    appendageRange = (1, 2)
    base_hp = 15
    size = 3
    wears = "animal_body"

class GiantMosquito(cr.creature):
    classname = "giant mosquito"
    team = "monster"
    namelist = ["giant mosquito"]
    baseElem = Thorax
    colors = ["black", "tan", "brown"]
    textures = ["haired"]
    suits = []
