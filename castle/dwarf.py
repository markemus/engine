"""A bearded creature known for its craftsmanship."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, cl.Jaw, cl.Beard]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = "head"
    base_hp = 10
    size = 2


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.SmallRArm, cl.SmallLArm, cl.SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3

class PHead(Head):
    # Prisoners may have tentacles, but rarely.
    subelement_classes = Head.subelement_classes.copy() + [(cl.PTentacle, None, None)]
class PTorso(Torso):
    subelement_classes = [PHead, cl.PSmallRArm, cl.PSmallLArm, cl.PSmallLeg]

class Dwarf(cr.creature):
    classname = "dwarf"
    team = "neutral"
    namelist = nm.names["dwarf"]
    baseElem = Torso
    colors = ["brown", "pale", "ruddy"]
    textures = ["skinned"]
    suits = [suits.plainsuit]

class PrisonerDwarf(Dwarf):
    team = "prisoner"
    baseElem = PTorso
    suits = [suits.prisonersuit]
