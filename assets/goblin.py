"""Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns and small stature."""
import engine.creature as cr
import assets.commonlimbs as cl
import assets.namelists as nm

from assets import suits

# Head
class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 10
    size = 2

# Torso
class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.SmallRArm, cl.SmallLArm, cl.SmallLeg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 20
    size = 3

# Goblin
class Goblin(cr.creature):
    classname = "goblin"
    team = "goblinkin"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.plainsuit, suits.iron_weapons]

class ServantGoblin(Goblin):
    """A role for a goblin- a civilian servant."""
    # This creature will not fight back if attacked.
    aggressive = False
    team = "goblinkin"
    suits = [suits.plainsuit]

class ShallowGoblin(cr.creature):
    """A shallow goblin. These creature are eking out a meager existence near the surface and have only basic equipment."""
    classname = "shallow goblin"
    team = "goblinkin"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"]
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.prisonersuit, suits.copper_weapons]

class DeepGoblin(ShallowGoblin):
    """Deep goblins are living deep in caves in their natural environment and have scrounged equipment from the dwarves."""
    classname = "deep goblin"
    suits = [suits.partial_iron_armorsuit, suits.iron_weapons]
