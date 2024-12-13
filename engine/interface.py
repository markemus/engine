"""An Interface is used to issue commands to the game's controller. Through it the player controls
all aspects of playing the game, such as entering or exiting combat, as well as movement, exploration, and saves."""
from colorist import Color as C
from colorist import BrightColor as BC

from . import controller
from . import save


# TODO equipping and unequipping armor and weapons
# TODO game over and load game
# TODO game stats sheet (kills, limbs lost?)
class Interface:
    def __init__(self, game):
        self.cont = controller.Controller(game)
        self.states = ["move", "fight"]
        self.state = "move"

        move = {
            "h": self.help,
            "c": self.cont.character_sheet,
            "l": self.cont.desc,
            "e": self.cont.examine,
            "i": self.cont.inventory,
            "p": self.cont.put_on,
            "t": self.cont.take_off,
            "m": self.cont.map,
            "b": self.cont.borders,
            "w": self.cont.north,
            "s": self.cont.south,
            "d": self.cont.east,
            "a": self.cont.west,
            ">": self.cont.stairs,
            "f": self.fight,
            "r": self.cont.rest,
            "q": self.cont.eat,
            "/": self.save,
        }

        fight = {
            "h": self.help,
            "l": self.cont.desc,
            "e": self.cont.examine,
            "m": self.cont.map,
            "a": self.cont.attack,
            "w": self.move
        }

        self.commands = {
            "move": move,
            "fight": fight
        }

    # Transitions
    def fight(self):
        print(f"{C.RED}You ready yourself for a fight.{C.OFF}")
        self.state = self.states[1]

    def move(self):
        safe = self.cont.check_safety()
        if safe:
            print(f"{BC.CYAN}You set out on your quest again.{BC.OFF}")
            self.state = self.states[0]
        else:
            print(f"{BC.CYAN}There are still enemies around.{BC.OFF}")

    # Commands
    def command(self):
        print(f"Available commands: {BC.BLUE}{''.join(self.commands[self.state].keys())}{C.OFF}")
        x = input(f"{BC.GREEN}Choose a command (h for help): {C.OFF}")
        if x in self.commands[self.state].keys():
            safety_val = self.commands[self.state][x]()
            # This should check after every action unless char is already fighting. None should be safe.
            if safety_val == False and self.state != "fight":
                self.fight()
        else:
            print(x, "is not a valid command.")

    def help(self):
        allcoms = self.commands[self.state]

        self.cont.dictprint(allcoms)

    def save(self):
        savepath = input("Please enter the filename for your save:")
        save.save(self, savepath)

    def load(self):
        savepath = input("Load stored save:")
        i = save.load(savepath)
        return i
