"""A simple creature made of ethereal mist and armor plate."""
import engine.creature as cr
from castle import suits

class Gem(cr.Limb):
    name = "gem"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    vital = True

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Gem]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"

# Arms
class Finger(cr.Limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
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

class Hand(cr.Weapon):
    name = "hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "hand"

class Arm(cr.Limb):
    name = "arm"
    subelement_classes = [Hand]
    isSurface = True
    appendageRange = (2, 3)
    wears = "arm"

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

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Arm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class AnimatedArmor(cr.creature):
    classname = "armor"
    team = "monster"
    namelist = ["Animated Armor"]
    baseElem = Torso
    colors = ["ethereal"]
    textures = ["mist"]
    suits = [suits.testsuit, suits.weapons]
