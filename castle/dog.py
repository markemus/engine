"""A three-headed dog who guards the gates of hell."""
import engine.creature as cr

import castle.commonlimbs as cl
import castle.namelists as nm


class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [cl.Nose, cl.Teeth, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 5

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True
    base_hp = 8

class TripleHead(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (3, 4)
    wear = "head"
    vital = True
    base_hp = 8

class Claw(cr.Limb):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 3

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "leg"
    base_hp = 15

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 3
    
class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 30

class CTorso(Torso):
    subelement_classes = [TripleHead, Leg, Tail]


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