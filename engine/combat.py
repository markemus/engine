import random

from colorist import BrightColor as BC, Color as C
from engine import item

class Combat:
    def __init__(self, char, cont):
        self.char = char
        self.cont = cont
        self.blockers = None

    def grab_weapon(self, actor):
        """AI creatures should grab weapons up off the floor if they have a spare hand."""
        # Search the room for weapons
        invs = actor.location.find_invs()
        for inv in invs:
            # isinstance is to stop enemies from wielding their own severed hands.
            weapons = [x for x in inv.vis_inv if isinstance(x, item.Item) and hasattr(x, "damage")]
            if weapons:
                weapon = max(weapons, key=lambda x: x.damage)
                graspHand = actor.grasp_check()
                if graspHand:
                    inv.vis_inv.remove(weapon)
                    graspHand.grasped = weapon
                    print(f"{BC.CYAN}{actor.name} grabs the {weapon.name} from the {inv.name}!")

    # TODO-DECIDE add enemies falling over (easier to-hit rolls)?
    def fullCombat(self, include_char=True):
        """Full combat round for all creatures."""
        creatures = self.char.location.get_creatures()
        # Neutral creatures will not attack (and will be ignored by combat ai, and not available to player)
        creatures = [creature for creature in creatures if creature.team != "neutral"]
        # if self.char.team == "neutral":
        #     print(f"{C.RED}{self.char.name}{C.OFF} remains neutral.")

        # Blockers must be reset each round.
        self.blockers = {}
        for actor in creatures:
            self.blockers[actor] = self.get_blockers(actor)

        # only one weapon per combat round
        for actor in creatures:
            if actor is self.char and not include_char:
                # Skip player round if for some reason they're not supposed to get one.
                continue
            if not actor.dead:
                # select best weapon
                if actor is not self.char:
                    # Check the room for a better weapon
                    self.grab_weapon(actor)

                weapons = self.get_weapons(actor)
                if weapons:
                    if actor is self.char:
                        weapon = self.cont.pick_weapon(weapons)
                    else:
                        # AI shouldn't favor one weapon if multiple are equal- makes for better gameplay.
                        random.shuffle(weapons)
                        weapon = max(weapons, key=lambda x: x.damage[0])

                    # Attack
                    used = self.combatRound(actor, weapon)
                    # # Can't block with weapons used to attack
                    # if used and (weapon in self.blockers[actor]):
                    #     self.blockers[actor].remove(weapon)
                else:
                    print(f"\n{C.RED}{actor.name}{C.OFF} has no weapons to attack with!")


    def combatRound(self, actor, weapon):
        """Single attack + defense + damage round."""
        used = False

        if actor is self.char:
            print(f"{C.RED}\nYou prepare to strike with your {weapon.name}.{C.OFF}")
            target = self.cont.pick_target()
        else:
            # Selects a nearby enemy at random
            target = actor.ai.target_creature()

        if target:
            if actor.limb_count("see") >= 1:
                if actor is self.char:
                    limb = self.cont.pick_limb(target)
                else:
                    limb = actor.ai.target_limb(target)
            else:
                # blind fighting
                print(f"\n{C.RED}{actor.name}{C.OFF} swings their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF} blindly!")
                limb = random.choice([x for x in target.subelements[0].limb_check("isSurface") if x.isSurface])
        else:
            limb = None

        if limb:
            if actor.limb_count("see") >= 1:
                print("") # we don't need the paragraph break if we already got one for blind fighting above.
            print(f"{C.RED}{actor.name}{C.OFF} attacks "
                  f"{BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} "
                  f"with their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF}!")
            print(f"It will deal up to {C.RED}{self.check_damage(weapon, limb)}{C.OFF} damage if not blocked ({C.RED}{limb.hp} hp{C.OFF}, {C.BLUE}{limb.armor} armor{C.OFF}).")

            # Blocking
            if target.limb_count("see") >= 1:
                blockers = self.blockers[target].copy()
                if target is self.char:
                    blocker = self.cont.pick_blocker(blockers)
                else:
                    blocker = actor.ai.block(blockers, limb)

                if blocker:
                    # 50/50 chance of blocking an attack
                    block_chance = random.randint(0, 1)
                    self.blockers[target].remove(blocker)
                    if block_chance:
                        limb = blocker
                        print(f"{BC.YELLOW}{target.name}{BC.OFF} blocks the blow with their {BC.CYAN}{blocker.name}{BC.OFF}!")
                    else:
                        print(f"{BC.YELLOW}{target.name}{BC.OFF} tries to block with {BC.CYAN}{blocker.name}{BC.OFF} but {C.RED}{actor.name}{C.OFF} blows through their defenses!")
                else:
                    print(f"{BC.YELLOW}{target.name}{BC.OFF} accepts the blow.")
            else:
                print(f"{BC.YELLOW}{target.name}{BC.OFF} cannot see the blow coming.")

            # To hit roll- smaller limbs are harder to hit
            if actor.limb_count("see") < 1:
                # Blind fighting
                roll = -3 + random.randint(0, 8) + limb.size
            elif target.limb_count("amble") < 1 and actor.limb_count("amble") >= 1:
                # easier to hit prone enemies
                print(f"{C.RED}{target.name} is prone!{C.OFF}")
                roll = 3 + random.randint(0, 2) + limb.size
            elif target.limb_count("amble") >= 1 and actor.limb_count("amble") < 1:
                print(f"{C.RED}{actor.name} is prone!{C.OFF}")
                roll = -3 + random.randint(0, 8) + limb.size
            else:
                roll = random.randint(0, 5) + limb.size

            if roll >= 5:
                limb = limb
                print(f"{C.RED}{actor.name}{C.OFF}'s attack is swift and sure.")
                self.attack(target, limb, weapon)
            elif roll >= 3:
                limb = random.choice(target.get_neighbors(limb))
                print(f"{C.RED}{actor.name}{C.OFF}'s attack misses narrowly and strikes {BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF}.")
                self.attack(target, limb, weapon)
            else:
                print(f"{C.RED}{actor.name}{C.OFF}'s attack misses!")
            used = True
        else:
            print(f"\n{C.RED}{actor.name}{C.OFF} withholds their blow.")

        return used

    def get_weapons(self, actor):
        """Any limb that can cause damage directly or wield a weapon."""
        claws = actor.subelements[0].limb_check("damage")
        hands = actor.subelements[0].limb_check("grasp")

        weapons = list(set(claws + hands))

        return weapons

    def check_damage(self, weapon, target):
        # No weapon
        if not weapon:
            return 0

        # Weapon damage
        try:
            damage = weapon.damage[0]
        except AttributeError:
            damage = 0

        # Adjust for armor
        if hasattr(target, "armor"):
            # damage = (damage - target.armor) if damage > target.armor else 0
            damage = (damage / target.armor)

        return round(damage, 2)

    def attack(self, defender, limb, weapon):
        damage = self.check_damage(weapon, limb)
        # Damage roll
        damage = round(random.random() * damage, 2)
        cutoff = False
        can_amble = defender.limb_count("amble") >= 1
        
        limb.hp -= damage
        print(f"It deals {C.RED}{damage}{C.OFF} damage!")

        if limb.hp <= 0:
            # core limb needs to be treated differently- it will drop when creature dies and we don't want to duplicate that.
            if limb is not defender.subelements[0]:
                defender.remove_limb(limb)
                print(f"The {BC.CYAN}{limb.name}{BC.OFF} is severed from {BC.YELLOW}{defender.name}{BC.OFF}'s body!")
                self.throw_limb(defender, limb)
                # check if target falls over
                if hasattr(limb, "amble") and can_amble:
                    if defender.limb_count("amble") < 1:
                        print(f"{C.RED}{defender.name} collapses to the ground!{C.OFF}")
            else:
                # Just remove the limb, the creature class will handle the rest.
                defender.remove_limb(limb)

            cutoff = True

        return cutoff

    def get_blockers(self, actor):
        """Any limb that can block damage directly."""
        blockers = [x for x in actor.subelements[0].limb_check("blocker") if x.blocker]
        return blockers

    def throw_limb(self, amputee, limb):
        """Arms have to land somewhere."""
        room = amputee.get_location()
        landings = room.elem_check("canCatch")
        
        if len(landings) > 0:
            lands_at = random.choice(landings)
            # Drop whatever it's holding
            hands = limb.limb_check("grasp")
            for hand in hands:
                if hand.grasped:
                    lands_at.vis_inv.append(hand.grasped)
                    print(f"{BC.CYAN}The {hand.grasped.name} slips from the {hand.name} and lands on the {lands_at.name}.{BC.OFF}")
                    hand.grasped = None
            # Limb lands
            lands_at.vis_inv.append(limb)
            print(f"{BC.CYAN}The {limb.name} lands on the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}The limb flies off and disappears out of sight.{BC.OFF}")
