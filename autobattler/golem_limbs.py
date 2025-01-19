import engine.creature as cr
import autobattler.effectsbook as aeff

from colorist import BrightColor as BC, Color as C
from engine import utils


class GolemLimb(cr.Limb):
    limb_type = None
    can_parent = None

    def use(self, char, controller):
        parent_limbs = [x for x in char.golem.limb_check("can_parent") if self.limb_type in x.can_parent]
        parent_limbs = utils.listtodict(parent_limbs, add_x=True)
        utils.dictprint(parent_limbs)
        i = input(f"{BC.GREEN}Select a parent limb to attach this limb to:{BC.OFF} ")
        if i in parent_limbs.keys() and i != "x":
            parent_limb = parent_limbs[i]
            inv = [x for x in char.find_invs() if self in x.vis_inv][0]
            parent_limb.subelements.append(self)
            inv.vis_inv.remove(self)
            print(f"{BC.MAGENTA}{char.name} grafts the {self.name} onto {char.golem.name}'s {parent_limb.name}.{BC.OFF}")


class GolemWeapon(cr.Weapon):
    limb_type = None
    can_parent = None

    def use(self, char, controller):
        parent_limbs = [x for x in char.golem.limb_check("can_parent") if self.limb_type in x.can_parent]
        parent_limbs = utils.listtodict(parent_limbs, add_x=True)
        utils.dictprint(parent_limbs)
        i = input(f"{BC.GREEN}Select a parent limb to attach this limb to:{BC.OFF} ")
        if i in parent_limbs.keys() and i != "x":
            parent_limb = parent_limbs[i]
            inv = [x for x in char.find_invs() if self in x.vis_inv][0]
            parent_limb.subelements.append(self)
            inv.vis_inv.remove(self)
            print(f"{BC.MAGENTA}{char.name} grafts the {self.name} onto {char.golem.name}'s {parent_limb.name}.{BC.OFF}")


class Buzzsaw(GolemWeapon):
    limb_type = "hand"
    _damage = 30


class Hammer(GolemWeapon):
    limb_type = "hand"
    _damage = 20
    weapon_effects = [aeff.ShatterArmor]


class Flamethrower(GolemWeapon):
    limb_type = "hand"
    _damage = 5
    weapon_effects = [aeff.FireDOT]


class Taser(GolemWeapon):
    limb_type = "hand"
    _damage = 2
    weapon_effects = [aeff.Lightning]


class Slimer(GolemWeapon):
    limb_type = "hand"
    _damage = 20
    weapon_effects = [aeff.Slime]
