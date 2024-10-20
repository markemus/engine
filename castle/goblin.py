"""Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.orc as orc
from castle import suits
import castle.namelists as nm


# Head
class Head(cr.limb):
    name = "head"
    subelement_classes = [orc.Ear, orc.Eye, orc.Teeth, orc.Tongue, orc.Nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"

# Torso
class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, cl.LArm, cl.RArm, orc.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

# Goblin
class Goblin(cr.creature):
    classname = "goblin"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.testsuit, suits.weapons]

class ServantGoblin(Goblin):
    """A role for a goblin- a civilian servant."""
    suits = [suits.plainsuit]
