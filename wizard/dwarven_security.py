import engine.creature as cr
import engine.effectsbook as eff
import engine.item as it

import assets.commonlimbs as cl
import assets.suits as asu

import wizard.effectsbook as weff


class Speaker(cl.MetalLimb):
    name = "speaker"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    passive_effects = [weff.SecurityAnnouncement]


class Spotlight(cl.MetalLimb):
    name = "spotlight"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    passive_effects = [weff.BrightLight]


class GrenadeDucts(cl.MetalLimb):
    name = "ceiling ducts"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    passive_effects = [weff.StunGrenades]


class DetentionCable(cl.MetalLimb):
    name = "autonomous cable"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    passive_effects = [weff.EntangleFeet]


class DetentionCableDeployer(cl.MetalLimb):
    name = "cable deployment system"
    subelement_classes = [DetentionCable]
    appendageRange = (1, 2)
    base_hp = 10
    size = 1


class GasVents(cl.MetalLimb):
    name = "thin floor vents"
    subelement_classes = []
    appendageRange = (1, 2)
    base_hp = 10
    size = 1
    passive_effects = [weff.GasAttack]


# Broken version of each security component
class BrokenSpeaker(Speaker):
    passive_effects = [weff.BrokenSecurityAnnouncement]

class BrokenSpotlight(Spotlight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrokenSecurityComponent(weff.BrokenSecurityComponent):
            delay = self.passive_effects[0].delay

        self.passive_effects = [BrokenSecurityComponent]


class BrokenGrenadeDucts(GrenadeDucts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrokenSecurityComponent(weff.BrokenSecurityComponent):
            delay = self.passive_effects[0].delay

        self.passive_effects = [BrokenSecurityComponent]


class BrokenDetentionCableDeployer(DetentionCableDeployer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrokenSecurityComponent(weff.BrokenSecurityComponent):
            delay = self.passive_effects[0].delay

        self.passive_effects = [BrokenSecurityComponent]


class BrokenGasVents(GasVents):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrokenSecurityComponent(weff.BrokenSecurityComponent):
            delay = self.passive_effects[0].delay

        self.passive_effects = [BrokenSecurityComponent]


class ControlBox(cl.MetalLimb):
    name = "control box"
    subelement_classes = [(Speaker, BrokenSpeaker), (Spotlight, BrokenSpotlight), (GrenadeDucts, BrokenGrenadeDucts), (DetentionCableDeployer, BrokenDetentionCableDeployer), (GasVents, BrokenGasVents)]
    appendageRange = (1, 2)
    base_hp = 15
    size = 2
    passive_effects = [weff.TurnOffAllSecurityEffects]


class DwarvenSecuritySystem(cr.Mechanoid):
    """Security system for the dwarven mountainhomes."""
    classname = "security system"
    team = "neutral"
    namelist = ["security system"]
    baseElem = ControlBox
    colors = ["silvery", "gray", "steely", "rusty", "matte"]
    textures = ["metallic"]
    suits = []
