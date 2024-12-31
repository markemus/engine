import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nl

from colorist import BrightColor as BC, Color as C


class Tentacle(cl.Tentacle):
    _damage = 20
    base_hp = 15

class Torso(cr.Limb):
    name = "trunk"
    subelement_classes = [Tentacle]
    size = 2
    isSurface = True
    base_hp = 60

class TentacleMonster(cr.creature):
    """A giant tentacle monster. This creature cannot move but is extremely dangerous."""
    classname = "tentacle monster"
    namelist = nl.names["eldritch"]
    team = "monster"
    can_breathe = False
    can_stun = False
    baseElem = Torso
    colors = ["black", "green", "gray"]
    textures = ["smooth", "slimy"]
    suits = []

    # def leave(self, direction):
    #     """Tentacle monsters have amble (so they don't fall over) but they can't actually move."""
    #     print(f"{C.RED}{self.name} cannot move.{C.OFF}")
