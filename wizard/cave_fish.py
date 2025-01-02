"""A gigantic blind cave fish, it dwells in shallow lakes deep beneath the earth."""
import engine.creature as cr
import assets.commonlimbs as cl

class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 15
    appendageRange = (1, 2)
    wears = "fang"
    base_hp = 10
    size = 1
    colors = ["white"]
    textures = ["sharp"]

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Teeth, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 7
    size = 1
    eats = 1
    _armor = 2
    strength = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 15
    size = 1
    _armor = 2

class Fin(cr.Limb):
    name = "fin"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "fin"
    base_hp = 7
    size = 1
    flight = 1/2

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "tail"
    base_hp = 7
    size = 1
    flight = 1

class Torso(cr.Limb):
    name = "body"
    subelement_classes = [Head, Fin, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 25
    size = 2
    _armor = 2

class BlindCaveFish(cr.creature):
    """A gigantic blind fish that lives in cave lakes deep beneath the surface."""
    classname = "cave fish"
    aggressive = True
    can_breathe = False
    team = "prey"
    namelist = ["cave fish"]
    baseElem = Torso
    colors = ["pale", "white", "translucent"]
    textures = ["slimy", "scaled"]
    suits = []
