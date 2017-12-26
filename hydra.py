import creature as cr 
import commonlimbs as cl
"""
The Hydra is a dangerous and terrifying creature with a varying number of heads.
Beware its flailing tail and sharp teeth!
"""

class snout(cr.limb):
    name = "snout"
    subelement_classes = [cl.tongue, cl.teeth]
    isSurface = True
    appendageRange = (1,2)

class head(cr.limb):
    name = "head"
    subelement_classes = [snout, cl.ear, cl.eye]
    isSurface = True
    appendageRange = (3,6)

leg = cl.leg
leg.appendageRange = (4,5)

class tail(cr.limb):
    name = "tail"
    subelement_classes = []
    isSurface = True
    f_grasp = 1
    t_grasp = 1
    grasp = 1
    damage = 7
    appendageRange = (1,2)

#torso
class torso(cr.limb):
    name = "torso"
    subelement_classes = [head, leg, tail]
    appendageRange = (1,2)

#hydra
class hydra(cr.creature):
    name = "hydra"
    isSurface = True
    baseElem = torso
    colors = ["black", "gray", "red"]
    textures = ["scaled"]

if __name__ == "__main__":
    howie = hydra("Howie")
    howie.desc()