import engine.creature as cr

from autobattler import golem_limbs as gl

from colorist import BrightColor as BC, Color as C


class Eye(gl.GolemLimb):
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


class Horn(gl.GolemWeapon):
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


class Fang(gl.GolemWeapon):
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


class Jaw(gl.GolemLimb):
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


class Head(cr.Limb):
    name = "head"
    subelement_classes = [Eye]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 75
    size = 2
    can_parent = ["eye", "mouth", "horn"]


# Hands
class Finger(gl.GolemLimb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 25
    size = 1
    limb_type = "finger"


class Thumb(gl.GolemLimb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"
    base_hp = 25
    size = 1
    limb_type = "thumb"


class Hand(gl.GolemWeapon):
    name = "hand"
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


class Arm(gl.GolemLimb):
    name = "arm"
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


# Legs
class Foot(gl.GolemLimb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"
    base_hp = 50
    size = 2
    limb_type = "foot"


class Leg(gl.GolemLimb):
    name = "leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"
    base_hp = 120
    size = 3
    can_parent = ["foot"]
    limb_type = "leg"


# Small limbs
class SmallHand(Hand):
    base_hp = int(Hand.base_hp * 2/3)
    size = 1


class SmallArm(Arm):
    subelement_classes = []
    base_hp = int(Arm.base_hp * 2/3)
    size = 2


class SmallFoot(Foot):
    base_hp = int(Foot.base_hp * 2/3)
    size = 1


class SmallLeg(Leg):
    subelement_classes = [SmallFoot]
    base_hp = int(Leg.base_hp * 2/3)
    size = 2


class SmallHead(Head):
    base_hp = int(Head.base_hp * 2/3)
    size = 1


class LargeTorso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Arm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 100
    size = 3


class SmallTorso(cr.Limb):
    name = "torso"
    subelement_classes = [SmallHead, SmallArm, SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 66
    size = 2


class Golem(cr.creature):
    team = "golem"
    namelist = ["golem"]
    colors = ["red", "brown", "yellow", "black", "beige"]
    textures = ["clay"]
    usable = True
    consumable = True

    def use(self, char, controller):
        if char.golem:
            print(f"{C.RED}{char} already has a golem deployed!{C.OFF}")
            return False

        if char.grasp_check():
            self.name = input(f"{BC.GREEN}Name your golem:{BC.OFF} ")
            char.location.creatures.append(self)
            self.location = char.location
            char.companions.append(self)
            char.golem = self
            print(f"{BC.YELLOW}{char.name} deploys {self.name}!{BC.OFF}")
            return True


class LargeGolem(Golem):
    classname = "large golem"
    namelist = ["large golem"]
    baseElem = LargeTorso
    price = 50
    suits = []


class SmallGolem(Golem):
    classname = "small golem"
    namelist = ["small golem"]
    baseElem = SmallTorso
    price = 50
    suits = []
