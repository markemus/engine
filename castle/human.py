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


class Human(cr.creature):
    classname = "man"
    team = "prisoner"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "red", "yellow", "brown"]
    textures = ["skinned"]
    suits = [suits.prisonersuit]

class HumanKing(Human):
    classname = "king"
    team = "monster"
    suits = [suits.weapons, suits.testsuit]
# TODO special equipment for king
