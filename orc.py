import creature as cr 
import suits
"""
Orcs are vile and nasty creatures, born to wreak havoc and destroy. They deserve nothing more
than a clean death.
"""

#head
class ear(cr.limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2,3)
    wears = "ear"

class eye(cr.limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2,3)
    wears = "eye"

class horn(cr.weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2,3)
    wears = "horn"

class teeth(cr.weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 2
    appendageRange = (1,2)
    wears = "teeth"

class tongue(cr.limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1,2)
    wears = "tongue"

class nose(cr.limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1,2)
    wears = "nose"

class head(cr.limb):
    name = "head"
    subelement_classes = [ear, eye, horn, teeth, tongue, nose]
    isSurface = True
    appendageRange = (1,2)
    wears = "head"

#arms
class finger(cr.limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4,5)
    wears = "finger"

class thumb(cr.limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1,2)
    wears = "finger"

class hand(cr.weapon):
    name = "hand"
    subelement_classes = [finger, thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1,2)
    wears = "hand"

class arm(cr.limb):
    name = "arm"
    subelement_classes = [hand]
    isSurface = True
    appendageRange = (2,3)
    wears = "arm"

#legs
class foot(cr.limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1,2)
    wears = "foot"

class leg(cr.limb):
    name = "leg"
    subelement_classes = [foot]
    isSurface = True
    appendageRange = (2,3)
    wears = "leg"

#torso
class torso(cr.limb):
    name = "body"
    subelement_classes = [head, arm, leg]
    isSurface = True
    appendageRange = (1,2)
    wears = "body"

#orc
class orc(cr.creature):
    name = "orc"
    baseElem = torso
    colors = ["red", "brown", "green", "black", "beige"]
    textures = ["scaled", "haired", "skinned"]
    suits = [suits.testsuit, suits.weapons]

if __name__ == '__main__':
    oscar = orc("Oscar", location=None)
    oscar.desc()