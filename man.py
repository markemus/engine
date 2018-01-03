import creature as cr
import commonlimbs as cl
import suits

class head(cr.limb):
    name = "head"
    subelement_classes = [cl.hair, cl.eye, cl.nose, cl.mouth]
    isSurface = True
    appendageRange = (1,2)
    wears = "head"

class torso(cr.limb):
    name = "torso"
    subelement_classes = [head, cl.arm, cl.leg]
    isSurface = True
    appendageRange = (1,2)
    wears = "body"




class man(cr.creature):
    name = "man"
    baseElem = torso
    colors = ["black", "white", "red", "yellow", "brown"]
    textures = ["skinned"]
    suits = [suits.testsuit, suits.weapons]

if __name__ == "__main__":
    eve = man("Eve", location=None)
    print(eve.desc())