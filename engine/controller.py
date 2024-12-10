from colorist import BrightColor as BC, Color as C
from . import combat


class Controller:
    def __init__(self, game):
        self.game = game
        self.combat = combat.Combat(self.game.char, self)

    def listtodict(self, l):
        d = {str(i): l[i] for i in range(len(l))}

        return d

    def dictprint(self, d, pfunc=None):
        """Pretty print a dictionary. Useful for displaying command sets for user input.
        pfunc amends the final string before printing."""
        intkeys = []
        strkeys = []

        for key in d.keys():
            if key.isdigit():
                intkeys.append(key)
            else:
                strkeys.append(key)

        intkeys.sort(key=int)

        keys = intkeys + strkeys

        for key in keys:
            # TODO-DECIDE consider replacing str(key) with a colored string
            # Keys should always have the same (brown) color.
            kval = f"{C.YELLOW}{str(key)}{C.OFF}: "
            # if function
            if hasattr(d[key], "__name__"):
                exstr = kval + d[key].__name__
            # or object with printcolor
            elif hasattr(d[key], "printcolor") and hasattr(d[key], "name"):
                exstr = kval + f"{d[key].printcolor}{d[key].name}{C.OFF}"
            # elif other objects
            elif hasattr(d[key], "name"):
                exstr = kval + f"{d[key].name}"
            # we don't want to ever see this, but we'd rather have it than an exception, I think.
            # This seems to be what happens when key is an int.
            else:
                exstr = kval + str(d[key])

            # pfunc processes d[key] and returns a string for printing. USE SPARINGLY.
            if pfunc:
                exstr = pfunc(exstr, d[key])

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

    def character_sheet(self):
        gc = self.game.char
        weapons = [f"{x.name}: {BC.YELLOW}{x.damage[1].name}{BC.OFF} {BC.RED}({x.damage[0]}){BC.OFF}\n" for x in gc.subelements[0].limb_check('damage')]
        inventory = [f"{BC.CYAN}{x.name}{BC.OFF}" for x in gc.inventory]

        if gc.limb_count("see") > 1:
            cs = f"\nCharacter Sheet\n" \
                 f"Name: {BC.YELLOW}{gc.name}{BC.OFF}\n" \
                 f"\nWeapons\n" \
                 f"{''.join(weapons)}" \
                 f"\nInventory\n" \
                 f"{''.join(inventory)}\n\n"
            self.display_long_text(cs)

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

    # TODO consider input values other than those listed as "x"
    def inventory(self):
        """Transfer items between the character's inventory and another object."""
        # Sight check
        if self.game.char.limb_count("see") > 1:
            inventory_dict = self.listtodict(self.game.char.location.elements)
            inventory_dict["x"] = "look away"
            self.dictprint(inventory_dict)

            i = input("\nWhich inventory would you like to exchange with (x for none)? ")
            if i != "x":
                other_inv = inventory_dict[i].vis_inv
                # Show inventories
                i = input("\nTransfer to or from your inventory (t/f)? ")
                if i == "t":
                    origin_inv = other_inv
                    target_inv = self.game.char.inventory
                elif i == "f":
                    origin_inv = self.game.char.inventory
                    target_inv = other_inv
                else:
                    print("You decide not to transfer at all.")
                    return
            else:
                print("You decide not to transfer at all.")
                return

            # Transfer
            self.dictprint(self.listtodict(origin_inv))
            i = input("\nWhich item would you like to transfer (x for none)?")
            if i != "x":
                origin_inv[int(i)].transfer(self.game.char, origin_inv, target_inv)
        else:
            print("You cannot see well enough for that.")

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

        i = input(f"{BC.GREEN}\nWho are you attacking {C.YELLOW}(x for none){C.GREEN}?{BC.OFF}")

        if i != "x":
            defender = targets[i]
        else:
            defender = False

        return defender

    def pick_weapon(self, weapons):
        weapons = self.listtodict(weapons)
        self.dictprint(weapons, pfunc=lambda x, y: x + f" {C.BLUE}({y.damage[1].name} {y.damage[0]}){C.OFF}")
        weapon = weapons[input(f"{BC.GREEN}Pick a weapon:{BC.OFF}")]
        return weapon

    def pick_limb(self, defender):
        # limblist = combat.get_target_limbs(defender)
        limblist = defender.subelements[0].limb_check("isSurface")
        limbs = self.listtodict(limblist)
        limbs["x"] = "Withhold your blow."

        def a_pfunc(str, obj):
            if hasattr(obj, "armor"):
                str = f"{str} {C.BLUE}({obj.armor}){C.OFF}"
            if hasattr(obj, "hp"):
                str = f"{str} {C.RED}({obj.hp}){C.OFF}"
            return str
        self.dictprint(limbs, pfunc=a_pfunc)

        i = input(f"\n{C.GREEN}Which limb are you targeting {C.YELLOW}(x for none){C.GREEN}? {C.OFF}")

        # TODO exception handling for this and other similar controller functions when non-indexed key is pressed.
        #  Easiest way is to just treat all unknown as x.
        if i != "x":
            limb = limbs[i]
        else:
            limb = False

        return limb

    def pick_blocker(self, blockers):
        blockers = self.listtodict(blockers)
        blockers["x"] = "Accept the blow."

        def a_pfunc(str, obj):
            if hasattr(obj, "armor"):
                str = f"{str} {C.BLUE}({obj.armor}){C.OFF}"
            if hasattr(obj, "hp"):
                str = f"{str} {C.RED}({obj.hp}){C.OFF}"
            return str

        self.dictprint(blockers, pfunc=a_pfunc)

        i = input(f"\n{BC.GREEN}Which {C.CYAN}limb{BC.GREEN} would you like to block with {C.YELLOW}(x for none){BC.GREEN}?{C.OFF}")

        if i != "x":
            blocker = blockers[i]
        else:
            blocker = False

        return blocker

    def rest(self):
        print(f"{C.RED}{self.game.char.name}{C.OFF} rests for one hour.")
        for limb in self.game.char.subelements[0].limb_check(tag="hp"):
            if limb.hp < limb.base_hp:
                hp_diff = 1 if (limb.base_hp - limb.hp >= 1) else (limb.base_hp - limb.hp)
                limb.hp += hp_diff
                print(f"{C.RED}{self.game.char.name}{C.OFF}'s {BC.RED}{limb.name}{BC.OFF} heals a little {BC.RED}({limb.hp}/{limb.base_hp}){BC.OFF}.")
