"""A giant version of a cute little critter."""
import engine.creature as cr

import assets.commonlimbs as cl


class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 3
    appendageRange = (1, 2)
    wears = "fangs"
    base_hp = 3
    size = 1
    colors = ["yellow"]
    textures = ["enameled"]

class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [Teeth, cl.Tongue]
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
    wears = "animal_head"
    vital = True
    base_hp = 10
    size = 1

class Claw(cr.Limb):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 3
    size = 1

class Paw(cr.Limb):
    name = "paw"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "paw"
    base_hp = 3
    size = 1
    amble = 1/3

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Paw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "animal_leg"
    base_hp = 5
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
    wears = "animal_body"
    base_hp = 15
    size = 2

class GiantRat(cr.creature):
    """Although much larger than a common rat, this creature still has a well-earned reputation as a creature
    for children to practice their skills against."""
    classname = "giant rat"
    aggressive = True
    team = "prey"
    namelist = ["giant rat"]
    baseElem = Torso
    colors = ["gray", "black", "brown"]
    textures = ["furred"]
    suits = []
