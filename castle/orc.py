"""Orcs are vile and nasty creatures, born to wreak havoc and destroy. They deserve nothing more
than a clean death."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


# Head
# class Ear(cr.Limb):
#     name = "ear"
#     subelement_classes = []
#     isSurface = 1
#     appendageRange = (2, 3)
#     wears = "ear"
#
# class Eye(cr.Limb):
#     name = "eye"
#     subelement_classes = []
#     isSurface = 1
#     appendageRange = (2, 3)
#     wears = "eye"
#
# class Horn(cr.Weapon):
#     name = "horn"
#     subelement_classes = []
#     _damage = 3
#     isSurface = True
#     appendageRange = (2, 3)
#     wears = "horn"
#
# class Teeth(cr.Weapon):
#     name = "teeth"
#     subelement_classes = []
#     _damage = 2
#     appendageRange = (1, 2)
#     wears = "teeth"
#
# class Tongue(cr.Limb):
#     name = "tongue"
#     subelement_classes = []
#     appendageRange = (1, 2)
#     wears = "tongue"
#
# class Nose(cr.Limb):
#     name = "nose"
#     subelement_classes = []
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "nose"

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Horn, cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 10

# Arms
# class Finger(cr.Limb):
#     name = "finger"
#     subelement_classes = []
#     f_grasp = 1/2
#     isSurface = True
#     appendageRange = (4, 5)
#     wears = "finger"
#
# class Thumb(cr.Limb):
#     name = "thumb"
#     subelement_classes = []
#     t_grasp = 1
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "finger"

# class Hand(cr.weapon):
#     name = "hand"
#     subelement_classes = [Finger, Thumb]
#     grasp = 1
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "hand"
#
# class Arm(cr.limb):
#     name = "arm"
#     subelement_classes = [Hand]
#     isSurface = True
#     appendageRange = (2, 3)
#     wears = "arm"

# Legs
# class Foot(cr.Limb):
#     name = "foot"
#     subelement_classes = []
#     amble = 1/2
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "foot"
#
# class Leg(cr.Limb):
#     name = "leg"
#     subelement_classes = [Foot]
#     isSurface = True
#     appendageRange = (2, 3)
#     wears = "leg"

# Torso
class Torso(cr.Limb):
    name = "body"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40

# Orc
class Orc(cr.creature):
    classname = "orc"
    team = "monster"
    namelist = nm.names["orc"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"]
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.plainsuit, suits.weapons]
