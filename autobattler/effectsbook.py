import engine.effectsbook as eff
import engine.spells as sp

from colorist import BrightColor as BC, Color as C


class FireDOT5(eff.FireDOT):
    damage = 5


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
    rounds = 10

    def _cast(self):
        self._damagers = []
        self.damagers = []
        self.update()

    def update(self):
        if self.limb.damage:
            weapon = self.limb.damage[1]
            if not hasattr(weapon, "orig_damage"):
                if hasattr(weapon, "_damage"):
                    weapon.orig_damage = weapon._damage
                    weapon._damage = weapon._damage / 2
                    self._damagers.append(weapon)
                else:
                    weapon.orig_damage = weapon.damage
                    weapon.damage = weapon.damage / 2
                    self.damagers.append(weapon)
        else:
            weapon = self.limb

        print(f"{BC.RED}{self.limb.creature}'s {weapon.name} is covered in slime!{BC.OFF}")

    def _expire(self):
        for weapon in self._damagers:
            weapon._damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} is no longer slimed.{BC.OFF}")

        for weapon in self.damagers:
            weapon.damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{BC.CYAN}{self.limb.creature}'s {weapon.name} is no longer slimed.{BC.OFF}")
