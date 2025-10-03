import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu

import monster.suits as msu


class FlameJaw2(cr.Weapon):
    name = "wyrm jaw"
    subelement_classes = [cl.Teeth, cl.Tongue]
    isSurface = True
    blockable = False
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 15
    size = 2
    _damage = 15
    eats = 1
    strength = 1
    weapon_effects = [eff.FireDOT2]

class VampiricJaw(cl.Jaw):
    subelement_classes = [cl.VampireFangs, cl.Tongue]

class PoisonJaw2(cl.Jaw):
    subelement_classes = [cl.PoisonFangs2, cl.Tongue]

class SlimeJaw(cl.Jaw):
    weapon_effects = [eff.Slime]
    passive_effects = [eff.DigestSlime]

class Head(cl.Head):
    # optional beard for humans
    subelement_classes = [(cl.Horn, None), cl.Ear, cl.Eye, cl.Nose, (SlimeJaw, PoisonJaw2, FlameJaw2, VampiricJaw, *[cl.Jaw] * 2), (cl.Beard, cl.PTentacle2, *[None] * 2)]

class ClubTail2(cr.Weapon):
    name = "spikeball tail"
    subelement_classes = []
    _damage = 25
    appendageRange = (1, 2)
    wears = "tail"
    base_hp = 20
    size = 3
    weapon_effects = [eff.Stun, eff.Bleed]

class KnifeFinger2(cr.Weapon):
    name = "dagger finger"
    subelement_classes = []
    f_grasp = 1 / 2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 7
    size = 1
    _damage = 12
    weapon_effects = [eff.Bleed]

class RHand(cr.Weapon):
    name = "right hand"
    subelement_classes = [KnifeFinger2, cl.Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"
    _damage = 3
    base_hp = 15
    size = 2

class LHand(cr.Weapon):
    name = "left hand"
    subelement_classes = [KnifeFinger2, cl.Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"
    _damage = 2
    base_hp = 15
    size = 2

class RArm(cl.RArm):
    subelement_classes = [RHand]
    _armor = 1.5

class LArm(cl.LArm):
    subelement_classes = [LHand]
    _armor = 1.5

class BloodSac(cr.Limb):
    name = "blood sac"
    subelement_classes = []
    isSurface = True
    appendageRange = (0, 4)
    base_hp = 20
    size = 5

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, (*[None] * 3, BloodSac), (*[cl.RArm] * 3, RArm), (*[cl.LArm] * 3, LArm), cl.Leg, (*[None] * 3, ClubTail2)]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 55
    size = 3

class MazeMonster(cr.creature):
    classname = "monster"
    team = "monster"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [(asu.prisonersuit, asu.partial_blood_armorsuit, asu.partial_flame_armorsuit, asu.partial_poison_armorsuit)]
