import random

import engine.creature as cr
import assets.namelists as nm

from assets.dwarf import Dwarf
from assets.hobbit import Hobbit
from assets.human import Human
from assets.elf import Elf
from assets.goblin import ServantGoblin

from autobattler import golem_limbs as gl

from colorist import BrightColor as BC, Color as C


class Golem(cr.creature):
    team = "golem"
    namelist = ["golem"]
    colors = ["red", "brown", "yellow", "black", "beige"]
    textures = ["clay"]
    usable = True
    consumable = True

    def use(self, char, controller):
        if char.golem:
            print(f"{C.RED}{char} already has a golem deployed!{C.OFF}")
            return False

        if char.grasp_check():
            self.name = input(f"{BC.GREEN}Name your golem:{BC.OFF} ")
            char.location.creatures.append(self)
            self.location = char.location
            char.companions.append(self)
            char.golem = self
            self.team = "combatant"
            print(f"{BC.YELLOW}{char.name} deploys {self.name}!{BC.OFF}")
            return True


class LargeGolem(Golem):
    classname = "large golem"
    namelist = ["large golem"]
    baseElem = gl.LargeTorso
    price = 50
    suits = []


class SmallGolem(Golem):
    classname = "small golem"
    namelist = ["small golem"]
    baseElem = gl.SmallTorso
    price = 30
    suits = []


def generate_golem_l0(location):
    owner_race = random.choice([Dwarf, Hobbit, Human, Elf, ServantGoblin])
    owner = owner_race(location=location)
    owner.team = "neutral"
    golem = random.choice([LargeGolem, SmallGolem])(location=location)
    golem.team = "opponent"
    golem.name = random.choice(nm.names["golem"])
    owner.location.creatures.append(owner)
    owner.location.creatures.append(golem)

    weapon = random.choice(gl.basic_weapons)
    extremities = [x for x in golem.limb_check("can_parent") if x.has_free_space(weapon.size)]
    if extremities:
        extremity = extremities[0]
        color = random.choice(weapon.colors)
        texture = random.choice(weapon.textures)
        extremity.subelements.append(weapon(color=color, texture=texture, creature=golem))

    return owner, golem
