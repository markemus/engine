"""A small creature fond of relaxation."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [cl.SmallHead, cl.SmallRArm, cl.SmallLArm, cl.SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 20

class PTorso(Torso):
    subelement_classes = [cl.PSmallHead, cl.PSmallRArm, cl.PSmallLArm, cl.PSmallLeg]


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
