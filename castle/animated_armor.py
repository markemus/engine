"""A simple creature made of ethereal mist and armor plate."""
import engine.creature as cr
from castle import suits

class Gem(cr.Limb):
    name = "gem"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    vital = "gem"
    colors = ["red", "blue", "green", "gold", "orange"]
    textures = ["glowing"]
    base_hp = 5
    size = 1
    see = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Gem]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    base_hp = 30
    size = 2

# Arms
class Finger(cr.Limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"
    base_hp = 10
    size = 1

class Thumb(cr.Limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"
    base_hp = 10
    size = 1

class RHand(cr.Weapon):
    name = "right hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "right hand"
    blocker = True
    base_hp = 15
    size = 2

class RArm(cr.Limb):
    name = "arm"
    subelement_classes = [RHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True
    base_hp = 40
    size = 2

class LHand(cr.Weapon):
    name = "left hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "left hand"
    blocker = True
    base_hp = 15
    size = 2

class LArm(cr.Limb):
    name = "arm"
    subelement_classes = [LHand]
    isSurface = True
    appendageRange = (1, 2)
    wears = "arm"
    blocker = True
    base_hp = 40
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

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, RArm, LArm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 80
    size = 3

class AnimatedArmor(cr.creature):
    classname = "armor"
    team = "monster"
    namelist = ["Animated Armor"]
    baseElem = Torso
    colors = ["ethereal"]
    textures = ["mist"]
    suits = [suits.armorsuit, suits.weapons]
    can_fear = False
