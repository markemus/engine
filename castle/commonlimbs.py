"""The Book of Common Limbs. These limbs are used for the creatures stored in separate modules.
If a creature needs a specialized limb, I've generally just made a new class instead of subclassing.

# Example
class Tentacle(cr.limb):
    name = "tentacle"

    # Subelements that will be generated. Only add once, use their appendageRange to determine how many will spawn.
    subelement_classes = [Subtentacle]

    # Whether the limb can be seen or not
    isSurface = True

    # How many of the limb will spawn (a range)
    appendageRange = (3, 6)

    # Tags. These determine behavior. A limb or its subelements can contain a tag to allow the behavior
    # A tentacle is hand-like (and doesn't need fingers or thumbs)
    grasp = 1
    f_grasp = 1
    t_grasp = 1
"""
import engine.creature as cr

class Hair(cr.Limb):
    name = "hair"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"
    size = 1
    colors = ["black", "red", "brown", "blonde"]
    textures = ["haired"]

class Beard(cr.Limb):
    name = "beard"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"
    base_hp = 1
    size = 1
    colors = ["black", "red", "brown", "blonde"]
    textures = ["haired"]

class Ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"
    base_hp = 3
    size = 1

class Eye(cr.Limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
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
    _damage = 2
    appendageRange = (1, 2)
    wears = "teeth"
    base_hp = 3
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
    base_hp = 3
    size = 1
    eats = 1

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
    vital = True
    base_hp = 10
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

class LArm(cr.Limb):
    name = "arm"
    subelement_classes = [LHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True
    base_hp = 30
    size = 2

# Legs
class Foot(cr.Limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"
    base_hp = 15
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
    appendageRange = (5, 6)
    grasp = 1
    f_grasp = 1
    t_grasp = 1
    base_hp = 5
    size = 2

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

class SmallLeg(Leg):
    base_hp = int(Leg.base_hp / 2)

class SmallHead(Head):
    base_hp = int(Head.base_hp / 2)


# Prisoner limbs- transmogrified
class PRArm(RArm):
    """Prisoner's right arm- transmogrified."""
    appendageRange = (0, 4)
    colors = ["pale"]
    textures = ["skinned"]

class PSmallRArm(SmallRArm):
    appendageRange = (0, 4)
    colors = ["pale"]
    textures = ["skinned"]
class PLArm(LArm):
    """Prisoner's left arm- transmogrified"""
    appendageRange = (0, 4)
    colors = ["pale"]
    textures = ["skinned"]

class PSmallLArm(SmallLArm):
    appendageRange = (0, 4)
    colors = ["pale"]
    textures = ["skinned"]

class PLeg(Leg):
    """Prisoner's leg- transmogrified."""
    appendageRange = (0, 9)
    colors = ["pale"]
    textures = ["skinned"]

class PSmallLeg(SmallLeg):
    appendageRange = (0, 4)
    colors = ["pale"]
    textures = ["skinned"]

# TODO-DONE let limbs have their own (coordinated) colors? How? (because PTentacles come from the potion).
class PTentacle(Tentacle):
    """Prisoners only have a small number of tentacles- no big deal."""
    appendageRange = (1, 3)
    colors = ["green"]
    textures = ["slimy"]

class PHead(Head):
    # Prisoners may have tentacles, but rarely.
    subelement_classes = Head.subelement_classes.copy() + [(PTentacle, None, None)]

class PSmallHead(PHead):
    base_hp = int(PHead.base_hp / 2)
