import engine.creature as cr
import engine.effectsbook as eff

import assets.commonlimbs as cl
import assets.namelists as nl

import wizard.fairy
import wizard.giant_spider
import wizard.owlbear
import wizard.suits as wsu
import wizard.tentacle_monster


class Torso(cr.Limb):
    name = "bloated torso"
    subelement_classes = [wizard.owlbear.Head, cl.Tentacle, wizard.fairy.FairyTorso, wizard.fairy.FairyTorso, wizard.fairy.FairyTorso]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"
    base_hp = 35
    size = 3
    impact_effects = [eff.ExplodeOnDeath]


class Thorax(wizard.giant_spider.Thorax):
    subelement_classes = wizard.giant_spider.Thorax.subelement_classes.copy()
    subelement_classes.remove(wizard.giant_spider.Head)
    subelement_classes.insert(0, Torso)


class Necromancer(cr.creature):
    classname = "necromancer"
    team = "necromancer"
    namelist = nl.names["elf"]
    baseElem = Thorax
    strong_will = True
    colors = ["black"]
    textures = ["skinned"]
    suits = [wsu.lightsuit]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
