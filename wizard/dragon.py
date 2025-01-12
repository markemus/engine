import engine.ai
import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "ear"
    base_hp = 15
    _armor = 3
    size = 1
    can_burn = False


class Eye(cr.Weapon):
    name = "eye"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "eye"
    see = 1
    base_hp = 15
    _armor = 3
    size = 1
    can_burn = False
    colors = ["blue", "hazel", "black", "brown", "green"]
    textures = ["colored"]
    _damage = 0
    weapon_effects = [eff.StunForSure]


class Horn(cr.Weapon):
    name = "horn"
    subelement_classes = []
    _damage = 30
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"
    can_burn = False
    base_hp = 25
    _armor = 3
    size = 1
    colors = ["black", "gray", "brown"]
    textures = ["smooth"]
    weapon_effects = [eff.Bleed]


class Nose(cr.Limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"
    base_hp = 15
    _armor = 3
    size = 1
    can_burn = False


class Fang(cr.Weapon):
    name = "fang"
    subelement_classes = []
    _damage = 30
    appendageRange = (2, 3)
    wears = "fang"
    base_hp = 25
    _armor = 4
    size = 1
    can_burn = False
    colors = ["white"]
    textures = ["enameled"]


class Tongue(cr.Limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"
    base_hp = 15
    _armor = 2
    size = 1
    can_burn = False
    colors = ["red"]
    textures = ["fleshy"]


class Snout(cr.Weapon):
    name = "snout"
    subelement_classes = [Nose, Fang, Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 25
    _armor = 3
    size = 1
    can_burn = False
    eats = 1
    _damage = 30
    weapon_effects = [eff.Firebreath]


class Head(cr.Limb):
    name = "head"
    subelement_classes = [Ear, Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 45
    _armor = 3
    size = 2
    can_burn = False


class TripleNeck(cr.Limb):
    name = "neck"
    subelement_classes = [Head]
    appendageRange = (3, 4)
    base_hp = 40
    _armor = 3
    size = 2
    blocker = True
    can_burn = False


class Claw(cr.Weapon):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 15
    _armor = 4
    size = 1
    can_burn = False
    _damage = 20


class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "leg"
    base_hp = 50
    _armor = 3
    size = 2
    can_burn = False
    amble = 1/3


class Wing(cr.Limb):
    name = "wing"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "wing"
    base_hp = 30
    _armor = 1
    size = 2
    can_burn = False
    flight = 1/2
    colors = ["thin"]
    textures = ["skin"]


class Tail(cr.Limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    base_hp = 60
    _armor = 3
    size = 2
    blocker = True
    can_burn = False


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [TripleNeck, Wing, Leg, Tail]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 90
    _armor = 3
    size = 3
    can_burn = False
    passive_effects = [eff.HealAllies]


class Dragon(cr.creature):
    classname = "dragon"
    team = "dragon"
    namelist = ["Vistaseragoth"]
    baseElem = Torso
    colors = ["black", "red", "gold", "white", "green", "silver"]
    textures = ["scaled"]
    suits = []
    strong_will = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai = engine.ai.PestAI(self)
