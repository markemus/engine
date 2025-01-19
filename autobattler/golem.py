import engine.creature as cr

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
    price = 50
    suits = []
