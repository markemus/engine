from engine import spells as sp

from colorist import BrightColor as BC, Color as C


class Stoneskin(sp.Effect):
    rounds = 10

    def _cast(self):
        if not hasattr(self.limb, "orig_color"):
            self.limb.orig_color = self.limb.color
        if not hasattr(self.limb, "orig_texture"):
            self.limb.orig_texture = self.limb.texture
        self.limb.base_hp *= 3
        self.limb.hp *= 3
        self.limb.color = "gray"
        self.limb.texture = "stony"
        return True

    def _expire(self):
        if self.limb.texture == "stony":
            self.limb.base_hp /= 3
            self.limb.hp /= 3
            self.limb.color = self.limb.orig_color
            self.limb.texture = self.limb.orig_texture


class FireDOT(sp.Effect):
    desc = "burning"
    damage = 1
    rounds = 4

    def _cast(self):
        if not(hasattr(self.creature.location, "wet") or not self.creature.location.wet):
            return True

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
        if not hasattr(self.limb, "orig_size"):
            self.limb.orig_size = self.limb.size
        if self.limb.orig_size < 3:
            self.limb.size = self.limb.orig_size + 1
        return True

    def update(self):
        """This is needed in case another effect overrode this one but expired."""
        if self.limb.orig_size < 3:
            self.limb.size = self.limb.orig_size + 1

    def _expire(self):
        self.limb.size = self.limb.orig_size


class Shadow(sp.Effect):
    """The limb is surrounded by a shadow, making it harder to hit."""
    desc = "shadowy"
    rounds = 10
    original_size = None

    def _cast(self):
        if not hasattr(self.limb, "orig_size"):
            self.limb.orig_size = self.limb.size
        if self.limb.orig_size > 1:
            self.limb.size = self.limb.orig_size - 1
        return True

    def update(self):
        """This is needed in case another effect overrode this one but expired."""
        if self.limb.orig_size > 1:
            self.limb.size = self.limb.orig_size - 1

    def _expire(self):
        self.limb.size = self.limb.orig_size

# TODO-DONE should not be usable as weapon or blocker
class Webbed(sp.Effect):
    """If this effect is on a limb, that limb cannot be used as an attacker or a blocker."""
    desc = "webbed"
    rounds = 3

    def _cast(self):
        if not hasattr(self.limb, "orig_amble") and hasattr(self.limb, "amble"):
            self.limb.orig_amble = self.limb.amble
        if hasattr(self.limb, "amble"):
            self.limb.amble = 0
        self.limb.webbed = True
        print(f"{C.RED}{self.creature.name}'s {self.limb.name} is webbed!{C.OFF}")
        return True

    def update(self):
        if hasattr(self.limb, "amble"):
            self.limb.amble = 0
        self.limb.webbed = True

    def _expire(self):
        if hasattr(self.limb, "amble"):
            self.limb.amble = self.limb.orig_amble
        self.limb.webbed = False
        print(f"{BC.CYAN}{self.creature.name}'s {self.limb.name} is no longer webbed.{BC.OFF}")


class Fear(sp.Effect):
    """A creature with a fear tag on creature.subelements[0] cannot attack."""
    rounds = 5

    def _cast(self):
        if self.creature.can_fear:
            self.creature.subelements[0].fear = True
            print(f"{C.RED}{self.creature.name} cowers in fear!{C.OFF}")
            return True

    def update(self):
        self.creature.subelements[0].fear = True

    def _expire(self):
        del self.creature.subelements[0].fear
        print(f"{BC.CYAN}{self.creature.name} is no longer terrified.{C.OFF}")


class Might(sp.Effect):
    rounds = 10

    def _cast(self):
        if not hasattr(self.limb, "orig_strength") and hasattr(self.limb, "strength"):
            self.limb.orig_strength = self.limb.strength

        if hasattr(self.limb, "strength"):
            self.limb.strength = self.limb.orig_strength + .5
        else:
            self.limb.strength = 1.5
        print(f"{BC.CYAN}{self.creature.name}'s {self.limb.name} bulges and swells!{BC.OFF}")
        return True

    def update(self):
        if hasattr(self.limb, "orig_strength"):
            self.limb.strength = self.limb.orig_strength + .5
        else:
            self.limb.strength = 1.5

    def _expire(self):
        if hasattr(self.limb, "orig_strength"):
            self.limb.strength = self.limb.orig_strength
        else:
            del self.limb.strength
        print(f"{BC.CYAN}{self.creature.name}'s {self.limb.name} shrinks back down to its normal size.{BC.OFF}")


class Bleed(sp.Effect):
    expire_on_removal = True
    def __init__(self, creature, limb, controller, amount=2):
        super().__init__(creature, limb, controller)
        self.amount = amount
        # More bleeding lasts for longer
        self.rounds = amount

    def update(self):
        self.creature.bled += self.amount
        if self.amount <= 2:
            desc = "oozes"
        elif self.amount == 4:
            desc = "drips"
        elif self.amount >= 6:
            desc = "spurts"

        print(f"{C.RED}Blood {desc} from {self.creature.name}'s {self.limb.name}.{C.OFF}")
        if self.creature.bled > self.creature.blood / 2:
            print(f"{C.RED}{self.creature.name}{C.OFF} looks pale.")
        if self.creature.bled >= self.creature.blood:
            self.creature.die()

    def _expire(self):
        print(f"{BC.CYAN}The wound on {self.creature.name}'s {self.limb.name} stops bleeding.{BC.OFF}")


class Poison(sp.Effect):
    rounds = 1
    amount = 2
    expire_on_removal = True

    def _cast(self):
        self.creature.poisoned += self.amount
        print(f"{C.RED}{self.creature.name} absorbs {self.amount} points of poison!{C.OFF}")
        if self.creature.poisoned > self.creature.poison_resist / 2:
            print(f"{C.RED}{self.creature.name}{C.OFF} looks green.")
        if self.creature.poisoned >= self.creature.poison_resist:
            print(f"{C.RED}{self.creature.name} has taken a fatal dose of poison!{C.OFF}")
            self.creature.die()
        return True

class Vampirism(sp.Effect):
    """Suck the lifeforce out of a creature."""
    # You need to overwrite this attribute in your subclass
    vampire = None
    amount = 5
    rounds = 1
    expire_on_removal = True

    def _cast(self):
        self.creature.bled += self.amount
        print(f"{C.RED}{self.vampire.name} drinks {self.creature.name}'s blood!{C.OFF}")
        if self.creature.bled > self.creature.blood / 2:
            print(f"{C.RED}{self.creature.name}{C.OFF} looks pale.")
        if self.creature.bled >= self.creature.blood:
            self.creature.die()

        self.vampire.heal(self.amount)

class HealAllies(sp.Effect):
    """Heals allies for a small amount every turn. This is an aura that resides on a creature, such as a fairy."""
    amount = 2
    rounds = "forever"
    expire_on_removal = True

    def update(self):
        allies = [c for c in self.creature.location.creatures if c.team == self.creature.team]
        for ally in allies:
            ally.heal(self.amount)
