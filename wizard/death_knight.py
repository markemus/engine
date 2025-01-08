import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nl
import assets.suits as asu


class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 7
    appendageRange = (1, 2)
    wears = "teeth"
    base_hp = 10
    size = 1
    colors = ["white"]
    textures = ["enameled"]
    _armor = 2

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Teeth]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 10
    size = 1
    eats = 1
    strength = 1.5
    _armor = 2

class Skull(cr.Limb):
    name = "skull"
    subelement_classes = [cl.Eye, Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 15
    size = 2
    _armor = 2

class SkeletalRHand(cl.RHand):
    name = "skeletal right hand"
    _armor = 2
    _damage = 5

class SkeletalRArm(cl.RArm):
    name = "humerus"
    subelement_classes = [SkeletalRHand]
    strength = 1.5
    _armor = 2

class SkeletalLHand(cl.LHand):
    name = "skeletal left hand"
    _armor = 2
    _damage = 5

class SkeletalLArm(cl.RArm):
    name = "humerus"
    subelement_classes = [SkeletalLHand]
    strength = 1.5
    _armor = 2

class SkeletalFoot(cl.Foot):
    name = "skeletal foot"
    _armor = 2

class Femur(cl.Leg):
    name = "femur"
    subelement_classes = [SkeletalFoot]
    _armor = 2

class Ribcage(cr.Limb):
    name = "ribcage"
    subelement_classes = [Skull, SkeletalRArm, SkeletalLArm, Femur]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 20
    size = 3
    _armor = 2

class DeathKnight(cr.creature):
    classname = "death knight"
    team = "necromancer"
    namelist = nl.names["human"]
    baseElem = Ribcage
    colors = ["white", "gray"]
    textures = ["bone"]
    suits = [asu.iron_armorsuit, asu.iron_weapons]
    can_stun = False
    can_rest = False
    can_breathe = False
    can_fear = False
    can_poison = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for limb in self.limb_check("name"):
            limb.can_heal = False
            limb.can_bleed = False
            limb.resurrected = True
