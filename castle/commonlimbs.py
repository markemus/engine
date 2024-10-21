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

class Hair(cr.limb):
    name = "hair"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"

class Beard(cr.limb):
    name = "beard"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"

class Ear(cr.limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"

class Eye(cr.limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "eye"
    see = 1

class Horn(cr.weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"
    blocker = True

class Teeth(cr.weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 2
    appendageRange = (1, 2)
    wears = "teeth"

class Tongue(cr.limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"

class Mouth(cr.limb):
    name = "mouth"
    subelement_classes = [Teeth, Tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"

class Nose(cr.limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class Head(cr.limb):
    name = "head"
    subelement_classes = [Ear, Eye, Mouth, Nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"

# Arms
# TODO-DECIDE how many fingers are really required to grasp?
class Finger(cr.limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"

class Thumb(cr.limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"

class RHand(cr.weapon):
    name = "right hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"

class LHand(cr.weapon):
    name = "left hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    blocker = True
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"

class RArm(cr.limb):
    name = "arm"
    subelement_classes = [RHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True

class LArm(cr.limb):
    name = "arm"
    subelement_classes = [LHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True

# Legs
class Foot(cr.limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"

class Leg(cr.limb):
    name = "leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"

# Tentacles
class Tentacle(cr.limb):
    name = "tentacle"
    subelement_classes = []
    isSurface = True
    appendageRange = (5, 6)
    grasp = 1
    f_grasp = 1
    t_grasp = 1
