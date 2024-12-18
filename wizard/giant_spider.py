"""A giant spider, roughly the size of a dog."""
import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nl


class Eye(cr.Limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    appendageRange = (8, 9)
    wears = "eye"
    see = 1
    base_hp = 3
    size = 1
    colors = ["oily", "pitch"]
    textures = ["black"]

class Fangs(cl.Teeth):
    name = "fangs"
    _damage = 10

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Fangs]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 3
    size = 1
    eats = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Eye, Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_head"
    vital = True
    base_hp = 10
    size = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (8, 9)
    wears = "animal_leg"
    base_hp = 40
    size = 3
    amble = 1/4

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 30
    size = 3

class GiantSpider(cr.creature):
    classname = "giant spider"
    team = "monster"
    namelist = nl.names["spider"]
    baseElem = Torso
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["furred"]
    suits = []
