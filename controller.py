import combat

class Controller:
    def __init__(self, game):
        self.game = game
        # self.combatFsm = combat.Fsm(game.char)

    def listtodict(self, l):
        d = {str(i): l[i] for i in range(len(l))}

        return d

    def dictprint(self, d):
        """What is this tho."""
        intkeys = []
        strkeys = []

        for key in d.keys():
            if key.isdigit():
                intkeys.append(key)
            else:
                strkeys.append(key)

        intkeys.sort(key=int)
        strkeys.sort()

        keys = intkeys + strkeys

        for key in keys:
            # if function
            if hasattr(d[key], "__name__"):
                print(str(key) + ": " + d[key].__name__)
            # elif object
            elif hasattr(d[key], "name"):            
                print(str(key) + ": " + d[key].name)
            # we don't want to ever see this, but we'd rather have it than an exception, I think.
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

    # Combat
    def attack(self):
        com = combat.Combat(self.game.char, self)
        com.fullCombat()

    def pick_target(self):
        enemylist = combat.get_target_creatures(self.game.char)
        targets = self.listtodict(enemylist)
        targets["x"] = "Withhold your blow."

        self.dictprint(targets)

        i = input("\nWho are you attacking (x for none)? ")

        if i != "x":
            defender = targets[i]
        else:
            defender = False

        return defender

    def pick_limb(self, defender):
        limblist = combat.get_target_limbs(defender)
        limbs = self.listtodict(limblist)
        limbs["x"] = "Withhold your blow."

        self.dictprint(limbs)

        i = input("\nWhich limb are you targeting (x for none)? ")
        
        if i != "x":
            limb = limbs[i]
        else:
            limb = False

        return limb

    def pick_blocker(self, limb, blockers):
        blockers = self.listtodict(blockers)
        blockers["x"] = "Accept the blow."

        self.dictprint(blockers)

        i = input("\nWhich limb would you like to block with (x for none)?")

        if i != "x":
            blocker = blockers[i]
        else:
            blocker = False

        return blocker

    def defend(self, cr):
        print("{} swings their {} at your {}.".format(cr.attacker.name, cr.weapon.name, cr.target.name))
