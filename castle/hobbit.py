"""A small creature fond of relaxation."""
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


class Hobbit(cr.creature):
    classname = "hobbit"
    team = "neutral"
    namelist = nm.names["hobbit"]
    baseElem = Torso
    colors = ["white", "tan", "ruddy"]
    textures = ["skinned"]
    suits = [suits.plainsuit]

class PrisonerHobbit(Hobbit):
    team = "prisoner"
    baseElem = PTorso
    suits = [suits.prisonersuit]
