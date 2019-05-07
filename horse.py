import engine.creature as cr
import suits

class eye(cr.limb):
    name = "eye"
    subelement_classes = []
    appendageRange = (2, 3)
    isSurface = True
    wears = "eye"

class ear(cr.limb):
    name = "ear"
    subelement_classes = []
    appendageRange = (2, 3)
    isSurface = True
    wears = "ear"

class head(cr.limb):
    name = "head"
    subelement_classes = [eye, ear]
    appendageRange = (1, 2)
    isSurface = True
    wears = "head"

class hoof(cr.limb):
    name = "hoof"
    subelement_classes = []
    appendageRange = (1, 2)
    isSurface = True
    wears = "hoof"

class leg(cr.limb):
    name = "leg"
    subelement_classes = [hoof]
    appendageRange = (4, 5)
    isSurface = True
    wears = "leg"

class torso(cr.limb):
    name = "torso"
    subelement_classes = [leg, head]
    appendageRange = (1, 2)
    isSurface = True
    wears = "body"

class horse(cr.creature):
    baseElem = torso
    colors = ["brown", "gray", "red", "black"]
    textures = ["dappled", "shaggy", "shorthaired"]
    suits = [suits.testsuit]


if __name__ == '__main__':
    h = horse("Nelly", location=None)
    print(h.desc())
