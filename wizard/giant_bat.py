import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl


class Fang(cr.Weapon):
    name = "fang"
    subelement_classes = []
    _damage = 3
    appendageRange = (2, 3)
    wears = "fang"
    base_hp = 5
    size = 1
    colors = ["yellow"]
    textures = ["enameled"]

class Snout(cr.Limb):
    name = "snout"
    subelement_classes = [Fang, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "snout"
    base_hp = 5
    size = 1
    eats = 1
    strength = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, Snout]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = "head"
    base_hp = 10
    size = 1

class Wing(cr.Limb):
    name = "wing"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "wing"
    base_hp = 5
    size = 2
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
    """A giant flying rat. Its bite drains its enemy's blood and heals it."""
    classname = "giant bat"
    aggressive = True
    team = "prey"
    namelist = ["giant bat"]
    baseElem = Torso
    colors = ["gray", "black", "brown"]
    textures = ["furred"]
    suits = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vampire bat
        fangs = [x for x in self.subelements[0].limb_check("name") if x.name == "fang"]
        class CVampirism(eff.Vampirism):
            vampire = self
            amount = 2

        for fang in fangs:
            fang.weapon_effects = [CVampirism]
