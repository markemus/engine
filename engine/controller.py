import random
import textwrap

from colorist import BrightColor as BC, Color as C
from . import combat


class Controller:
    def __init__(self, game):
        self.game = game
        self.combat = combat.Combat(self.game.char, self)

    def listtodict(self, l, add_x=False):
        d = {str(i): l[i] for i in range(len(l))}
        if add_x:
            d["x"] = "Cancel"

        return d

    def dictprint(self, d, pfunc=None, show_invs=False):
        """Pretty print a dictionary. Useful for displaying command sets for user input.
        pfunc amends the final string before printing.
        show_invs puts a star next to items with inventories."""
        intkeys = []
        strkeys = []

        for key in d.keys():
            if key.isdigit():
                intkeys.append(key)
            else:
                strkeys.append(key)

        intkeys.sort(key=int)

        keys = intkeys + strkeys
        fullstr = ""

        for key in keys:
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

            # pfunc processes d[key] and returns a string for printing.
            if pfunc:
                exstr = pfunc(exstr, d[key])

            if show_invs:
                # Add star if item has inv or subelements
                if (hasattr(d[key], "vis_inv") and d[key].vis_inv) or (hasattr(d[key], "equipment") and d[key].equipment):
                    exstr = exstr + " *"

            fullstr = fullstr + "\n" + exstr
        self.display_long_text(fullstr)

    def desc(self):
        # Sight check
        if self.game.char.limb_count("see") >= 1:
            self.display_long_text(self.game.char.location.desc(full=False))
        else:
            print(f"{C.RED}You cannot see well enough to see the room well.{C.OFF}")

    def character_sheet(self):
        gc = self.game.char
        weapons = [f"{x.name}: {C.BLUE}{x.damage[1].name}{C.OFF} {C.RED}({x.damage[0]}){C.OFF}\n" for x in gc.subelements[0].limb_check('damage')]

        inventory = ""
        for subelement in gc.subelements[0].limb_check('equipment'):
            for equipment in subelement.equipment:
                if hasattr(equipment, "vis_inv") and equipment.vis_inv:
                    inv_elements = '\n  '.join([x.name for x in equipment.vis_inv])
                    inventory = inventory + f"{equipment.name}:\n  {BC.CYAN}{inv_elements}{BC.OFF}\n"
        for subelement in gc.subelements[0].limb_check("grasp"):
            if hasattr(subelement.grasped, "vis_inv"):
                inv_elements = '\n  '.join([x.name for x in subelement.grasped.vis_inv])
                inventory = inventory + f"{subelement.grasped.name}:\n  {BC.CYAN}{inv_elements}{BC.OFF}\n"

        if gc.limb_count("see") >= 1:
            cs = f"\n{C.RED}Character Sheet{C.OFF}\n" \
                 f"Name: {BC.YELLOW}{gc.name}{BC.OFF}\n" \
                 f"\n{C.RED}Weapons{C.OFF}\n" \
                 f"{''.join(weapons)}" \
                 f"\n{C.RED}Inventories{C.OFF}\n" \
                 f"{inventory}\n" \
                 f"{self.game.char.desc(stats=True)}"
            self.display_long_text(cs)

    def examine(self):
        """Desc for a particular creature or element in the room."""
        # Sight check
        if self.game.char.limb_count("see") >= 1:
            examine_dict = self.listtodict(self.game.char.location.creatures + self.game.char.location.elements, add_x=True)
            self.dictprint(examine_dict)
            i = input(f"{BC.GREEN}\nWho/what are you examining?{BC.OFF}")
            if i in examine_dict.keys() and i != "x":
                self.display_long_text(examine_dict[i].desc(full=True))
            else:
                print(f"{BC.CYAN}You look away.{BC.OFF}")
        else:
            print(f"{C.RED}You cannot see well enough to examine anything closely.{C.OFF}")

    def inventory(self):
        """Transfer items between the character's inventory and another object."""
        # Sight check
        if self.game.char.limb_count("see") >= 1:
            # gather vis_invs in room (not all elements)
            # room_inventories = [elem for elem in self.game.char.location.elements if hasattr(elem, "vis_inv")]
            room_inventories = self.game.char.location.find_invs()
            your_inventories = self.game.char.subelements[0].find_invs()
            all_inventories = your_inventories + room_inventories
            inventory_dict = self.listtodict(all_inventories)
            inventory_dict["x"] = "look away"
            def pfunc(str, invobj):
                ex_str = ""
                if hasattr(invobj, "vis_inv") and invobj.vis_inv:
                    ex_str += f" ("+ ", ".join([x.name for x in invobj.vis_inv]) +")"
                if hasattr(invobj, "equipment") and invobj.equipment:
                    ex_str += f" ({', '.join([x.name for x in invobj.equipment])})"
                # if hasattr(invobj, "grasped") and invobj.grasped:
                #     ex_str += f" ({invobj.grasped.name})"
                return str + ex_str
            self.dictprint(inventory_dict, pfunc=pfunc)

            i = input(f"\n{BC.GREEN}First, which inventory would you like to take from (x to cancel)?{BC.OFF} ")
            if i != "x" and i in inventory_dict.keys():
                origin_inv = inventory_dict[i]
                if hasattr(origin_inv, "vis_inv"):
                    origin_inv = origin_inv.vis_inv
                elif hasattr(origin_inv, "equipment"):
                    origin_inv = origin_inv.equipment
                del inventory_dict[i]

                j = input(f"\n{BC.GREEN}Second, which inventory would like to transfer to (x to cancel)?{BC.OFF} ")
                if j != "x" and j in inventory_dict.keys():
                    target_inv = inventory_dict[j]
                    if hasattr(target_inv, "vis_inv"):
                        target_inv = target_inv.vis_inv
                    elif hasattr(target_inv, "equipment"):
                        target_inv = target_inv.equipment
                    self.dictprint(self.listtodict(origin_inv))
                    k = input(f"\n{BC.GREEN}Which item would you like to transfer (x to cancel)?{BC.OFF} ")
                    if k != "x" and 0 <= int(k) < len(origin_inv):
                        # TODO why does this fail twice when it fails?
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
        if self.game.char.limb_count("see") >= 1:
            self.game.current_level.printMap(self.game.char)
        else:
            print("You cannot see well enough to read the map.")

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

        return self.check_safety()

    # Combat
    # TODO-DONE ai should defend things like eyes. Maybe always block if possible? Needs decent chance of failing to block (then bring back shields) (50%?).
    # TODO-DONE should not be able to attack without vision
    def attack(self):
        self.combat.fullCombat()

    def check_safety(self):
        """Checks whether the current room is safe."""
        for creature in self.game.char.location.creatures:
            if creature.aggressive and (creature.team != self.game.char.team) and (self.game.char.team != "neutral") and (creature.team != "neutral"):
                return False
        return True

    def pick_target(self):
        # TODO-DONE chopping off thumbs is too easy now. Smaller targets should be harder to hit?
        enemylist = self.game.char.ai.get_target_creatures()
        targets = self.listtodict(enemylist)
        targets["x"] = "Withhold your blow."

        self.dictprint(targets)

        i = input(f"{BC.GREEN}\nWho are you attacking {C.YELLOW}(x for none){BC.GREEN}?{BC.OFF} ")

        if i != "x" and i in targets.keys():
            defender = targets[i]
            print(f"{C.RED}{self.game.char.name}{C.OFF} aims at {C.YELLOW}{defender.name}{C.OFF}!")
        else:
            defender = False
            # print(f"{C.RED}{self.game.char.name}{C.OFF} withholds their blow.")

        return defender

    def pick_weapon(self, weapons):
        weapons = self.listtodict(weapons)
        # self.dictprint(weapons, pfunc=lambda x, y: x + f" {C.BLUE}({y.damage[1].name} {y.damage[0]}){C.OFF}" if y != "Cancel" else x)
        self.dictprint(weapons, pfunc=lambda x, y: x + f" {C.BLUE}({y.damage[1].name}) {C.RED}({y.damage[0]}){C.OFF}")

        i = None
        while i not in weapons.keys():
            i = input(f"{BC.GREEN}Pick a weapon:{BC.OFF} ")
            if i in weapons.keys():
                weapon = weapons[i]
            else:
                print(f"{C.RED}{i} is not a recognized weapon! You must pick a weapon.{C.OFF}")
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
            if hasattr(obj, "size"):
                str = f"{str} {C.YELLOW}({obj.size}){C.OFF}"
            return str
        self.dictprint(limbs, pfunc=a_pfunc)

        i = input(f"\n{BC.GREEN}Which limb are you targeting {C.YELLOW}(x for none){C.OFF}{BC.GREEN}? {BC.OFF}")

        if i != "x" and i in limbs.keys():
            limb = limbs[i]
        else:
            limb = False

        return limb

    def pick_blocker(self, blockers):
        if self.game.char.limb_count("see") >= 1:
            blockers = self.listtodict(blockers)
            blockers["x"] = "Accept the blow."

            def a_pfunc(str, obj):
                if hasattr(obj, "armor"):
                    str = f"{str} {C.BLUE}({obj.armor}){C.OFF}"
                if hasattr(obj, "hp"):
                    str = f"{str} {C.RED}({obj.hp}){C.OFF}"
                return str

            self.dictprint(blockers, pfunc=a_pfunc)

            i = input(f"\n{BC.GREEN}Which {BC.CYAN}limb{BC.GREEN} would you like to block with {C.YELLOW}(x for none){BC.GREEN}?{C.OFF} ")

            if i != "x" and i in blockers.keys():
                blocker = blockers[i]
            else:
                blocker = False
        else:
            print(f"{C.RED}{self.game.char.name} cannot see well enough to block!{C.OFF}")
            blocker = False

        return blocker

    # TODO resting should not restore hp, or only a limited amount. Add healing potions and misses.
    def rest(self):
        print(f"{C.RED}{self.game.char.name}{C.OFF} rests for one hour.")
        for limb in self.game.char.subelements[0].limb_check(tag="hp"):
            if limb.hp < limb.base_hp:
                hp_diff = 1 if (limb.base_hp - limb.hp >= 1) else (limb.base_hp - limb.hp)
                limb.hp += hp_diff
                print(f"{C.RED}{self.game.char.name}{C.OFF}'s {BC.RED}{limb.name}{BC.OFF} heals a little {BC.RED}({limb.hp}/{limb.base_hp}){BC.OFF}.")

    def eat(self):
        invs = self.game.char.subelements[0].find_invs()
        # Drop equipment
        invs = [inv for inv in invs if hasattr(inv, "vis_inv")]
        invs = self.listtodict(invs, add_x=True)
        self.dictprint(invs)
        i = input(f"\n{BC.GREEN}Which inventory would you like to eat from?{BC.OFF} ")

        if i in invs.keys() and i != "x":
            edibles = self.listtodict([item for item in invs[i].vis_inv if hasattr(item, "edible") and item.edible], add_x=True)
            self.dictprint(edibles)
            j = input(f"\n{BC.GREEN}Select an item to eat/drink:{BC.OFF} ")

            if j in edibles.keys() and j != "x":
                food = edibles[j]
                # print(f"{BC.CYAN}{self.game.char.name} consumes the {food.name}{BC.OFF}.")
                food.eat(self.game.char)
                invs[i].vis_inv.remove(food)

    def put_on(self):
        invs = self.listtodict(self.game.char.subelements[0].find_invs(), add_x=True)
        self.dictprint(invs)
        i = input(f"\n{BC.GREEN}Which inventory would you like to equip from?{BC.OFF} ")

        if i in invs.keys() and i != "x":
            inventory = self.listtodict(invs[i].vis_inv, add_x=True)
            self.dictprint(inventory)
            j = input(f"\n{BC.GREEN}Select an item to equip:{BC.OFF} ")

            if j in inventory.keys() and j != "x":
                gear = inventory[j]
                limbs = self.listtodict(self.game.char.subelements[0].limb_check("name"), add_x=True)
                self.dictprint(limbs)
                k = input(f"\n{BC.GREEN}Select a limb to equip the {gear.name} on:{BC.OFF} ")

                if k in limbs.keys() and k != "x":
                    limb = limbs[k]
                    equipped = limb.equip(gear)
                    invs[i].vis_inv.remove(gear)
                    if equipped:
                        print(f"{BC.CYAN}{self.game.char.name} puts the {gear.name} on their {limb.name}.{BC.OFF}")

    def take_off(self):
        """Remove equipment from a limb."""
        limbs = self.listtodict(self.game.char.subelements[0].limb_check("name"), add_x=True)
        self.dictprint(limbs)
        i = input(f"\n{BC.GREEN}Which limb would you like to unequip from?{BC.OFF} ")

        if i in limbs.keys() and i != "x":
            limb = limbs[i]
            equipment = self.listtodict(limb.equipment, add_x=True)
            self.dictprint(equipment)
            j = input(f"\n{BC.GREEN}Select the gear you would like to remove:{BC.OFF} ")

            if j in equipment.keys() and j != "x":
                gear = equipment[j]
                invs = self.listtodict(self.game.char.subelements[0].find_invs(), add_x=True)
                self.dictprint(invs)
                k = input(f"\n{BC.GREEN}Select an inventory to put the gear into:{BC.OFF} ")

                if k in invs.keys() and k != "x":
                    target_inv = invs[k]
                    limb.equipment.remove(gear)
                    target_inv.vis_inv.append(gear)
                    print(f"{BC.CYAN}{self.game.char.name} removes the {gear.name} and places it in their {target_inv.name}.{BC.OFF}")

    def grasp(self):
        """Pick something up in your hand."""
        room_inventories = [elem for elem in self.game.char.location.elements if hasattr(elem, "vis_inv")]
        your_inventories = self.game.char.subelements[0].find_invs()
        all_inventories = your_inventories + room_inventories
        inventory_dict = self.listtodict(all_inventories, add_x=True)
        self.dictprint(inventory_dict)
        i = input(f"\n{BC.GREEN}Select an inventory to take something from:{BC.OFF} ")

        if i in inventory_dict.keys() and i != "x":
            target_inv = inventory_dict[i]
            inventory = self.listtodict(target_inv.vis_inv, add_x=True)
            self.dictprint(inventory)
            j = input(f"\n{BC.GREEN}Select an item to pick up:{BC.OFF} ")

            if j in inventory.keys() and j != "x":
                wielded = target_inv.vis_inv[int(j)]
                hands = self.listtodict(self.game.char.subelements[0].limb_check("grasp"), add_x=True)
                self.dictprint(hands)
                k = input(f"\n{BC.GREEN}Choose a hand to grasp the {wielded.name} with:{BC.OFF} ")

                if k in hands.keys() and k != "x":
                    hand = hands[k]
                    if hand.grasped:
                        print(f"{C.RED}{self.game.char.name}'s {hand.name} is already holding a {hand.grasped.name}!{C.OFF}")

                    # grasp check fails if no thumb or not enough fingers (or tentacly equivalent, whatever)
                    elif (sum([x.f_grasp for x in hand.limb_check("f_grasp")]) >= 1) and (sum([x.t_grasp for x in hand.limb_check("t_grasp")]) >= 1):
                        print(f"{BC.CYAN}{self.game.char.name} grasps the {wielded.name} in their {hand.name}.{BC.OFF}")
                        target_inv.vis_inv.remove(wielded)
                        hand.grasped = wielded
                    else:
                        print(f"{C.RED}The {wielded.name} slips out of {self.game.char.name}'s maimed {hand.name}!{C.OFF} ")
                        target_inv.vis_inv.remove(wielded)
                        room = self.game.char.get_location()
                        landings = room.elem_check("canCatch")
                        if len(landings) > 0:
                            lands_at = random.choice(landings)
                            lands_at.vis_inv.append(wielded)
                            print(f"{BC.CYAN}The {wielded.name} lands on the {lands_at.name}.{BC.OFF}")
                        else:
                            print(f"{BC.CYAN}The limb falls and disappears out of sight.{BC.OFF}")

    def ungrasp(self):
        graspers = self.game.char.subelements[0].limb_check("grasp")
        graspers_desc = self.listtodict([f"{g.name}: {BC.CYAN}{g.grasped.name}{BC.OFF}" for g in graspers if g.grasped])
        self.dictprint(graspers_desc)
        i = input(f"\n{BC.GREEN}Which hand would you like to empty?{BC.OFF}")

        if i in graspers_desc.keys() and i != "x":
            hand = graspers[int(i)]
            room_inventories = [elem for elem in self.game.char.location.elements if hasattr(elem, "vis_inv")]
            your_inventories = self.game.char.subelements[0].find_invs()
            all_inventories = your_inventories + room_inventories
            inventory_dict = self.listtodict(all_inventories, add_x=True)
            self.dictprint(inventory_dict)
            j = input(f"\n{BC.GREEN}Which inventory would you like to place the {hand.grasped.name} into?{BC.OFF} ")

            if j in inventory_dict.keys() and j != "x":
                # Transfer the item to target_inv.
                # We won't use the item.transfer() function because "who" is already grasping the item.
                target_inv = inventory_dict[j]
                print(f"{BC.CYAN}{self.game.char.name} places the {hand.grasped.name} into the {target_inv.name}.{BC.OFF} ")
                target_inv.vis_inv.append(hand.grasped)
                hand.grasped = None

