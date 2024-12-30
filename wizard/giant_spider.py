"""A giant spider, roughly the size of a dog."""
import engine.creature as cr

import assets.commonlimbs as cl
import engine.effectsbook as eff
import assets.namelists as nl

import wizard.suits as wsu


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
    wears = "fangs"
    _damage = 10
    # weapon effects are applied when the weapon strikes
    weapon_effects = [eff.Webbed, eff.Poison]

class Jaw(cr.Limb):
    name = "jaw"
    subelement_classes = [Fangs]
    isSurface = True
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 5
    size = 1
    eats = 1
    strength = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [Eye, Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "spider_head"
    vital = True
    base_hp = 20
    size = 2

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (8, 9)
    wears = "spider_leg"
    base_hp = 10
    size = 2
    amble = 1/4

class Torso(cr.Limb):
    name = "body"
    subelement_classes = [Head, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "spider_body"
    base_hp = 30
    size = 3

class GiantSpider(cr.creature):
    classname = "giant spider"
    team = "dark elf"
    namelist = nl.names["spider"]
    baseElem = Torso
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["furred"]
    suits = []

class ArmoredGiantSpider(GiantSpider):
    classname = "armored spider"
    suits = [wsu.spider_bronze_suit]
