import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nm
import assets.suits as asu


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 10
    size = 2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 20
    size = 3

class Uruk(cr.creature):
    classname = "uruk"
    team = "goblinkin"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["black", "white", "gray"]
    textures = ["skinned"]
    suits = [asu.partial_iron_armorsuit, asu.iron_weapons]
