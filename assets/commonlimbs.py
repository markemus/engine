"""The Book of Common Limbs. These limbs are used for the creatures stored in separate modules.
See human.py for a description of creature specifications.

# Example
class Tentacle(cr.Limb):
    name = "tentacle"

    # Subelements make up the lower parts of the limb tree that will be generated.
    # Only add once, use their appendageRange attribute to determine how many will spawn (eg for two arms- Arm.appendageRange = (2,3)).
    subelement_classes = [Subtentacle]

    # Whether the limb can be seen or not
    isSurface = True

    # How many of the limb will spawn (a range)
    appendageRange = (3, 6)

    # Tags. These determine behavior. A limb or its subelements can contain a tag to allow the behavior.
    # Generally they need to sum to 1 for the limb to execute an action.
    # A tentacle is hand-like (and doesn't need finger or thumb subelements to grasp)
    grasp = 1
    f_grasp = 1
    t_grasp = 1

    # Wears tells the generator what type of equipment the limb can wear.
    wears = "noodly"

    # How hard a limb is to hit in combat (1,2,3)
    size = 2

    # Colors, textures are used during element generation. If limb doesn't have these it will inherit from parent limb.
    colors = []
    textures = []
"""
import engine.creature as cr
import engine.effectsbook as eff


class Hair(cr.Limb):
    name = "hair"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "hair"
    size = 1
    colors = ["black", "red", "brown", "blonde"]
    textures = ["haired"]

class Beard(cr.Limb):
    name = "beard"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "hair"
    base_hp = 1
    size = 1
    colors = ["black", "red", "brown", "blonde"]
    textures = ["haired"]

class WizardBeard(Beard):
    base_mana = 5
    mana = 5
    colors = ["white"]
    textures = ["luxuriant"]

class Ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "ear"
    base_hp = 3
    size = 1

class Eye(cr.Limb):
    name = "eye"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "eye"
    see = 1
    base_hp = 3
    size = 1
    colors = ["blue", "hazel", "black", "brown", "green"]
    textures = ["colored"]

class Horn(cr.Weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"
    blocker = True
    base_hp = 5
    size = 1
    colors = ["black", "gray", "brown"]
    textures = ["smooth"]

class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 3
    appendageRange = (1, 2)
    wears = "teeth"
    base_hp = 5
    size = 1
    colors = ["white"]
    textures = ["enameled"]

class Tongue(cr.Limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"
    base_hp = 3
    size = 1
    colors = ["red"]
    textures = ["fleshy"]

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Teeth, Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 5
    size = 1
    eats = 1
    strength = 1

class Nose(cr.Limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"
    base_hp = 3
    size = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Ear, Eye, Nose, Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 15
    size = 2

# Arms
class Finger(cr.Limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 5
    size = 1

class Thumb(cr.Limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"
    base_hp = 5
    size = 1

class RHand(cr.Weapon):
    name = "right hand"
    subelement_classes = [Finger, Thumb]
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
    subelement_classes = [Finger, Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"
    _damage = 2
    base_hp = 10
    size = 2

class RArm(cr.Limb):
    name = "arm"
    subelement_classes = [RHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True
    base_hp = 30
    size = 2
    strength = 1

class LArm(cr.Limb):
    name = "arm"
    subelement_classes = [LHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True
    base_hp = 30
    size = 2
    strength = 1

# Legs
class Foot(cr.Limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"
    base_hp = 10
    size = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"
    base_hp = 40
    size = 3

# Tentacles
class Tentacle(cr.Weapon):
    name = "tentacle"
    subelement_classes = []
    isSurface = True
    blocker = True
    appendageRange = (8, 9)
    wears = "tentacle"
    grasp = 1
    f_grasp = 1
    t_grasp = 1
    base_hp = 5
    size = 2
    strength = 1
    _damage = 10
    weapon_effects = [eff.Entangled]
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     class Entangled(eff.Entangled):
    #         entangling_limb = self
    #     self.weapon_effects = [Entangled]


# Small limbs- for smaller creatures
class SmallRHand(RHand):
    base_hp = int(RHand.base_hp / 2)

class SmallRArm(RArm):
    subelement_classes = [SmallRHand]
    base_hp = int(RArm.base_hp / 2)

class SmallLHand(LHand):
    base_hp = int(LHand.base_hp / 2)

class SmallLArm(LArm):
    subelement_classes = [SmallLHand]
    base_hp = int(LArm.base_hp / 2)

class SmallFoot(Foot):
    base_hp = int(Foot.base_hp / 2)

class SmallLeg(Leg):
    subelement_classes = [SmallFoot]
    base_hp = int(Leg.base_hp / 2)

class SmallHead(Head):
    base_hp = int(Head.base_hp / 2)

# Tiny limbs- for tiny creatures
class TinyRHand(RHand):
    base_hp = int(RHand.base_hp / 3)
    size = 1

class TinyRArm(RArm):
    subelement_classes = [TinyRHand]
    base_hp = int(RArm.base_hp / 3)
    size = 1

class TinyLHand(LHand):
    base_hp = int(LHand.base_hp / 3)
    size = 1

class TinyLArm(LArm):
    subelement_classes = [TinyLHand]
    base_hp = int(LArm.base_hp / 3)
    size = 1

class TinyFoot(Foot):
    base_hp = int(Foot.base_hp / 3)
    size = 1

class TinyLeg(Leg):
    subelement_classes = [TinyFoot]
    base_hp = int(Leg.base_hp / 3)
    size = 1

class TinyHead(Head):
    base_hp = int(Head.base_hp / 3)
    size = 1

# Special limbs
# Tentacles created by a potion or spell
class PTentacle(Tentacle):
    """This creature only has a small number of tentacles- no big deal."""
    appendageRange = (1, 3)
    _damage = 5
    colors = ["green"]
    textures = ["slimy"]

# Vampire fangs
class VampireFangs(Teeth):
    name = "fangs"
    _damage = 10
    weapon_effects = [eff.Vampirism]

class SwordHand(cr.Weapon):
    """A powerful sword hand to replace your hand."""
    name = "sword hand"
    subelement_classes = []
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"
    _damage = 40
    base_hp = 30
    size = 2
    armor = 3


# Metal limbs
class MetalLimb(cr.Limb):
    _armor = 2
    can_bleed = False
    can_heal = False
    can_burn = False

class MetalWeapon(cr.Weapon):
    _armor = 2
    can_bleed = False
    can_heal = False
    can_burn = False

class MetalEar(MetalLimb):
    name = "ear"
    subelement_classes = []
    isSurface = True
    appendageRange = (2, 3)
    wears = "ear"
    base_hp = 3
    size = 1

class MetalEye(MetalLimb):
    name = "vision plate"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "eye"
    see = 1
    base_hp = 5
    size = 1
    colors = ["blue", "hazel", "black", "brown", "green"]
    textures = ["metallic"]

class MetalNose(MetalLimb):
    name = "nose"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "nose"
    base_hp = 3
    size = 1

class MetalHead(MetalLimb):
    name = "head"
    subelement_classes = [MetalEar, MetalEye, MetalNose]
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
    base_hp = 15
    size = 2
    _armor = 2

class MetalHand(MetalWeapon):
    name = "grasper"
    appendageRange = (1, 2)
    wears = "right hand"
    subelement_classes = []
    blocker = True
    base_hp = 10
    _damage = 9
    size = 2
    grasp = 1
    f_grasp = 1
    t_grasp = 1

class MetalArm(MetalLimb):
    name = "arm"
    appendageRange = (1, 2)
    wears = "arm"
    subelement_classes = [MetalHand]
    blocker = True
    base_hp = 30
    size = 2

class MetalTreads(MetalLimb):
    name = "treads"
    appendageRange = (1, 2)
    subelement_classes = []
    base_hp = 10
    size = 2
    amble = 1

class MetalFoot(MetalLimb):
    name = "foot"
    appendageRange = (1, 2)
    wears = "foot"
    subelement_classes = []
    base_hp = 10
    size = 2
    amble = 1 / 2

class MetalLeg(MetalLimb):
    name = "leg"
    appendageRange = (2, 3)
    wears = "leg"
    subelement_classes = [MetalFoot]
    base_hp = 30
    size = 2

class MetalSpiderLeg(MetalLimb):
    name = "leg"
    appendageRange = (8, 9)
    wears = "spider_leg"
    subelement_classes = []
    base_hp = 20
    size = 2
    amble = 1/4
