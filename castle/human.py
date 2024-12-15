import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [cl.Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class PTorso(Torso):
    subelement_classes = [cl.PHead, cl.PRArm, cl.PLArm, cl.PLeg]


class Human(cr.creature):
    classname = "man"
    team = "neutral"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [suits.plainsuit]

class PlayerHuman(Human):
    """A non-transmogrified Human, but a prisoner."""
    team = "prisoner"
    suits = [suits.prisonersuit]

class PrisonerHuman(Human):
    team = "prisoner"
    baseElem = PTorso
    suits = [suits.prisonersuit]


class HumanKing(Human):
    classname = "king"
    team = "monster"
    suits = [suits.weapons, suits.testsuit]
# TODO special equipment for king
