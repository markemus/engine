"""A simple creature made of ethereal mist."""
import engine.creature as cr
from castle import suits

class Head(cr.limb):
    name = "head"
    subelement_classes = []
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

class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, Arm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class AnimatedArmor(cr.creature):
    classname = "armor"
    namelist = ["Animated Armor"]
    baseElem = Torso
    colors = ["ethereal"]
    textures = ["mist"]
    suits = [suits.testsuit, suits.weapons]
