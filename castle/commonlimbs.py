"""The Book of Common Limbs."""
import engine.creature as cr

class Hair(cr.limb):
    name = "hair"
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

class Horn(cr.weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"

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

# class hornedhead(cr.limb):
#     name = "head"
#     subelement_classes = [ear, eye, horn, mouth, nose]
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "head"

class Head(cr.limb):
    name = "head"
    subelement_classes = [Ear, Eye, Mouth, Nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"

# Arms
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

class Hand(cr.weapon):
    name = "hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "hand"

class Arm(cr.limb):
    name = "arm"
    subelement_classes = [Hand]
    isSurface = True
    appendageRange = (2, 3)
    wears = "arm"

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

# TODO we should be using these common limbs for our creatures