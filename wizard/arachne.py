"""Half spider, half human hybrid."""
import engine.creature as cr
import assets.commonlimbs as cl
import assets.namelists as nl

import assets.suits as asu
import wizard.suits as wsu


class PointyEar(cl.Ear):
    name = "pointy ear"
    size = 1

class Head(cr.Limb):
    name = "head"
    subelement_classes = [PointyEar, cl.Eye, cl.Nose, cl.Jaw]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"
    vital = True
    base_hp = 15
    size = 2

class Torso(cr.Limb):
    name = "torso"
    subelement_classes = [Head, cl.RArm, cl.LArm]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 35
    size = 3

class Leg(cr.Limb):
    name = "leg"
    subelement_classes = []
    isSurface = True
    appendageRange = (8, 9)
    wears = "spider_leg"
    base_hp = 10
    size = 2
    amble = 1/4

class SpiderTorso(cr.Limb):
    name = "body"
    subelement_classes = [Torso, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "spider_body"
    base_hp = 30
    size = 3

class Arachne(cr.creature):
    classname = "arachne"
    team = "dark elf"
    namelist = nl.names["spider"]
    baseElem = SpiderTorso
    colors = ["black", "brindled", "spotted", "brown", "rust"]
    textures = ["furred"]
    suits = [wsu.partial_spider_bronze_suit, asu.partial_bronze_armorsuit, wsu.double_iron_poisonsword]
