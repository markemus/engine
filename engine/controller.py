from colorist import Color as C
from . import combat
from . import save


class Controller:
    def __init__(self, game):
        self.game = game
        self.combat = combat.Combat(self.game.char, self)

    def listtodict(self, l):
        d = {str(i): l[i] for i in range(len(l))}

        return d

    def dictprint(self, d):
        """Pretty print a dictionary. Useful for displaying command sets for user input."""
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
                exstr = str(key) + ": " + d[key].__name__
            # or object with printcolor
            elif hasattr(d[key], "printcolor") and hasattr(d[key], "name"):
                exstr = f"{str(key)}: {d[key].printcolor}{d[key].name}{C.OFF}"
            # elif other objects
            elif hasattr(d[key], "name"):
                exstr = str(key) + ": " + d[key].name
            # we don't want to ever see this, but we'd rather have it than an exception, I think.
            else:
                exstr = str(key) + ": " + str(d[key])

            # Add star if item has inv or subelements
            if (hasattr(d[key], "vis_inv") and d[key].vis_inv) or (hasattr(d[key], "elements") and d[key].elements):
                exstr = exstr + " *"

            print(exstr)

    def desc(self):
        # Sight check
        if self.game.char.limb_count("see") > 1:
            self.display_long_text(self.game.char.location.desc(full=False))
        else:
            print("You cannot see well enough to see the room well.")

    def examine(self):
        """Desc for a particular creature or element in the room."""
        # Sight check
        if self.game.char.limb_count("see") > 1:
            examine_dict = self.listtodict(self.game.char.location.creatures + self.game.char.location.elements)
            examine_dict["x"] = "look away"
            self.dictprint(examine_dict)
            i = input("\nWho/what are you examining (x for none)? ")
            if i != "x":
                self.display_long_text(examine_dict[i].desc(full=True))
            else:
                print("You look away.")
        else:
            print("You cannot see well enough to examine anything closely.")

    def display_long_text(self, text, n=20):
        """Used to display long text blobs, so that the player won't need to scroll the terminal upward to read.
        https://stackoverflow.com/a/15369848/9095840"""
        lines = text.splitlines()
        # lines = text
        while lines:
            print("\n".join(lines[:n]))
            lines = lines[n:]
            if lines:
                input("")

    def map(self):
        if self.game.char.limb_count("see") > 1:
            self.game.current_level.printMap(self.game.char)
        else:
            print("You cannot see well enough to read the map.")

    def borders(self):
        borders = self.game.char.location.borders
        for direction in borders.keys():
            # print(direction + ": " + str(borders[direction]))
            if borders[direction] is not None:
                border = f"{C.RED}{borders[direction].name}{C.OFF}"
            else:
                border = str(borders[direction])
            print(direction + ": " + border)

    def north(self):
        self.game.char.leave("n")

    def south(self):
        self.game.char.leave("s")

    def west(self):
        self.game.char.leave("w")

    def east(self):
        self.game.char.leave("e")

    def stairs(self):
        """Stairs cross over between levels."""
        self.game.char.leave(">")
        new_level = self.game.char.location.get_level()
        new_level_idx = self.game.level_list.index(new_level)
        self.game.set_current_level(new_level_idx)

    # def take(self):
    #

    # Combat
    def attack(self):
        # com = combat.Combat(self.game.char, self)
        # com.fullCombat()
        self.combat.fullCombat()

    def pick_target(self):
        enemylist = self.game.char.ai.get_target_creatures()
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
        # limblist = combat.get_target_limbs(defender)
        limblist = defender.subelements[0].limb_check("isSurface")
        limbs = self.listtodict(limblist)
        limbs["x"] = "Withhold your blow."

        self.dictprint(limbs)

        i = input("\nWhich limb are you targeting (x for none)? ")
        
        if i != "x":
            limb = limbs[i]
        else:
            limb = False

        return limb

    def pick_blocker(self, blockers):
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
