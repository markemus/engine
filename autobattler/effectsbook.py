import engine.effectsbook as eff
import engine.spells as sp

from colorist import BrightColor as BC, Color as C


class FireDOT(eff.FireDOT):
    damage = 5


class Lightning(eff.Lightning):
    amount = 10


class ShatterArmor(sp.Effect):
    desc = "shattered"

    def _cast(self):
        self.update()

    def update(self):
        if self.limb.armored >= 2:
            if not hasattr(self.limb, "orig_armor"):
                self.limb.orig_armor = self.limb._armor
            self.limb._armor = self.limb.orig_armor - 1

    def _expire(self):
        self.limb._armor = self.limb.orig_armor
        del self.limb.orig_armor


class Slime(sp.Effect):
    desc = "slimy"

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

                print(f"{C.RED}{self.limb.creature}{BC.GREEN}'s {BC.YELLOW}{weapon.name}{BC.GREEN} is covered in slime!{BC.OFF}")

    def _expire(self):
        for weapon in self._damagers:
            weapon._damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{C.RED}{self.limb.creature}{BC.GREEN}'s {BC.YELLOW}{weapon.name}{BC.GREEN} is no longer slimed.{BC.OFF}")

        for weapon in self.damagers:
            weapon.damage = weapon.orig_damage
            del weapon.orig_damage
            print(f"{C.RED}{self.limb.creature}{BC.GREEN}'s {BC.YELLOW}{weapon.name}{BC.GREEN} is no longer slimed.{BC.OFF}")
