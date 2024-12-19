import engine.creature as cr

import assets.commonlimbs as cl
import assets.namelists as nl

from colorist import BrightColor as BC, Color as C


class Tentacle(cl.Tentacle):
    _damage = 10
    base_hp = 15

class Torso(cr.Limb):
    name = "trunk"
    subelement_classes = [Tentacle]
    amble = 1
    size = 2
    isSurface = True

class TentacleMonster(cr.creature):
    classname = "tentacle monster"
    namelist = nl.names["eldritch"]
    team = "monster"
    baseElem = Torso
    colors = ["black", "green", "gray"]
    textures = ["smooth", "slimy"]
    suits = []

    def leave(self, direction):
        """Tentacle monsters have amble (so they don't fall over) but they can't actually move."""
        print(f"{C.RED}{self.name} cannot move.{C.OFF}")
