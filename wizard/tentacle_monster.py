import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nl

from colorist import BrightColor as BC, Color as C


class Tentacle(cl.Tentacle):
    _damage = 15
    strength = 2
    base_hp = 15

class Trunk(cr.Limb):
    name = "trunk"
    subelement_classes = [Tentacle]
    size = 2
    isSurface = True
    base_hp = 60

class TentacleMonster(cr.creature):
    """A giant tentacle monster. This creature cannot move but is extremely dangerous."""
    classname = "tentacle monster"
    namelist = nl.names["eldritch"]
    team = "squids"
    can_breathe = False
    can_stun = False
    baseElem = Trunk
    colors = ["black", "green", "gray"]
    textures = ["smooth", "slimy"]
    suits = []
