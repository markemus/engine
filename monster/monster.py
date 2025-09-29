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
    _damage = 5
    eats = 1
    strength = 1
    weapon_effects = [eff.FireDOT]

class VampiricJaw(cl.Jaw):
    subelement_classes = [cl.VampireFangs, cl.Tongue]

class Head(cl.Head):
    # optional beard for humans
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, (FlameJaw, VampiricJaw, *[cl.Jaw] * 3), (cl.Beard, cl.Tentacle, *[None] * 3)]

class ClubTail(cr.Weapon):
    name = "club tail"
    subelement_classes = []
    _damage = 10
    appendageRange = (1, 2)
    wears = "tail"
    base_hp = 10
    size = 3

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg, (*[None] * 3, ClubTail)]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3

class MonsterHuman(cr.creature):
    classname = "monster"
    team = "monster"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [suits.prisonersuit]
