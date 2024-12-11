"""A cute little critter, mostly harmless."""
import engine.creature as cr

import castle.commonlimbs as cl
import castle.namelists as nm


class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [cl.Teeth, cl.Tongue, cl.Nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True

class Claw(cr.Limb):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "leg"

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class Cat(cr.creature):
    classname = "cat"
    aggressive = False
    team = None
    namelist = nm.names["cat"]
    baseElem = Torso
    colors = ["white", "tabby", "tortoiseshell", "gray"]
    textures = ["furred"]
    suits = []
