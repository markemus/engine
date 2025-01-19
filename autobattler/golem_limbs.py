import engine.creature as cr
import engine.effectsbook as eff
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
    base_hp = 50

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
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Hammer(GolemWeapon):
    limb_type = "hand"
    _damage = 20
    weapon_effects = [aeff.ShatterArmor, eff.Stun]
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Flamethrower(GolemWeapon):
    limb_type = "hand"
    _damage = 5
    weapon_effects = [aeff.FireDOT5]
    price = 5
    colors = ["red", "brown", "yellow", "black"]
    textures = ["tubular"]


class Taser(GolemWeapon):
    limb_type = "hand"
    _damage = 2
    weapon_effects = [aeff.Lightning]
    price = 5
    colors = ["gray", "silver"]
    textures = ["metal"]


class Slimer(GolemWeapon):
    limb_type = "hand"
    _damage = 20
    weapon_effects = [aeff.Slime]
    price = 5
    colors = ["green"]
    textures = ["slimy"]


class Shield(GolemLimb):
    limb_type = "hand"
    blocker = True
    _armor = 4
    base_hp = 50
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


basic_weapons = [Buzzsaw, Hammer, Flamethrower, Taser, Slimer, Shield]
