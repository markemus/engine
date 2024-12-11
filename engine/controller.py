import textwrap

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
            if (hasattr(d[key], "vis_inv") and d[key].vis_inv) or (hasattr(d[key], "subelements") and d[key].subelements) or (hasattr(d[key], "equipment") and d[key].equipment):
                exstr = exstr + " *"

            print(exstr)

    def desc(self):
        # Sight check
        if self.game.char.limb_count("see") > 1:
            self.display_long_text(self.game.char.location.desc(full=False))
        else:
            print(f"{C.RED}You cannot see well enough to see the room well.{C.OFF}")

    def character_sheet(self):
        gc = self.game.char
        weapons = [f"{x.name}: {BC.YELLOW}{x.damage[1].name}{BC.OFF} {BC.RED}({x.damage[0]}){BC.OFF}\n" for x in gc.subelements[0].limb_check('damage')]
        inventory = [f"{BC.CYAN}{x.name}{BC.OFF}" for x in gc.vis_inv]

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
            i = input(f"{BC.GREEN}\nWho/what are you examining (x for none)?{BC.OFF}")
            if i != "x":
                self.display_long_text(examine_dict[i].desc(full=True))
            else:
                print(f"{BC.CYAN}You look away.{BC.OFF}")
        else:
            print(f"{C.RED}You cannot see well enough to examine anything closely.{C.OFF}")

    # TODO consider input values other than those listed as "x"
    def inventory(self):
        """Transfer items between the character's inventory and another object."""
        # Sight check
        if self.game.char.limb_count("see") > 1:
            # TODO gather vis_invs in room (not all elements)
            room_inventories = [elem for elem in self.game.char.location.elements if hasattr(elem, "vis_inv")]
            your_inventories = self.game.char.subelements[0].find_invs()
            all_inventories = your_inventories + room_inventories
            inventory_dict = self.listtodict(all_inventories)
            inventory_dict["x"] = "look away"
            self.dictprint(inventory_dict)

            i = input(f"\n{BC.GREEN}First, which inventory would you like to take from (x to cancel)?{BC.OFF}")
            if i != "x":
                origin_inv = inventory_dict[i].vis_inv
                del inventory_dict[i]
                j = input(f"\n{BC.GREEN}Second, which inventory would like to transfer to (x to cancel)?{BC.OFF}")
                if j != "x":
                    target_inv = inventory_dict[j].vis_inv
                    self.dictprint(self.listtodict(origin_inv))
                    k = input(f"\n{BC.GREEN}Which item would you like to transfer (x to cancel)?{BC.OFF}")
                    origin_inv[int(k)].transfer(self.game.char, origin_inv, target_inv)
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
        return self.check_safety()

    def south(self):
        self.game.char.leave("s")
        return self.check_safety()

    def west(self):
        self.game.char.leave("w")
        return self.check_safety()

    def east(self):
        self.game.char.leave("e")
        return self.check_safety()

    def stairs(self):
        """Stairs cross over between levels."""
        left = self.game.char.leave(">")
        if left:
            new_level = self.game.char.location.get_level()
            new_level_idx = self.game.level_list.index(new_level)
            self.game.set_current_level(new_level_idx)
            # TODO only print level_text if this is first time entering level (and entering first_room)
            print(self.game.current_level.level_text)
        return self.check_safety()

    # Combat
    def attack(self):
        self.combat.fullCombat()

    def check_safety(self):
        """Checks whether the current room is safe."""
        for creature in self.game.char.location.creatures:
            if creature.aggressive and (creature.team != self.game.char.team):
                return False
        return True

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

    def eat(self):
        # edibles = self.listtodict([item for item in self.game.char.vis_inv if hasattr(item, "edible") and item.edible])
        invs = self.listtodict(self.game.char.subelements[0].find_invs())
        invs["x"] = "Cancel"
        self.dictprint(invs)
        i = input(f"\n{BC.GREEN}Which inventory would you like to eat from?{BC.OFF}")

        if i != "x":
            edibles = self.listtodict([item for item in invs[i].vis_inv if hasattr(item, "edible") and item.edible])
            edibles["x"] = "Don't eat anything."
            self.dictprint(edibles)
            j = input(f"\n{BC.GREEN}Select an item to eat/drink:{BC.OFF}")

            if j in edibles.keys() and j != "x":
                food = edibles[j]
                food.eat(self.game.char)
                invs[i].vis_inv.remove(food)
