import engine.creature as cr
import engine.effectsbook as eff
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu

import wizard.effectsbook as weff


class Speaker(cr.Limb):
    name = "speaker"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    _armor = 2
    passive_effects = [weff.SecurityAnnouncement]

class Spotlight(cr.Limb):
    name = "spotlight"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    _armor = 2
    passive_effects = [weff.BrightLight]


class GrenadeDucts(cr.Limb):
    name = "ceiling ducts"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    _armor = 2
    passive_effects = [weff.StunGrenades]

class DetentionCable(cr.Limb):
    name = "autonomous cable"
    subelement_classes = []
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    _armor = 2

class DetentionCableDeployer(cr.Limb):
    name = "cable deployment system"
    subelement_classes = [DetentionCable]
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    _armor = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class EntangleFeet(weff.EntangleFeet):
            entangling_limb = self.subelements[0]

        self.passive_effects = [EntangleFeet]


class ControlBox(cr.Limb):
    name = "control box"
    subelement_classes = [Speaker, Spotlight, GrenadeDucts, DetentionCableDeployer]
    can_bleed = False
    can_heal = False
    resurrected = True
    appendageRange = (1, 2)
    base_hp = 15
    size = 2
    _armor = 2
    passive_effects = [weff.TurnOffAllSecurityEffects]


class DwarvenSecuritySystem(cr.creature):
    """Security system for the dwarven mountainhomes"""
    classname = "security system"
    team = "neutral"
    namelist = ["security system"]
    baseElem = ControlBox
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
    can_fear = False
    can_rest = False
    can_stun = False
    can_poison = False
    can_breathe = False
    # This creature cannot be enthralled or possessed
    strong_will = True
