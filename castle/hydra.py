"""The Hydra is a dangerous and terrifying creature with a varying number of heads.
Beware its flailing tail and sharp teeth!"""
import engine.creature as cr
import castle.commonlimbs as cl
from castle import suits


class snout(cr.limb):
    name = "snout"
    subelement_classes = [cl.tongue, cl.teeth]
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class head(cr.limb):
    name = "head"
    subelement_classes = [snout, cl.ear, cl.eye]
    isSurface = True
    appendageRange = (3, 6)
    wears = "head"


leg = cl.leg
leg.appendageRange = (4, 5)

class tail(cr.weapon):
    name = "tail"
    subelement_classes = []
    isSurface = True
    f_grasp = 1
    t_grasp = 1
    grasp = 1
    _damage = 7
    appendageRange = (1, 2)
    wears = "tail"

# Torso
class torso(cr.limb):
    name = "torso"
    subelement_classes = [head, leg, tail]
    appendageRange = (1, 2)
    wears = "body"

# Hydra
class hydra(cr.creature):
    name = "hydra"
    isSurface = True
    baseElem = torso
    colors = ["black", "gray", "red"]
    textures = ["scaled"]
    suits = [suits.testsuit]


if __name__ == "__main__":
    howie = hydra("Howie", location=None)
    print(howie.desc())
    # print(howie.subelements[0].inventory)
