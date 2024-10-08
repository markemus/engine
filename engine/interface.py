"""An Interface is used to issue commands to the game's controller. Through it the player controls
all aspects of playing the game, such as entering or exiting combat, as well as movement, exploration, and saves."""
from colorist import Color as C
from colorist import BrightColor as BC
from transitions import Machine

from . import controller
from . import save


class Interface:
    def __init__(self, game):
        self.cont = controller.Controller(game)
        states = ["move", "fight"]
        self.machine = Machine(model=self, states=states, initial="move")

        # TODO-DONE need commands for: examine inventory of Elements, examine creature desc()
        move = {
            "h": self.help,
            "l": self.cont.desc,
            "e": self.cont.examine,
            "i": self.cont.inventory,
            "m": self.cont.map,
            "b": self.cont.borders,
            "w": self.cont.north,
            "s": self.cont.south,
            "d": self.cont.east,
            "a": self.cont.west,
            ">": self.cont.stairs,
            "f": self.fight,
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

    # We need these for our interface- transition methods are partial functions and
    # have no __name__ or clean str() cast.
    def fight(self):
        print("You ready yourself for a fight.")
        self.to_fight()

    def move(self):
        print("You set out on your quest again.")
        self.to_move()

    # Standard

    def command(self):
        print(f"Available commands: {BC.BLUE}{''.join(self.commands[self.state].keys())}{C.OFF}")
        x = input(f"{BC.GREEN}Choose a command (h for help): {C.OFF}")
        if x in self.commands[self.state].keys():
            self.commands[self.state][x]()
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
