"""A cute little critter, mostly harmless."""
import engine.creature as cr

import castle.commonlimbs as cl
import castle.namelists as nm


class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [cl.Nose, cl.Teeth, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 1
    size = 1
    eats = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True
    base_hp = 5
    size = 1

class Claw(cr.Limb):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 3
    size = 1

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "leg"
    base_hp = 10
    size = 2

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 3
    size = 2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 15
    size = 2

class Cat(cr.creature):
    classname = "cat"
    aggressive = False
    team = "neutral"
    namelist = nm.names["cat"]
    baseElem = Torso
    colors = ["white", "tabby", "tortoiseshell", "gray"]
    textures = ["furred"]
    suits = []
