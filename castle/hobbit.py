"""A small creature fond of relaxation."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Torso(cr.limb):
    name = "torso"
    subelement_classes = [cl.Head, cl.LArm, cl.RArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

class Hobbit(cr.creature):
    classname = "hobbit"
    team = "prisoner"
    namelist = nm.names["hobbit"]
    baseElem = Torso
    colors = ["white", "tan", "ruddy"]
    textures = ["skinned"]
    suits = [suits.testsuit, suits.weapons]
