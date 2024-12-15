import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class PointyEar(cl.Ear):
    name = "pointy ear"
class Head(cr.Limb):
    name = "head"
    subelement_classes = [PointyEar, cl.Eye, cl.Mouth, cl.Nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True

class PHead(Head):
    # Prisoners may have tentacles, but rarely.
    subelement_classes = Head.subelement_classes.copy() + [(cl.PTentacle, None, None)]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class PTorso(Torso):
    subelement_classes = [PHead, cl.PRArm, cl.PLArm, cl.PLeg]

class Elf(cr.creature):
    classname = "elf"
    team = "neutral"
    namelist = nm.names["elf"]
    baseElem = Torso
    colors = ["pale", "white", "black"]
    textures = ["skinned"]
    suits = [suits.plainsuit]

class PrisonerElf(Elf):
    team = "prisoner"
    baseElem = PTorso
    suits = [suits.prisonersuit]
