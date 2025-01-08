import engine.creature as cr
import engine.effectsbook as eff

from engine import ai


class Tendril(cr.Weapon):
    name = "tendril"
    appendageRange = (7, 14)
    subelement_classes = []
    size = 1
    isSurface = True
    can_bleed = False
    base_hp = 5
    _damage = 5
    weapon_effects = [eff.Poison, eff.Stun]


class JellySac(cr.Limb):
    name = "jelly sac"
    appendageRange = (1, 2)
    subelement_classes = [Tendril]
    size = 2
    isSurface = True
    can_bleed = False
    base_hp = 15
    flight = 1


class Jellyfish(cr.Fish):
    classname = "jellyfish"
    namelist = ["jellyfish"]
    team = "pest"
    can_breathe = False
    can_stun = False
    can_poison = False
    baseElem = JellySac
    colors = ["pink", "white", "blue", "cyan"]
    textures = ["clear", "translucent", "cloudy"]
    suits = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai = ai.PestAI(creature=self)
