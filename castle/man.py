import engine.creature as cr
import castle.commonlimbs as cl
import castle.namelists as nm
from castle import suits

# class Head(cr.limb):
#     name = "head"
#     subelement_classes = [cl.hair, cl.eye, cl.nose, cl.mouth]
#     isSurface = True
#     appendageRange = (1, 2)
#     wears = "head"

class Torso(cr.limb):
    name = "torso"
    subelement_classes = [cl.Head, cl.Arm, cl.Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"


class Man(cr.creature):
    # name = "man"
    namelist = nm.names["human"]
    baseElem = Torso
    colors = ["black", "white", "red", "yellow", "brown"]
    textures = ["skinned"]
    suits = [suits.testsuit, suits.weapons]


# if __name__ == "__main__":
    # eve = Man("Eve", location=None)
    # print(eve.desc())
