import engine.creature as cr
import engine.effectsbook as eff
import autobattler.effectsbook as aeff

from colorist import BrightColor as BC, Color as C
from engine import utils


# TODO-DONE sublimb_size param that limits the total size of limbs allowed to be attached.
# Base limbs
class GolemBaseLimb:
    """Should only be used in inheritance in combination with some Limb class."""
    limb_type = None
    can_parent = []
    consumable = True
    sublimb_size = 0

    def has_free_space(self, amount):
        """Checks whether limb has room for another subelement."""
        used_space = sum([x.size for x in self.subelements])
        if used_space + amount <= self.sublimb_size:
            return True

    def use(self, char, controller):
        if char.golem:
            parent_limbs = [x for x in char.golem.limb_check("can_parent") if self.limb_type in x.can_parent and x.has_free_space(self.size)]
            parent_limbs = utils.listtodict(parent_limbs, add_x=True)
            utils.dictprint(parent_limbs)
            i = input(f"{BC.GREEN}Select a parent limb to attach this limb to:{BC.OFF} ")
            if i in parent_limbs.keys() and i != "x":
                parent_limb = parent_limbs[i]
                parent_limb.subelements.append(self)
                self.creature = parent_limb.creature
                print(f"{BC.MAGENTA}{char.name} grafts the {self.name} onto {self.creature.name}'s {parent_limb.name}.{BC.OFF}")
                return True
        else:
            print(f"{C.RED}You must deploy a golem before you can graft limbs to it.{C.OFF}")


class GolemLimb(cr.Limb, GolemBaseLimb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GolemWeapon(cr.Weapon, GolemBaseLimb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Basic limbs
class Eye(GolemLimb):
    name = "eye"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "eye"
    see = 1
    base_hp = 15
    size = 1
    colors = ["blue", "hazel", "black", "brown", "green"]
    textures = ["colored"]
    limb_type = "eye"
    price = 5


class Horn(GolemWeapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"
    blocker = True
    base_hp = 25
    size = 1
    colors = ["black", "gray", "brown"]
    textures = ["smooth"]
    limb_type = "horn"
    price = 5


class Fang(GolemWeapon):
    name = "fang"
    subelement_classes = []
    _damage = 3
    appendageRange = (2, 3)
    wears = "fang"
    base_hp = 25
    size = 1
    colors = ["white"]
    textures = ["enameled"]
    limb_type = "tooth"
    price = 5


class Jaw(GolemLimb):
    name = "jaw"
    subelement_classes = [Fang]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 25
    size = 1
    eats = 1
    strength = 1
    can_parent = ["tooth", "tongue"]
    limb_type = "mouth"
    price = 5


class Head(GolemLimb):
    name = "large head"
    subelement_classes = [Eye]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 75
    size = 2
    can_parent = ["eye", "mouth", "horn"]
    sublimb_size = 10
    price = 5


# Hands
class Finger(GolemLimb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 25
    size = 1
    limb_type = "finger"
    sublimb_size = 0


class Thumb(GolemLimb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"
    base_hp = 25
    size = 1
    limb_type = "thumb"
    sublimb_size = 0


class Hand(GolemWeapon):
    name = "large hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "hand"
    _damage = 3
    base_hp = 50
    size = 2
    can_parent = ["finger", "thumb"]
    limb_type = "hand"
    sublimb_size = 5
    price = 5


class Arm(GolemLimb):
    name = "large arm"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "arm"
    blocker = True
    base_hp = 150
    size = 3
    strength = 1
    can_parent = ["hand"]
    limb_type = "arm"
    sublimb_size = 2
    price = 5


# Legs
class Foot(GolemLimb):
    name = "large foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"
    base_hp = 50
    size = 2
    limb_type = "foot"
    sublimb_size = 0
    price = 5


class Leg(GolemLimb):
    name = "large leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"
    base_hp = 120
    size = 3
    can_parent = ["foot"]
    limb_type = "leg"
    price = 5


# Small limbs
class SmallHand(Hand):
    name = "small hand"
    base_hp = int(Hand.base_hp * 2/3)
    size = 1


class SmallArm(Arm):
    name = "small arm"
    subelement_classes = []
    base_hp = int(Arm.base_hp * 2/3)
    size = 2
    strength = 1


class SmallFoot(Foot):
    name = "small foot"
    base_hp = int(Foot.base_hp * 2/3)
    size = 1


class SmallLeg(Leg):
    name = "small leg"
    subelement_classes = [SmallFoot]
    base_hp = int(Leg.base_hp * 2/3)
    size = 2


class SmallHead(Head):
    name = "small head"
    base_hp = int(Head.base_hp * 2/3)
    size = 1


class LargeTorso(GolemLimb):
    name = "large torso"
    subelement_classes = [Head, Arm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 100
    size = 3
    can_parent = ["head", "arm", "leg", "module"]
    sublimb_size = 23


class SmallTorso(GolemLimb):
    name = "small torso"
    subelement_classes = [SmallHead, SmallArm, SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 66
    size = 2
    can_parent = ["head", "arm", "leg", "module"]
    sublimb_size = 15


# Basic weapons
class Buzzsaw(GolemWeapon):
    name = "buzzsaw"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 30
    weapon_effects = [aeff.RipLimb]
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Hammer(GolemWeapon):
    name = "hammer"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 20
    weapon_effects = [aeff.ShatterArmor, eff.Stun]
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Flamethrower(GolemWeapon):
    name = "flamethrower"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 5
    weapon_effects = [aeff.FireDOT5]
    price = 5
    colors = ["red", "brown", "yellow", "black"]
    textures = ["tubular"]


class Taser(GolemWeapon):
    name = "taser"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 2
    weapon_effects = [aeff.Lightning]
    price = 5
    colors = ["gray", "silver"]
    textures = ["metal"]


class Slimer(GolemWeapon):
    name = "slimer"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 20
    weapon_effects = [aeff.Slime]
    price = 5
    colors = ["green"]
    textures = ["slimy"]


class Shield(GolemLimb):
    name = "shield"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 100
    blocker = True
    _armor = 4
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Digester(GolemLimb):
    name = "digester"
    subelement_classes = []
    limb_type = "module"
    base_hp = 20
    price = 25
    size = 2
    colors = ["red"]
    textures = ["fleshy"]
    passive_effects = [aeff.DigestSlime]


basic_weapons = [Buzzsaw, Hammer, Flamethrower, Taser, Slimer]
basic_defense = [Shield]
basic_large_limbs = [Arm, Hand, Leg, Foot, Head]
basic_small_limbs = [SmallArm, SmallHand, SmallLeg, SmallFoot, SmallHead]
modules = [Digester]