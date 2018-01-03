from transitions import Machine

import game
import man
import styles
import combat

class Interface():
    def __init__(self, game):
        self.game = game
        states = ["move", "fight"]

        move = {
            "w" : self.north,
            "s" : self.south,
            "a" : self.west,
            "d" : self.east,
            "l" : self.desc,
            "m" : self.map,
            "b" : self.borders,
            "h" : self.help,
            "f" : self.attack
        }

        basics = {
            "l" : self.desc,
            "m" : self.map,
            "h" : self.help,
        }

        fight = {}

        self.commands = {
            "move" : move,
            "fight" : fight
        }
        self.machine = Machine(model=self, states=states, initial="move")
        self.machine.on_enter_fight('get_targets')

    def command(self):
        x = input("Choose a command: ")
        if x in self.commands[self.state].keys():
            self.commands[self.state][x]()
        else:
            print(x, "is not a valid command.")

    def help(self):
        allcoms = self.commands[self.state]

        self.dictprint(allcoms)

    def dictprint(self, d):
        for key in sorted(d.keys(), key=int):
            #if method
            try:
                print(str(key) + ": " + d[key].__name__)
            #elif object
            except AttributeError:
                print(str(key) + ": " + d[key].name)

    def listtodict(self, l):
        d = {str(i): l[i] for i in range(len(l))}

        return d

    def desc(self):
        print(self.game.char.location.desc())

    def map(self):
        self.game.current_level.printMap()

    def borders(self):
        borders = self.game.char.location.borders
        for direction in borders.keys():
            print(direction + ": " + str(borders[direction]))

    def north(self):
        self.game.char.leave("n")

    def south(self):
        self.game.char.leave("s")

    def west(self):
        self.game.char.leave("w")

    def east(self):
        self.game.char.leave("e")

    #combat

    def attack(self):
        targetlist = combat.get_target_creatures(self.game.char)
        targets = self.listtodict(targetlist)

        self.dictprint(targets)

        i = input("Who are you attacking?")
        defender = targets[i]

        limblist = combat.get_target_limbs(defender)
        limbs = self.listtodict(limblist)

        self.dictprint(limbs)

        j = input("Which limb are you targeting?")
        limb = limbs[j]

        weapon = combat.pick_weapon(self.game.char)
        print("interface.attack: ", weapon)
        print("interface.attack: ", combat.check_damage(weapon))

        combat.attack(defender, limb, weapon)











if __name__ == "__main__":
    x = game.Game("testGame", styles.Castle)
    adam = man.man("Adam", location=x.level_list[0].start)
    x.level_list[0].start.addCreature(adam)
    x.set_char(adam)
    adam.team = "player"
    i = Interface(x)
    print(i.state)
    # i.to_combat()
    print(adam.location.borders)
    # combat.round(x.char)
    while True:
        i.command()




# def you():                  #defines the "creature.you" object, which is the PC
#     race_list_names = []
#     count = 1
#     for n in creature.race_list:            #creates a list of the starting races names
#         race_list_names.append(str(count) + ". " + n.name)
#         count = count + 1
#     print(race_list_names)
#     x = input("Please pick a race by choosing a number.")
#     try:                                    #checks that they're using numbers, and that the numbers aren't too large
#         if int(x) > 0:                      #checks that they're not using negatives, or zero (which would count backward down the list)
#             print(race_list_names[int(x)-1])
#             creature.you = creature.race_list[int(x)-1]
#             creature.you.name = input("Please choose a name for your character.")
#         else:
#             print("That number has no equivalent value. Please try again.")
#             you()
#     except (ValueError, IndexError):
#         print("That number has no equivalent value. Please try again.")

# you()