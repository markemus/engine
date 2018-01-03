import creature as cr 
import orc as orc
import suits
"""
Goblins are the Orc's smaller cousin. They are no more worthy of kindness than their equally foul
kinsmen. They can be distinguished by their lack of horns.
"""

#head
class head(cr.limb):
    name = "head"
    subelement_classes = [orc.ear, orc.eye, orc.teeth, orc.teeth, orc.tongue, orc.nose]
    isSurface = True
    appendageRange = (1,2)
    wears = "head"

#torso
class torso(cr.limb):
    name = "torso"
    subelement_classes = [head, orc.arm, orc.leg]
    isSurface = True
    appendageRange = (1,2)
    wears = "body"

#goblin
class goblin(cr.creature):
    name = "goblin"
    baseElem = torso
    colors = ["red", "brown", "green", "black", "beige"] 
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.testsuit, suits.weapons]

if __name__ == '__main__':
    greedo = goblin("Greedo", location=None)
    greedo.desc()