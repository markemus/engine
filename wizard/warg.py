import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm


class Fang(cl.Teeth):
    name = "fang"
    appendageRange = (2, 3)
    _damage = 20
    colors = ["flaming"]
    textures = ["slavering"]
    weapon_effects = [eff.FireDOT]
    base_hp = 10
    _armor = 2

class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [cl.Nose, Fang, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 20
    size = 1
    eats = 1
    strength = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wear = "animal_head"
    vital = True
    base_hp = 20
    size = 2

class Claw(cr.Weapon):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 3
    size = 1
    _damage = 10

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "animal_leg"
    base_hp = 10
    size = 2
    amble = 1/3
    strength = 1

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 5
    size = 1

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 50
    size = 3

class Warg(cr.creature):
    classname = "warg"
    team = "goblinkin"
    namelist = ["warg"]
    baseElem = Torso
    colors = ["black"]
    textures = ["furred"]
    suits = []
