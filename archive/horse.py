import engine.creature as cr
import suits

class eye(cr.Limb):
    name = "eye"
    subelement_classes = []
    appendageRange = (2, 3)
    isSurface = True
    wears = "eye"

class ear(cr.Limb):
    name = "ear"
    subelement_classes = []
    appendageRange = (2, 3)
    isSurface = True
    wears = "ear"

class head(cr.Limb):
    name = "head"
    subelement_classes = [eye, ear]
    appendageRange = (1, 2)
    isSurface = True
    wears = "head"

class hoof(cr.Limb):
    name = "hoof"
    subelement_classes = []
    appendageRange = (1, 2)
    isSurface = True
    wears = "hoof"

class leg(cr.Limb):
    name = "leg"
    subelement_classes = [hoof]
    appendageRange = (4, 5)
    isSurface = True
    wears = "leg"

class torso(cr.Limb):
    name = "torso"
    subelement_classes = [leg, head]
    appendageRange = (1, 2)
    isSurface = True
    wears = "body"

class horse(cr.creature):
    baseElem = torso
    colors = ["brown", "gray", "red", "black"]
    textures = ["dappled", "shaggy", "shorthaired"]
    suits = [suits.armorsuit]


if __name__ == '__main__':
    h = horse("Nelly", location=None)
    print(h.desc())
