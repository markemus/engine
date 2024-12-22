from engine import spells as sp
from engine import combat as co

from colorist import BrightColor as BC, Color as C


class FireDOT(sp.Effect):
    desc = "burning"
    damage = 1
    rounds = 5
    def __init__(self, creature, limb):
        super().__init__(creature=creature, limb=limb)
        self.cc = co.Combat(char=None, cont=None)
    # def cast(self):
    #     self.update()

    def update(self):
        print(f"{C.RED}{self.limb.name} is burning!{C.OFF}")
        self.cc.apply_damage(defender=self.creature, limb=self.limb, damage=self.damage)

    def _expire(self):
        print(f"{BC.RED}The fire on {C.RED}{self.limb.name}{BC.RED} goes out.{C.OFF}")

# TODO bleed- builds up and if it hits a certain level, creature dies
# TODO poison- same as bleed
# TODO shatter- lowers armor
# TODO light, shadow effects
