"""Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns and small stature."""
import engine.creature as cr
import castle.commonlimbs as cl
import castle.household_items as hi
from castle import suits
import castle.namelists as nm


# Head
class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = "head"
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
    team = "monster"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.plainsuit, suits.weapons, hi.potions_suit]

class ServantGoblin(Goblin):
    """A role for a goblin- a civilian servant."""
    # This creature will fight if attacked but you can leave them alone too.
    aggressive = False
    team = "monster"
    suits = [suits.plainsuit]

class GoblinCook(Goblin):
    classname = "goblin chef"
    team = "monster"
    suits = [suits.chefsuit, suits.chefface, suits.cookery]
