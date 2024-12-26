import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class PointyEar(cl.Ear):
    name = "pointy ear"
    size = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [PointyEar, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 15
    size = 2

class PHead(Head):
    # Prisoners may have tentacles, but rarely.
    subelement_classes = Head.subelement_classes.copy() + [(cl.PTentacle, None, None)]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 35
    size = 3

class Elf(cr.creature):
    classname = "elf"
    team = "neutral"
    namelist = nm.names["elf"]
    baseElem = Torso
    colors = ["pale", "white"]
    textures = ["skinned"]
    suits = [suits.plainsuit]
