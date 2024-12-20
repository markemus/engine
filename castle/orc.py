"""Orcs are vile and nasty creatures, born to wreak havoc and destroy. They deserve nothing more
than a clean death."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits


class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Horn, cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 15
    size = 2

# Torso
class Torso(cr.Limb):
    name = "body"
    subelement_classes = [Head, cl.RArm, cl.LArm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 40
    size = 3

# Orc
class Orc(cr.creature):
    classname = "orc"
    team = "monster"
    namelist = nm.names["orc"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"]
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.partial_armorsuit, suits.weapons]
