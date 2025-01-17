import engine.ai as ai
import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nl


class Beak(cr.Weapon):
    name = "beak"
    subelement_classes = []
    _damage = 30
    appendageRange = (1, 2)
    wears = "beak"
    base_hp = 30
    size = 2
    eats = 1
    strength = 1
    colors = ["black", "gray", "steely"]
    textures = ["hooked"]
    _armor = 2

class Ear(cl.Ear):
    base_hp = 10
    _armor = 2

class Eye(cl.Eye):
    base_hp = 10

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Ear, Eye, Beak]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 40
    size = 2
    _armor = 2

class Claw(cr.Weapon):
    name = "claw"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    wears = "claw"
    base_hp = 10
    size = 1
    _damage = 25
    _armor = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Claw]
    isSurface = True
    appendageRange = (4, 5)
    wears = "animal_leg"
    base_hp = 35
    size = 2
    amble = 1/3
    strength = 1
    _armor = 2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 60
    size = 3
    _armor = 2

class Owlbear(cr.creature):
    """A ferocious creature that is impossible for most to ignore."""
    classname = "owlbear"
    team = "goblinkin"
    namelist = nl.names["dog"]
    baseElem = Torso
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["feathered"]
    suits = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai = ai.PestAI(self)

        weapons = self.subelements[0].limb_check("_damage")

        for weapon in weapons:
            weapon.weapon_effects = [eff.DrawAggro]
