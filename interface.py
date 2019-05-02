from transitions import Machine

import controller
import game
import man
import styles

class Interface():
    def __init__(self, game):
        # self.game = game
        self.cont = controller.Controller(game)
        states = ["move", "fight"]
        self.machine = Machine(model=self, states=states, initial="move")

        move = {
            "h" : self.help,
            "l" : self.cont.desc,
            "m" : self.cont.map,
            "w" : self.cont.north,
            "s" : self.cont.south,
            "a" : self.cont.west,
            "d" : self.cont.east,
            "b" : self.cont.borders,
            "f" : self.fight
        }

        fight = {
            "h" : self.help,
            "l" : self.cont.desc,
            "m" : self.cont.map,
            "a" : self.cont.attack,
            "w" : self.move
        }

        self.commands = {
            "move" : move,
            "fight" : fight
        }

    #transitions

    #we need these for our interface- transition methods are partial functions and have no __name__ or clean str() cast.
    def fight(self):
        print("You ready yourself for a fight.")
        self.to_fight()

    def move(self):
        print("You set out on your quest again.")
        self.to_move()

    #standard

    def command(self):
        x = input("Choose a command: ")
        if x in self.commands[self.state].keys():
            self.commands[self.state][x]()
        else:
            print(x, "is not a valid command.")

    def help(self):
        allcoms = self.commands[self.state]

        self.cont.dictprint(allcoms)






if __name__ == "__main__":
    x = game.Game("testGame", styles.Castle)
    adam = man.Man("Adam", location=x.level_list[0].start)
    x.level_list[0].start.creatures = [adam] + x.level_list[0].start.creatures
    x.set_char(adam)
    adam.team = "player"
    i = Interface(x)
    print(i.state)
    print(adam.location.borders)
    while True:
        i.command()