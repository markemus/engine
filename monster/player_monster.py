import engine.creature as cr
import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu

class Head(cl.Head):
    # optional beard for humans
    subelement_classes = cl.Head.subelement_classes.copy() + [(cl.Beard, None)]

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3


class Human(cr.creature):
    classname = "man"
    team = "neutral"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "brown", "tan"]
    textures = ["skinned"]
    suits = [asu.plainsuit, asu.backpack]
