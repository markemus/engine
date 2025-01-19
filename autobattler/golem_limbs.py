import engine.creature as cr
import engine.effectsbook as eff
import autobattler.effectsbook as aeff

from colorist import BrightColor as BC, Color as C
from engine import utils


# TODO-DONE sublimb_size param that limits the total size of limbs allowed to be attached.
class GolemBaseLimb:
    """Should only be used in inheritance in combination with some Limb class."""
    limb_type = None
    can_parent = []
    consumable = True
    sublimb_size = 0

    def has_free_space(self, amount):
        """Checks whether limb has room for another subelement."""
        used_space = sum([x.size for x in self.subelements])
        if used_space + amount <= self.sublimb_size:
            return True

    def use(self, char, controller):
        if char.golem:
            parent_limbs = [x for x in char.golem.limb_check("can_parent") if self.limb_type in x.can_parent and x.has_free_space(self.size)]
            parent_limbs = utils.listtodict(parent_limbs, add_x=True)
            utils.dictprint(parent_limbs)
            i = input(f"{BC.GREEN}Select a parent limb to attach this limb to:{BC.OFF} ")
            if i in parent_limbs.keys() and i != "x":
                parent_limb = parent_limbs[i]
                parent_limb.subelements.append(self)
                print(f"{BC.MAGENTA}{char.name} grafts the {self.name} onto {char.golem.name}'s {parent_limb.name}.{BC.OFF}")
                return True
        else:
            print(f"{C.RED}You must deploy a golem before you can graft limbs to it.{C.OFF}")


class GolemLimb(cr.Limb, GolemBaseLimb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GolemWeapon(cr.Weapon, GolemBaseLimb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Buzzsaw(GolemWeapon):
    name = "buzzsaw"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 30
    weapon_effects = [aeff.RipLimb]
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Hammer(GolemWeapon):
    name = "hammer"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 20
    weapon_effects = [aeff.ShatterArmor, eff.Stun]
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


class Flamethrower(GolemWeapon):
    name = "flamethrower"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 5
    weapon_effects = [aeff.FireDOT5]
    price = 5
    colors = ["red", "brown", "yellow", "black"]
    textures = ["tubular"]


class Taser(GolemWeapon):
    name = "taser"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 2
    weapon_effects = [aeff.Lightning]
    price = 5
    colors = ["gray", "silver"]
    textures = ["metal"]


class Slimer(GolemWeapon):
    name = "slimer"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 50
    _damage = 20
    weapon_effects = [aeff.Slime]
    price = 5
    colors = ["green"]
    textures = ["slimy"]


class Shield(GolemLimb):
    name = "shield"
    subelement_classes = []
    limb_type = "hand"
    base_hp = 100
    blocker = True
    _armor = 4
    price = 5
    colors = ["gray", "black", "rusty"]
    textures = ["steel", "iron"]


basic_weapons = [Buzzsaw, Hammer, Flamethrower, Taser, Slimer, Shield]
