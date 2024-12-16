"""An Interface is used to issue commands to the game's controller. Through it the player controls
all aspects of playing the game, such as entering or exiting combat, as well as movement, exploration, and saves."""
from colorist import Color as C
from colorist import BrightColor as BC

from . import controller
from . import save


# TODO game stats sheet (kills, limbs lost?)
class Interface:
    def __init__(self, game):
        self.cont = controller.Controller(game)
        self.states = ["move", "fight", "dead"]
        self.state = "move"

        move = {
            "h": self.help,
            "c": self.cont.character_sheet,
            # "H": self.cont.display_health,
            "l": self.cont.desc,
            "e": self.cont.examine,
            "i": self.cont.inventory,
            "p": self.cont.put_on,
            "t": self.cont.take_off,
            "g": self.cont.grasp,
            "u": self.cont.ungrasp,
            "m": self.cont.map,
            # "b": self.cont.borders,
            "w": self.cont.north,
            "s": self.cont.south,
            "d": self.cont.east,
            "a": self.cont.west,
            ">": self.cont.stairs,
            "f": self.fight,
            "r": self.cont.rest,
            "q": self.cont.eat,
            "/": self.save,
            "*": self.load,
        }

        fight = {
            "h": self.help,
            "c": self.cont.character_sheet,
            # "H": self.cont.display_health,
            "l": self.cont.desc,
            "e": self.cont.examine,
            "m": self.cont.map,
            "q": self.cont.eat,
            "a": self.cont.attack,
            "w": self.move
        }

        dead = {
            "h": self.help,
            "*": self.load,
        }

        self.commands = {
            "move": move,
            "fight": fight,
            "dead": dead,
        }

    # Transitions
    def fight(self):
        print(f"{C.RED}You ready yourself for a fight.{C.OFF}")
        self.state = self.states[1]

    def dead(self):
        print(self.cont.game.death_splash)
        self.state = self.states[2]

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
            # Commands that lead to a state that would initialize combat should return False
            if safety_val is False and self.state == "move":
                self.fight()
            if self.cont.game.char.dead and self.state != "dead":
                self.dead()
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
        # Overwrite game with the saved game
        self.cont.game = i.cont.game
        self.state = i.state
        print("Save loaded.")
