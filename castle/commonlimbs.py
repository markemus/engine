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

class Beard(cr.Limb):
    name = "beard"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"

class Ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"

class Eye(cr.Limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "eye"
    see = 1

class Horn(cr.Weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"
    blocker = True

class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 2
    appendageRange = (1, 2)
    wears = "teeth"

class Tongue(cr.Limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"

class Mouth(cr.Limb):
    name = "mouth"
    subelement_classes = [Teeth, Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"

class Nose(cr.Limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Ear, Eye, Mouth, Nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True

# Arms
# TODO-DECIDE how many fingers are really required to grasp?
class Finger(cr.Limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/2
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"

class Thumb(cr.Limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"

class RHand(cr.Weapon):
    name = "right hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"
    _damage = 3

class LHand(cr.Weapon):
    name = "left hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"
    _damage = 2

class RArm(cr.Limb):
    name = "arm"
    subelement_classes = [RHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True

class LArm(cr.Limb):
    name = "arm"
    subelement_classes = [LHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True

# Legs
class Foot(cr.Limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"

# Tentacles
class Tentacle(cr.Limb):
    name = "tentacle"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    grasp = 1
    f_grasp = 1
    t_grasp = 1
