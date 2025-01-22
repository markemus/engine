import math

import engine.effectsbook as eff
import engine.spells as sp

from colorist import BrightColor as BC, Color as C


class FireDOT(eff.FireDOT):
    damage = 7


class Lightning(eff.Lightning):
    amount = 10


class RipLimb(sp.Effect):
    rounds = 1

    def _cast(self):
        if self.limb.hp <= (self.limb.base_hp / 4):
            print(f"{C.RED}The rest of the {self.limb.name} is ripped away!{C.OFF}")
            self.cont.combat.apply_damage(defender=self.limb.creature, limb=self.limb, damage=self.limb.hp + 1)


class ShatterArmor(sp.Effect):
    desc = "shattered"
    rounds = 10

    def _cast(self):
        self.update()

    def update(self):
        if self.limb.armored >= 2:
            if not hasattr(self.limb, "orig_armor"):
                self.limb.orig_armor = self.limb._armor
            self.limb._armor = self.limb.orig_armor - 1

            print(f"{BC.RED}{self.limb.name}'s armor is shattered.{BC.OFF}")

    def _expire(self):
        self.limb._armor = self.limb.orig_armor
        del self.limb.orig_armor
        print(f"{BC.CYAN}{self.limb.name}'s armor is no longer damaged.{BC.OFF}")


class Slime(sp.Effect):
    desc = "slimy"
    allow_duplicates = False
    rounds = 10

    def _cast(self):
        self._damagers = []
        self.damagers = []
        self.update()
        return True

    def update(self):
        if hasattr(self.limb, "damage"):
            weapon = self.limb.damage[1]
            if not hasattr(weapon, "orig_damage"):
                if hasattr(weapon, "_damage"):
                    weapon.orig_damage = weapon._damage
                    self._damagers.append(weapon)
                else:
                    weapon.orig_damage = weapon.damage
                    self.damagers.append(weapon)

            # Notice that this counters Flywheel, resetting damage to base then dividing.
            if hasattr(weapon, "_damage"):
                weapon._damage = weapon.orig_damage / 2
            else:
                weapon.damage = weapon.orig_damage / 2

        else:
            weapon = self.limb

        print(f"{BC.RED}{self.limb.creature.name}'s {weapon.name} is covered in slime!{BC.OFF}")

    def _expire(self):
        for weapon in self._damagers:
            weapon._damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} is no longer slimed.{BC.OFF}")

        for weapon in self.damagers:
            weapon.damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} is no longer slimed.{BC.OFF}")


class DigestSlime(sp.Effect):
    desc = "slimy"
    rounds = "forever"
    amount = 5

    def update(self):
        opponents = self.casting_limb.creature.ai.get_enemy_creatures()
        for opponent in opponents:
            limbs = [l for l in opponent.limb_check("name") if sum([isinstance(e, Slime) for e in l.active_effects])]
            for limb in limbs:
                print(f"{BC.RED}{self.casting_limb.creature.name} digests {limb.name} for {self.amount}!{BC.OFF}")
                self.cont.combat.apply_damage(defender=opponent, limb=limb, damage=self.amount)
                self.casting_limb.creature.heal(amount=self.amount)


class Flywheel(sp.Effect):
    """Increases damage as fight goes on."""
    desc = "spinning"
    rounds = "forever"
    ratio = .05

    def _cast(self):
        self._damagers = []
        self.damagers = []
        weapons = self.casting_limb.creature.limb_check("damage")
        for weapon in weapons:
            weapon = weapon.damage[1]
            if hasattr(weapon, "_damage"):
                self._damagers.append(weapon)
            elif hasattr(weapon, "damage"):
                self.damagers.append(weapon)
        return True

    def update(self):
        for weapon in self._damagers:
            if not hasattr(weapon, "orig_damage"):
                weapon.orig_damage = weapon._damage
            if not sum([isinstance(e, Slime) for e in weapon.active_effects]):
                amount = math.floor((self.ratio * weapon._damage) * 100) / 100
                weapon._damage += amount
                print(f"{BC.MAGENTA}{self.casting_limb.creature.name} revs up their {weapon.name} for {amount}!{BC.OFF}")
            else:
                print(f"{C.RED}{self.casting_limb.creature.name} tries to rev their {weapon.name} but it is slimed!{C.OFF}")

        for weapon in self.damagers:
            if not hasattr(weapon, "orig_damage"):
                weapon.orig_damage = weapon.damage
            if not sum([isinstance(e, Slime) for e in weapon.active_effects]):
                amount = math.floor((self.ratio * weapon.damage) * 100) / 100
                weapon.damage += amount
                print(f"{BC.MAGENTA}{self.casting_limb.creature.name} revs up their {weapon.name} for {amount}!{BC.OFF}")
            else:
                print(f"{C.RED}{self.casting_limb.creature.name} tries to rev their {weapon.name} but it is slimed!{C.OFF}")

    def _expire(self):
        for weapon in self._damagers:
            weapon._damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} spins down.{BC.OFF}")

        for weapon in self.damagers:
            weapon.damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} spins down.{BC.OFF}")


class EntangledVampirism(sp.Effect):
    rounds = "forever"

    def update(self):
        opponents = self.casting_limb.creature.ai.get_enemy_creatures()
        for opponent in opponents:
            limbs = [l for l in opponent.limb_check("name") if sum([isinstance(e, eff.Entangled) for e in l.active_effects]) or sum([isinstance(e, eff.Webbed) for e in l.active_effects])]
            for limb in limbs:
                vampirism = eff.MinorVampirism(casting_limb=self.casting_limb, limb=limb, controller=self.cont)
                print(f"{BC.MAGENTA}{self.casting_limb.creature.name} sucks blood from {opponent.name}'s entangled {limb.name}!{BC.OFF}")
                vampirism.cast()


class Mastery(eff.Mastery):
    rounds = "forever"
