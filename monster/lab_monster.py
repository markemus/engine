import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm
from assets import suits


class FlameJaw(cr.Weapon):
    name = "draconid jaw"
    subelement_classes = [cl.Teeth, cl.Tongue]
    isSurface = True
    blockable = False
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 10
    size = 2
    _damage = 10
    eats = 1
    strength = 1
    weapon_effects = [eff.FireDOT]

class VampiricJaw(cl.Jaw):
    subelement_classes = [cl.VampireFangs, cl.Tongue]

class PoisonJaw(cl.Jaw):
    subelement_classes = [cl.PoisonFangs, cl.Tongue]

class Head(cl.Head):
    # optional beard for humans
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, (PoisonJaw, FlameJaw, VampiricJaw, cl.Jaw), (cl.Beard, cl.PTentacle, *[None] * 2)]

class ClubTail(cr.Weapon):
    name = "club tail"
    subelement_classes = []
    _damage = 12
    appendageRange = (1, 2)
    wears = "tail"
    base_hp = 10
    size = 3
    weapon_effects = [eff.Stun]

class KnifeFinger(cr.Weapon):
    name = "knife finger"
    subelement_classes = []
    f_grasp = 1 / 2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 5
    size = 1
    _damage = 7
    weapon_effects = [eff.Bleed]

class RHand(cr.Weapon):
    name = "right hand"
    subelement_classes = [KnifeFinger, cl.Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"
    _damage = 3
    base_hp = 10
    size = 2

class LHand(cr.Weapon):
    name = "left hand"
    subelement_classes = [KnifeFinger, cl.Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"
    _damage = 2
    base_hp = 10
    size = 2

class RArm(cl.RArm):
    subelement_classes = [RHand]

class LArm(cl.LArm):
    subelement_classes = [LHand]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, (*[cl.RArm] * 3, RArm), (*[cl.LArm] * 3, LArm), cl.Leg, (*[None] * 3, ClubTail)]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3

class LabMonster(cr.creature):
    classname = "monster"
    team = "monster"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [suits.prisonersuit]
