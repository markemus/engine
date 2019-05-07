"""Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns."""
import creature as cr
import orc as orc
import suits


# Head
class Head(cr.limb):
    name = "head"
    subelement_classes = [orc.ear, orc.eye, orc.teeth, orc.tongue, orc.nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"

# Torso
class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, orc.arm, orc.leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

# Goblin
class goblin(cr.creature):
    name = "goblin"
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.testsuit, suits.weapons]


if __name__ == '__main__':
    greedo = goblin("Greedo", location=None)
    print(greedo.desc())
