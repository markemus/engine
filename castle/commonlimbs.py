"""The Book of Common Limbs."""
import engine.creature as cr
# import castle.suits

class hair(cr.limb):
    name = "hair"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "hair"

class ear(cr.limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"

class eye(cr.limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "eye"

class horn(cr.weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"

class teeth(cr.weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 2
    appendageRange = (1, 2)
    wears = "teeth"

class tongue(cr.limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"

class mouth(cr.limb):
    name = "mouth"
    subelement_classes = [teeth, tongue]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"

class nose(cr.limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class hornedhead(cr.limb):
    name = "head"
    subelement_classes = [ear, eye, horn, mouth, nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"

class hornlesshead(cr.limb):
    name = "head"
    subelement_classes = [ear, eye, mouth, nose]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"

# Arms
class finger(cr.limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"

class thumb(cr.limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"

class hand(cr.weapon):
    name = "hand"
    subelement_classes = [finger, thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "hand"

class arm(cr.limb):
    name = "arm"
    subelement_classes = [hand]
    isSurface = True
    appendageRange = (2, 3)
    wears = "arm"

# Legs
class foot(cr.limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"

class leg(cr.limb):
    name = "leg"
    subelement_classes = [foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"

# Torso
class torso(cr.limb):
    name = "body"
    subelement_classes = [hornlesshead, arm, leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"


# if __name__ == '__main__':
#     wep = suits.sword()
#     test = hand()
#     test.inventory.append(wep)
#     print(test.damage)
