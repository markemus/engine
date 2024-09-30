from transitions import Machine

from . import controller


class Interface:
    def __init__(self, game):
        # self.game = game
        self.cont = controller.Controller(game)
        states = ["move", "fight"]
        self.machine = Machine(model=self, states=states, initial="move")

        move = {
            "h": self.help,
            "l": self.cont.desc,
            "m": self.cont.map,
            "w": self.cont.north,
            "s": self.cont.south,
            "a": self.cont.west,
            "d": self.cont.east,
            ">": self.cont.stairs,
            "b": self.cont.borders,
            "f": self.fight
        }

        fight = {
            "h": self.help,
            "l": self.cont.desc,
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
        print("Available commands: "+"".join(self.commands[self.state].keys()))
        x = input("Choose a command (h for help): ")
        if x in self.commands[self.state].keys():
            self.commands[self.state][x]()
        else:
            print(x, "is not a valid command.")

    # TODO-DONE we should print a string of all concatenated commands available under the map: HLMS... for a visual cue.
    def help(self):
        allcoms = self.commands[self.state]

        self.cont.dictprint(allcoms)
