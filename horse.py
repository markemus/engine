import creature as cr 

class eye(cr.limb):
    name = "eye"
    subelement_classes = []
    appendageRange = (2,3)
    isSurface = True

class ear(cr.limb):
    name = "ear"
    subelement_classes = []
    appendageRange = (2,3)
    isSurface = True

class head(cr.limb):
    name = "head"
    subelement_classes = [eye, ear]
    appendageRange = (1,2)
    isSurface = True

class hoof(cr.limb):
    name = "hoof"
    subelement_classes = []
    appendageRange = (1,2)
    isSurface = True

class leg(cr.limb):
    name = "leg"
    subelement_classes = [hoof]
    appendageRange = (4,5)
    isSurface = True

class torso(cr.limb):
    name = "torso"
    subelement_classes = [leg, head]
    appendageRange = (1,2)
    isSurface = True

class horse(cr.creature):
    baseElem = torso
    colors = ["brown", "gray", "red", "black"]
    textures = ["dappled", "shaggy", "shorthaired"]

if __name__ == '__main__':
    h = horse("horsey")
    h.desc()