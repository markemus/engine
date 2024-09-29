"""The Hydra is a dangerous and terrifying creature with a varying number of heads.
Beware its flailing tail and sharp teeth!"""
import engine.creature as cr
import castle.commonlimbs as cl
from castle import suits


class Teeth(cl.Teeth):
    _damage = 10

class Snout(cr.limb):
    name = "snout"
    subelement_classes = [cl.Tongue, Teeth]
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class Head(cr.limb):
    name = "head"
    subelement_classes = [Snout, cl.Ear, cl.Eye]
    isSurface = True
    appendageRange = (3, 6)
    wears = "head"

class Leg(cl.Leg):
    appendageRange = (4, 5)

class Tail(cr.weapon):
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
class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, Leg, Tail]
    appendageRange = (1, 2)
    wears = "body"

# Hydra
class Hydra(cr.creature):
    name = "hydra"
    isSurface = True
    baseElem = Torso
    colors = ["black", "gray", "red"]
    textures = ["scaled"]
    suits = [suits.testsuit]


if __name__ == "__main__":
    howie = Hydra("Howie", location=None)
    print(howie.desc())
    # print(howie.subelements[0].inventory)
