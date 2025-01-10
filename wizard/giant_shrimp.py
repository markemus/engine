"""A gigantic blind shrimp that lives in shallow cave lakes deep beneath the earth."""
import engine.creature as cr

class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "tail"
    base_hp = 7
    size = 1
    flight = 1
    _armor = 2

class Head(cr.Limb):
    name = "head"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 15
    size = 1
    _armor = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (8, 9)
    wears = "animal_leg"
    base_hp = 10
    size = 2
    amble = 1/4
    _armor = 2

class Claw(cr.Weapon):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 2
    _armor = 2
    _damage = 15

class Arm(cr.Limb):
    name = "arm"
    subelement_classes = [Claw]
    appendageRange = (2, 3)
    base_hp = 25
    size = 2
    _armor = 2
    strength = 1

class Torso(cr.Limb):
    name = "carapace"
    subelement_classes = [Head, Arm, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 25
    size = 2
    _armor = 2

class BlindCaveShrimp(cr.Fish):
    """A big blind shrimp that lives in lakes in caves."""
    classname = "cave shrimp"
    aggressive = True
    team = "prey"
    namelist = ["cave shrimp"]
    baseElem = Torso
    colors = ["pale", "white", "translucent"]
    textures = ["armored"]
    suits = []
