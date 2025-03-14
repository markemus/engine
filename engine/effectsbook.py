import random

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
    damage = .5
    rounds = 8

    def _cast(self):
        if ((not hasattr(self.limb.creature.location, "wet")) or (not self.limb.creature.location.wet)) and self.limb.can_burn:
            return True

    def update(self):
        print(f"{C.RED}{self.limb.creature.name}'s {self.limb.name} is burning!{C.OFF}")
        self.cont.combat.apply_damage(defender=self.limb.creature, limb=self.limb, damage=self.damage)

    def _expire(self):
        print(f"{BC.RED}The fire on {C.RED}{self.limb.name}{BC.RED} goes out.{C.OFF}")


class Light(sp.Effect):
    """The limb is surrounded by a halo, making it easier to hit."""
    desc = "luminous"
    rounds = 10
    original_size = None
    allow_duplicates = False

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


class SquirtInk(sp.Effect):
    rounds = 1
    def _cast(self):
        class Ink(Shadow):
            desc = "inky"

        for limb in self.limb.creature.subelements[0].limb_check("isSurface"):
            ink = Ink(casting_limb=None, limb=limb, controller=self.cont)
            ink.cast()
        print(f"{C.RED}{self.limb.creature.name} squirts out a cloud of ink!{C.OFF}")


class Webbed(sp.Effect):
    """If this effect is on a limb, that limb cannot be used as an attacker or a blocker."""
    desc = "webbed"
    rounds = 5

    def _cast(self):
        if not hasattr(self.limb, "orig_amble") and hasattr(self.limb, "amble"):
            self.limb.orig_amble = self.limb.amble
        if hasattr(self.limb, "amble"):
            self.limb.amble = 0
        self.limb.webbed = True
        print(f"{C.RED}{self.limb.creature.name}'s {self.limb.name} is webbed!{C.OFF}")
        return True

    def update(self):
        if hasattr(self.limb, "amble"):
            self.limb.amble = 0
        self.limb.webbed = True

    def _expire(self):
        if hasattr(self.limb, "amble"):
            self.limb.amble = self.limb.orig_amble
        self.limb.webbed = False
        print(f"{BC.CYAN}{self.limb.creature.name}'s {self.limb.name} is no longer webbed.{BC.OFF}")


class Fear(sp.Effect):
    """A creature with a fear tag on creature.subelements[0] cannot attack."""
    rounds = 5

    def _cast(self):
        if self.limb.creature.can_fear:
            self.limb.creature.afraid = True
            print(f"{C.RED}{self.limb.creature.name} cowers in fear!{C.OFF}")
            return True

    def update(self):
        self.limb.creature.afraid = True

    def _expire(self):
        self.limb.creature.afraid = False
        print(f"{BC.CYAN}{self.limb.creature.name} is no longer terrified.{C.OFF}")


class Might(sp.Effect):
    rounds = 10
    desc = "bulging"

    def _cast(self):
        if not hasattr(self.limb, "orig_strength") and hasattr(self.limb, "strength"):
            self.limb.orig_strength = self.limb.strength

        if hasattr(self.limb, "strength"):
            self.limb.strength = self.limb.orig_strength + .5
        else:
            self.limb.strength = 1.5
        print(f"{BC.CYAN}{self.limb.creature.name}'s {self.limb.name} bulges and swells!{BC.OFF}")
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
        print(f"{BC.CYAN}{self.limb.creature.name}'s {self.limb.name} shrinks back down to its normal size.{BC.OFF}")


class Mastery(sp.Effect):
    """Increases a creature's to-hit chance."""
    rounds = 15

    def _cast(self):
        if not hasattr(self.limb.creature, "orig_mastery") and hasattr(self.limb.creature, "mastery"):
            self.limb.creature.orig_mastery = self.limb.creature.mastery

        if hasattr(self.limb.creature, "mastery"):
            self.limb.creature.mastery = self.limb.creature.orig_mastery + 2
        else:
            self.limb.creature.mastery = 2
        print(f"{BC.CYAN}A thrumming energy fills {self.limb.creature.name}'s body.{BC.OFF}")
        return True

    def update(self):
        if hasattr(self.limb.creature, "orig_mastery"):
            self.limb.creature.mastery = self.limb.creature.orig_mastery + 2
        else:
            self.limb.creature.mastery = 2

    def _expire(self):
        if hasattr(self.limb.creature, "orig_mastery"):
            self.limb.creature.mastery = self.limb.creature.orig_mastery
        else:
            del self.limb.creature.mastery
        print(f"{BC.CYAN}{self.limb.creature.name}'s body stops thrumming.{BC.OFF}")


class Bleed(sp.Effect):
    expire_on_removal = True
    cast_on_removal = False
    desc = "bleeding"

    def __init__(self, casting_limb, limb, controller, amount=2):
        super().__init__(casting_limb, limb, controller)
        self.amount = amount
        # More bleeding lasts for longer
        self.rounds = amount

    def _cast(self):
        if self.limb.can_bleed:
            return True

    def update(self):
        self.limb.creature.bled += self.amount
        if self.amount <= 2:
            desc = "oozes"
        elif self.amount == 4:
            desc = "drips"
        elif self.amount >= 6:
            desc = "spurts"

        print(f"{C.RED}Blood {desc} from {self.limb.creature.name}'s {self.limb.name}.{C.OFF}")
        if self.limb.creature.bled > self.limb.creature.blood / 2:
            print(f"{C.RED}{self.limb.creature.name}{C.OFF} looks pale.")
        if self.limb.creature.bled >= self.limb.creature.blood:
            self.limb.creature.die()

    def _expire(self):
        print(f"{BC.CYAN}The wound on {self.limb.creature.name}'s {self.limb.name} stops bleeding.{BC.OFF}")


class Poison(sp.Effect):
    rounds = 1
    amount = 2
    expire_on_removal = True
    cast_on_removal = False

    def _cast(self):
        if self.limb.creature.can_poison:
            self.limb.creature.poisoned += self.amount
            print(f"{C.RED}{self.limb.creature.name} absorbs {self.amount} points of poison!{C.OFF}")
            if self.limb.creature.poisoned > self.limb.creature.poison_resist / 2:
                print(f"{C.RED}{self.limb.creature.name}{C.OFF} looks green.")
            if self.limb.creature.poisoned >= self.limb.creature.poison_resist:
                print(f"{C.RED}{self.limb.creature.name} has taken a fatal dose of poison!{C.OFF}")
                self.limb.creature.die()


class Stun(sp.Effect):
    rounds = 5
    expire_on_removal = True
    allow_duplicates = False

    def _cast(self):
        if self.limb.creature.can_stun:
            head_wears = ["head", "animal_head", "spider_head"]
            if self.limb.wears in head_wears:
                other_heads = [x for x in self.limb.creature.subelements[0].limb_check("wears") if x is not self.limb and x.wears in head_wears]
                if not other_heads:
                    self.limb.creature.stunned = True
                    print(f"{C.RED}{self.limb.creature.name} is stunned!{C.OFF}")
                    return True

    def update(self):
        self.limb.creature.stunned = True

    def _expire(self):
        self.limb.creature.stunned = False
        print(f"{C.RED}{self.limb.creature.name} is no longer stunned.{C.OFF}")


class StunForSure(sp.Effect):
    """Cast this effect on creature.subelements[0]."""
    rounds = 5
    expire_on_removal = True
    allow_duplicates = False

    def _cast(self):
        if self.limb.creature.can_stun:
            self.limb.creature.stunned = True
            print(f"{C.RED}{self.limb.creature.name} is stunned!{C.OFF}")
            return True

    def update(self):
        self.limb.creature.stunned = True

    def _expire(self):
        self.limb.creature.stunned = False
        print(f"{C.RED}{self.limb.creature.name} is no longer stunned.{C.OFF}")


class Vampirism(sp.Effect):
    """Suck the lifeforce out of a creature."""
    amount = 5
    rounds = 1
    expire_on_removal = True
    cast_on_removal = False

    def _cast(self):
        if self.limb.can_bleed:
            self.limb.creature.bled += self.amount
            print(f"{C.RED}{self.casting_limb.creature.name} drinks {self.limb.creature.name}'s blood!{C.OFF}")
            if self.limb.creature.bled > self.limb.creature.blood / 2:
                print(f"{C.RED}{self.limb.creature.name}{C.OFF} looks pale.")
            if self.limb.creature.bled >= self.limb.creature.blood:
                self.limb.creature.die()

            self.casting_limb.creature.heal(self.amount)
        else:
            print(f"{C.RED}{self.limb.creature.name}'s {self.limb.name} has no blood to drink!{C.OFF}")


class MinorVampirism(Vampirism):
    amount = 2


class SuckBlood(sp.Effect):
    amount = 5
    rounds = 1
    cast_on_removal = False

    def _cast(self):
        if self.limb.can_bleed:
            self.limb.creature.bled += self.amount
            print(f"{C.RED}{self.casting_limb.creature} drinks {self.limb.creature.name}'s blood!{C.OFF}")
            if self.limb.creature.bled > self.limb.creature.blood / 2:
                print(f"{C.RED}{self.limb.creature.name}{C.OFF} looks pale.")
            if self.limb.creature.bled >= self.limb.creature.blood:
                self.limb.creature.die()
        else:
            print(f"{C.RED}{self.limb.creature.name}'s {self.limb.name} has no blood to suck.{C.OFF}")


class HealAllies(sp.Effect):
    """Heals allies for a small amount every turn. This is an aura that resides on a creature, such as a fairy."""
    desc = "glowing"
    amount = 2
    rounds = "forever"
    expire_on_removal = True

    def update(self):
        allies = [c for c in self.limb.creature.location.creatures if c.team == self.limb.creature.team]
        for ally in allies:
            ally.heal(self.amount)
            if ally.bled:
                ally.heal_blood(1)
            if ally.poisoned:
                ally.heal_poison(1)


class Entangled(sp.Effect):
    desc = "entangled"
    rounds = 4
    expire_on_removal = True
    allow_duplicates = False
    cast_on_removal = False

    def cast(self):
        """We need custom cast() and expire() since this effect affects two limbs."""
        if not self.allow_duplicates:
            if sum([isinstance(x, self.__class__) and (x.casting_limb is self.casting_limb) for x in self.limb.active_effects]):
                return False

        if not self.cast_on_removal:
            if self.limb not in self.limb.creature.limb_check("name"):
                return False

        print(f"{C.RED}{self.casting_limb.name} and {self.limb.name} are entangled!{C.OFF}")

        self.update()

        self.limb.active_effects.append(self)
        self.casting_limb.active_effects.append(self)
        self.cont.game.active_spells.append(self)
        return True

    def update(self):
        """Entangled limbs cannot walk or fly."""
        for l in [self.casting_limb, self.limb]:
            if hasattr(l, "amble"):
                if not hasattr(l, "orig_amble"):
                    l.orig_amble = l.amble
                l.amble = 0
            if hasattr(l, "flight"):
                if not hasattr(l, "orig_flight"):
                    l.orig_flight = l.flight
                l.flight = 0

    def expire(self):
        print(f"{C.RED}{self.casting_limb.creature.name}'s {self.casting_limb.name} and {self.limb.creature.name}'s {self.limb.name} separate.{C.OFF}")

        for l in [self.casting_limb, self.limb]:
            if hasattr(l, "amble"):
                l.amble = l.orig_amble
            if hasattr(l, "flight"):
                l.flight = l.orig_flight

        self.limb.active_effects.remove(self)
        self.casting_limb.active_effects.remove(self)
        self.cont.game.active_spells.remove(self)
        self.expired = True


class DrawAggro(sp.Effect):
    """This creature will draw the aggression of any creature it attacks."""
    rounds = 1

    def _cast(self):
        old_target = self.limb.creature.ai.target
        if old_target is not self.casting_limb.creature and not self.limb.creature.dead:
            self.limb.creature.ai.target = self.casting_limb.creature
            print(f"{C.RED}{self.limb.creature.name} turns on {self.casting_limb.creature.name}!{C.OFF}")


class RegrowLimb(sp.Effect):
    rounds = 5
    # Subclass and set limb_parent as parent limb
    limb_parent = None

    def _cast(self):
        """Will apply if limb has been removed from creature."""
        limbs = self.limb.creature.subelements[0].limb_check("name")
        if self.limb not in limbs:
            # fire stops regeneration
            if not sum([isinstance(e, FireDOT) for e in self.limb.active_effects]):
                return True

    def _expire(self):
        if not self.limb.creature.dead:
            self.limb_parent.subelements.append(self.limb.__class__(self.limb.color, self.limb.texture, self.limb.creature))
            print(f"{BC.CYAN}A new {self.limb.name} sprouts from {self.limb.creature.name}'s {self.limb_parent.name}!{BC.OFF}")


class ExplodeOnDeath(sp.Effect):
    rounds = 3
    expire_on_removal = False
    cast_on_removal = True

    def _cast(self):
        if self.casting_limb.creature.dead:
            return True

    def update(self):
        print(f"{C.RED}{self.casting_limb.creature.name}'s corpse bloats and distends.{C.OFF}")

    def _expire(self):
        print(f"{C.RED}{self.casting_limb.creature.name}'s bloated corpse explodes!{C.OFF}")
        enemies = [c for c in self.casting_limb.creature.location.creatures if c.team not in [self.casting_limb.creature.team, "neutral"]]

        for enemy in enemies:
            limbs = enemy.limb_check("isSurface")
            random.shuffle(limbs)
            limbs = limbs[:random.randint(0, 4)]

            for limb in limbs:
                print(f"{C.RED}{enemy.name}'s {limb.name} is caught in the explosion!{C.OFF}")
                self.cont.combat.apply_damage(defender=enemy, limb=limb, damage=random.randint(0, 3))


class Explosive(sp.Effect):
    rounds = 1
    amount = 2

    def _cast(self):
        print(f"{BC.MAGENTA}The shell explodes!{BC.OFF}")
        neighbors = [self.limb] + self.limb.creature.get_neighbors(self.limb)
        for limb in neighbors:
            print(f"{C.RED}{limb.name} is caught in the explosion!{C.OFF}")
            self.cont.combat.apply_damage(defender=self.limb.creature, limb=limb, damage=self.amount)
        return True


class Lightning(sp.Effect):
    rounds = 1
    amount = 2

    def _cast(self):
        cc = self.cont.combat
        # Other limbs to strike from same target
        other_limbs_to_strike = self.limb.creature.get_neighbors(self.limb)
        if other_limbs_to_strike:
            other_limbs_to_strike = other_limbs_to_strike[:random.randrange(0, len(other_limbs_to_strike))]

        print(f"{BC.MAGENTA}Lightning zaps {BC.YELLOW}{self.limb.creature.name}{BC.MAGENTA}'s {C.RED}{self.limb.name}{BC.MAGENTA}!{BC.OFF}")
        cc.apply_damage(self.limb.creature, self.limb, self.amount)

        for limb in other_limbs_to_strike:
            print(f"{BC.MAGENTA}Lightning spreads through {C.RED}{limb.name}{BC.MAGENTA}!{BC.OFF}")
            cc.apply_damage(self.limb.creature, limb, self.amount)

        # Other limbs to strike from other targets
        other_targets = [c for c in self.limb.creature.location.creatures if c.team not in [self.casting_limb.creature.team, "neutral"] and c is not self.limb.creature]
        if other_targets:
            other_targets = other_targets[:random.randrange(0, len(other_targets))]
            for ot in other_targets:
                jump_limb = random.choice(ot.subelements[0].limb_check("isSurface"))
                random_neighbors = ot.get_neighbors(jump_limb)
                print(
                    f"{BC.MAGENTA}Lightning jumps to {BC.YELLOW}{ot.name}{BC.MAGENTA}'s {C.RED}{jump_limb.name}{BC.MAGENTA}!{BC.OFF}")
                cc.apply_damage(ot, jump_limb, self.amount)

                random_neighbors = random_neighbors[:random.randrange(0, len(random_neighbors))]
                for r_limb in random_neighbors:
                    print(f"{BC.MAGENTA}Lightning spreads through {C.RED}{r_limb.name}{BC.MAGENTA}!{BC.OFF}")
                    cc.apply_damage(ot, r_limb, self.amount)
        print(f"{BC.MAGENTA}The lightning goes out, leaving a searing afterimage.{BC.OFF}")
        return True


class Firebreath(sp.Effect):
    rounds = 1

    def _cast(self):
        print(f"{BC.MAGENTA}It exhales a great gout of fire!{BC.OFF}")
        neighbors = self.limb.creature.get_neighbors(self.limb)
        for limb in neighbors:
            if not sum([isinstance(e, FireDOT) for e in limb.active_effects]):
                e = FireDOT(casting_limb=self.casting_limb, limb=limb, controller=self.cont)
                if e.cast():
                    print(f"{C.RED}{limb.name} is caught in the flames!{BC.OFF}")
        return True
