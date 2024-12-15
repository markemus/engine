"""A bearded creature known for its craftsmanship."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Mouth, cl.Nose, cl.Beard]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    vital = True


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class PHead(Head):
    # Prisoners may have tentacles, but rarely.
    subelement_classes = Head.subelement_classes.copy() + [(cl.PTentacle, None, None)]
class PTorso(Torso):
    subelement_classes = [PHead, cl.PRArm, cl.PLArm, cl.PLeg]

# TODO add neutrals to combat (untargeted and don't fight)
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
