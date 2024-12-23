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
    base_hp = 5
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

class Wing(cr.Limb):
    name = "wing"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "wing"
    base_hp = 5
    size = 1
    flight = 1/2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Wing]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 15
    size = 2

class GiantBat(cr.creature):
    """A giant flying rat."""
    classname = "giant bat"
    aggressive = True
    team = "prey"
    namelist = ["giant bat"]
    baseElem = Torso
    colors = ["gray", "black", "brown"]
    textures = ["furred"]
    suits = []
