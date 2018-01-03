import combat


class Controller():

    def __init__(self, game):
        self.game = game
        self.combatFsm = combat.Fsm(game.char)

    def listtodict(self, l):
        d = {str(i): l[i] for i in range(len(l))}

        return d

    def dictprint(self, d):
        try:
            #for lists cast to dicts in listtodict
            keys = sorted(d.keys(), key=int)
        except ValueError:
            #for builtin interfaces
            keys = sorted(d.keys())

        for key in keys:
            #if function
            if hasattr(d[key], "__name__"):
                print(str(key) + ": " + d[key].__name__)
            #elif object
            elif hasattr(d[key], "name"):            
                print(str(key) + ": " + d[key].name)
            #we don't want to ever see this, but we'd rather have it than an exception, I think.
            else:
                print(str(key) + ": " + str(d[key]))

    def desc(self):
        print(self.game.char.location.desc())

    def map(self):
        self.game.current_level.printMap(self.game.char)

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

        self.combatFsm.to_ai()