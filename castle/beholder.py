"""A floating eye with tentacles."""
from castle import commonlimbs as cl
from castle import namelists as nm
from engine import creature as cr


class Eye(cr.Limb):
    """Beholders only have one eye."""
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (1, 2)
    wears = "eye"
    base_hp = 3
    size = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [cl.Ear, Eye, cl.Jaw, cl.Tentacle]
    isSurface = True
    appendageRange = (1, 2)
    wear = "head"
    amble = 1 # beholders fly
    vital = "head"
    base_hp = 10
    size = 2

class Beholder(cr.creature):
    classname = "beholder"
    team = "monster"
    namelist = nm.names["beholder"]
    baseElem = Head
    colors = ["gray", "off-white"]
    textures = ["slimy", "sheeny"]
    suits = []
    can_fear = False
