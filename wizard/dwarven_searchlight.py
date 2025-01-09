import engine.creature as cr
import engine.effectsbook as eff
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu


class Searchlight(cr.Limb):
    name = "searchlight"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 15
    size = 2
    _armor = 2
    passive_effects = [eff.BrightLight]


class MetalFrame(cr.Limb):
    name = "frame"
    subelement_classes = [Searchlight, cl.MetalEye, cl.MetalTreads, cl.MetalTreads]
    isSurface = True
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 40
    size = 3
    _armor = 2

class DwarvenSearchlight(cr.creature):
    """A small mechanoid that can wield a weapon."""
    classname = "searchlight"
    team = "dwarven"
    namelist = ["searchlight"]
    baseElem = MetalFrame
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = [asu.iron_weapons]
    can_fear = False
    can_rest = False
    can_stun = False
    can_poison = False
    can_breathe = False
    # This creature cannot be enthralled or possessed
    strong_will = True
