"""A small creature fond of relaxation."""
import engine.creature as cr
import assets.commonlimbs as cl
import assets.namelists as nm
from assets import suits


class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [cl.SmallHead, cl.SmallRArm, cl.SmallLArm, cl.SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 20
    size = 3


class Hobbit(cr.creature):
    classname = "hobbit"
    team = "neutral"
    namelist = nm.names["hobbit"]
    baseElem = Torso
    colors = ["white", "tan", "ruddy"]
    textures = ["skinned"]
    suits = [suits.plainsuit]
