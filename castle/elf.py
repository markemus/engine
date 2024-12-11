import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class PointyEar(cl.Ear):
    name = "pointy ear"
class Head(cr.limb):
    name = "head"
    subelement_classes = [PointyEar, cl.Eye, cl.Mouth, cl.Nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True

class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class Elf(cr.creature):
    classname = "elf"
    team = "prisoner"
    namelist = nm.names["elf"]
    baseElem = Torso
    colors = ["pale", "white", "black"]
    textures = ["skinned"]
    suits = [suits.testsuit, suits.weapons, suits.jewelry]
