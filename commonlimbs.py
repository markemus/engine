import creature as cr

class ear(cr.limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2,3)

class eye(cr.limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2,3)

class horn(cr.limb):
    name = "horn"
    subelement_classes = []
    damage = 3
    isSurface = True
    appendageRange = (2,3)

class teeth(cr.limb):
    name = "teeth"
    subelement_classes = []
    damage = 2
    appendageRange = (1,2)

class tongue(cr.limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1,2)

class nose(cr.limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1,2)

class hornedhead(cr.limb):
    name = "head"
    subelement_classes = [ear, eye, horn, teeth, tongue, nose]
    isSurface = True
    appendageRange = (1,2)

class hornlesshead(cr.limb):
    name = "head"
    subelement_classes = [ear, eye, teeth, tongue, nose]
    isSurface = True
    appendageRange = (1,2)

#arms
class finger(cr.limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4,5)

class thumb(cr.limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1,2)

class hand(cr.limb):
    name = "hand"
    subelement_classes = [finger, thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1,2)

class arm(cr.limb):
    name = "arm"
    subelement_classes = [hand]
    isSurface = True
    appendageRange = (2,3)

#legs
class foot(cr.limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1,2)

class leg(cr.limb):
    name = "leg"
    subelement_classes = [foot]
    isSurface = True
    appendageRange = (2,3)

#torso
class torso(cr.limb):
    name = "body"
    subelement_classes = [hornlesshead, arm, leg]
    isSurface = True
    appendageRange = (1,2)