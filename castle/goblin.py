"""Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns."""
import engine.creature as cr
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
    subelement_classes = [Head, orc.Arm, orc.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

# Goblin
class Goblin(cr.creature):
    name = "goblin"
    namelist = nm.names["goblin"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.testsuit, suits.weapons]


if __name__ == '__main__':
    greedo = Goblin("Greedo", location=None)
    print(greedo.desc())
