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

class Hair(cr.Limb):
    name = "hair"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"
    size = 1
    colors = ["black", "red", "brown", "blonde"]
    textures = ["haired"]

# TODO beards should give mana
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

class WizardBeard(Beard):
    base_mana = 5
    mana = 5
    colors = ["white"]
    textures = ["luxuriant"]

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

class SmallFoot(Foot):
    base_hp = int(Foot.base_hp / 2)

class SmallLeg(Leg):
    subelement_classes = [SmallFoot]
    base_hp = int(Leg.base_hp / 2)

class SmallHead(Head):
    base_hp = int(Head.base_hp / 2)
