import copy

import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu

import wizard.suits as wsu


class Ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"
    base_hp = 7
    size = 2
    _armor = 3

class Nose(cr.Limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"
    base_hp = 7
    size = 2
    _armor = 3

class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 7
    appendageRange = (1, 2)
    wears = "teeth"
    base_hp = 15
    size = 1
    colors = ["gray"]
    textures = ["stony"]
    _armor = 3

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Teeth, cl.Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 5
    size = 1
    eats = 1
    strength = 1
    _armor = 3

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Ear, cl.Eye, Nose, Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 30
    size = 2
    _armor = 3

class LargeRHand(cl.RHand):
    base_hp = int(cl.RHand.base_hp * 2)
    _armor = 3
    _damage = 10

class LargeRArm(cl.RArm):
    subelement_classes = [LargeRHand]
    base_hp = int(cl.RArm.base_hp * 2)
    strength = 2
    _armor = 3

class LargeLHand(cl.LHand):
    base_hp = int(cl.LHand.base_hp * 2)
    _armor = 3

class LargeLArm(cl.LArm):
    subelement_classes = [LargeLHand]
    base_hp = int(cl.LArm.base_hp * 2)
    strength = 2
    _armor = 3

class LargeFoot(cl.Foot):
    base_hp = int(cl.Foot.base_hp * 2)
    _armor = 3

class LargeLeg(cl.Leg):
    subelement_classes = [LargeFoot]
    base_hp = int(cl.Leg.base_hp * 2)
    _armor = 3

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, LargeRArm, LargeLArm, LargeLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 50
    size = 3
    _armor = 3

class Troll(cr.creature):
    classname = "troll"
    team = "goblinkin"
    namelist = nm.names["troll"]
    baseElem = Torso
    colors = ["green", "gray", "brown"]
    textures = ["stony"]
    suits = [wsu.troll_gear, asu.prisonersuit]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for limb in self.subelements[0].limb_check("name"):
            if limb.wears not in ["head", "body"]:
                parent_limb = self.get_parents(limb)[-2]
                class RegrowLimb(eff.RegrowLimb):
                    limb_parent = parent_limb

                limb.impact_effects.append(RegrowLimb)
                # print(limb.name)
