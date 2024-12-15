"""A three-headed dog who guards the gates of hell."""
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

class TripleHead(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (3, 4)
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

class CTorso(Torso):
    subelement_classes = [TripleHead, Leg]


class Dog(cr.creature):
    classname = "dog"
    team = "monster"
    namelist = nm.names["dog"]
    baseElem = Torso
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["furred"]
    suits = []

class Cerberus(Dog):
    """A dog with three heads."""
    classname = "cerberus"
    team = "monster"
    baseElem = CTorso
