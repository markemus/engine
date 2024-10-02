import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Head(cr.limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Mouth, cl.Nose, cl.Beard]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"


class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, cl.Arm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class Dwarf(cr.creature):
    classname = "dwarf"
    namelist = nm.names["dwarf"]
    baseElem = Torso
    colors = ["brown", "pale", "ruddy"]
    textures = ["skinned"]
    suits = [suits.testsuit, suits.weapons]
