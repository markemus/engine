from engine import spells as sp

from colorist import BrightColor as BC, Color as C


class FireDOT(sp.Effect):
    desc = "burning"
    damage = 1
    rounds = 5

    def update(self):
        print(f"{C.RED}{self.creature}'s {self.limb.name} is burning!{C.OFF}")
        self.cont.combat.apply_damage(defender=self.creature, limb=self.limb, damage=self.damage)

    def _expire(self):
        print(f"{BC.RED}The fire on {C.RED}{self.limb.name}{BC.RED} goes out.{C.OFF}")


class Light(sp.Effect):
    """The limb is surrounded by a halo, making it easier to hit."""
    desc = "luminous"
    rounds = 10
    original_size = None

    def _cast(self):
        self.original_size = self.limb.size
        if self.limb.size < 3:
            self.limb.size += 1

    def _expire(self):
        self.limb.size = self.original_size


class Shadow(sp.Effect):
    """The limb is surrounded by a shadow, making it harder to hit."""
    desc = "shadowy"
    rounds = 10
    original_size = None

    def _cast(self):
        self.original_size = self.limb.size
        if self.limb.size > 1:
            self.limb.size -= 1

    def _expire(self):
        self.limb.size = self.original_size

# TODO bleed- builds up and if it hits a certain level, creature dies
# TODO poison- same as bleed
# TODO shatter- lowers armor
# TODO-DONE light, shadow effects
