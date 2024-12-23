from engine import spells as sp

from colorist import BrightColor as BC, Color as C


class Stoneskin(sp.Effect):
    rounds = 10
    set_color = False
    set_texture = False
    # original_color = None
    # original_texture = None

    def _cast(self):
        # TODO-DONE store original_color and original_texture on limbs
        #  so that they can always be referenced accurately with no danger of being overwritten.
        if not hasattr(self.limb, "orig_color"):
            self.limb.orig_color = self.limb.color
        if not hasattr(self.limb, "orig_texture"):
            self.limb.orig_texture = self.limb.texture
        self.limb.base_hp *= 3
        self.limb.hp *= 3

        self.limb.color = "gray"
        self.limb.texture = "stony"

    def _expire(self):
        # print(f"{BC.CYAN}{self.limb.name}'s skin returns to normal.{BC.OFF}")

        if self.limb.texture == "stony":
            self.limb.base_hp /= 3
            self.limb.hp /= 3
            self.limb.color = self.limb.orig_color
            self.limb.texture = self.limb.orig_texture


class FireDOT(sp.Effect):
    desc = "burning"
    damage = 1
    rounds = 5

    def update(self):
        print(f"{C.RED}{self.creature.name}'s {self.limb.name} is burning!{C.OFF}")
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

# TODO should not be usable as weapon or blocker
class Webbed(sp.Effect):
    """If this effect is on a limb, limb will return amble=0."""
    desc = "webbed"
    rounds = 5
    webbed = True

# TODO bleed- builds up and if it hits a certain level, creature dies
# TODO poison- same as bleed
# TODO shatter- lowers armor
# TODO webbed effect- can't amble or use as weapon
# TODO fear effect- on subelements[0], makes creature unable to attack
