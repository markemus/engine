import random

from colorist import BrightColor as BC, Color as C
from transitions import Machine


class Combat:
    def __init__(self, char, cont):
        self.char = char
        self.cont = cont
        self.blockers = None

    def fullCombat(self):
        """Full combat round for all creatures."""
        creatures = self.char.location.get_creatures()
        # Neutral creatures will not attack (and will be ignored by combat ai, and not available to player)
        creatures = [creature for creature in creatures if creature.team != "neutral"]

        # Blockers must be reset each round.
        self.blockers = {}
        for actor in creatures:
            self.blockers[actor] = self.get_blockers(actor)

        # only one weapon per combat round
        for actor in creatures:
            # select best weapon
            weapons = self.get_weapons(actor)
            if weapons:
                if actor is self.char:
                    weapon = self.cont.pick_weapon(weapons)
                else:
                    weapon = max(weapons, key=lambda x: x.damage[0])

                # Attack
                used = self.combatRound(actor, weapon)
                # # Can't block with weapons used to attack
                # if used and (weapon in self.blockers[actor]):
                #     self.blockers[actor].remove(weapon)
            else:
                print(f"\n{C.RED}{actor.name}{C.OFF} has no weapons to attack with!")

    # TODO combat needs a vision check before each section (for attacker and defender).
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
            if actor is self.char:
                limb = self.cont.pick_limb(target)
            else:
                limb = actor.ai.target_limb(target)
        else:
            limb = None

        if limb:
            # TODO-DONE allow near misses (should hit neighboring limb on the pick_limb() list. Or neighboring on the tree would be better)
            print(f"\n{C.RED}{actor.name}{C.OFF} attacks "
                  f"{BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} "
                  f"with their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF}!")
            print(f"It will deal up to {C.RED}{self.check_damage(weapon, limb)}{C.OFF} damage if not blocked {C.RED}({limb.hp} hp){C.OFF}.")

            # Blocking
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
            # TODO-DONE damage rolls, to miss rolls (hit neighboring limb), blocking rolls. Right now it's too algorithmic.

            # TODO-DECIDE we need to do the math on this to-hit algorithm. Seems reasonable but might lead to strange results.
            # To hit roll
            roll = random.randint(0, 5) + limb.size
            if roll >= 6:
                limb = limb
                print(f"{C.RED}{actor.name}{C.OFF}'s attack is swift and sure.")
                self.attack(target, limb, weapon)
            elif roll >= 4:
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
        
        limb.hp -= damage
        print(f"It deals {C.RED}{damage}{C.OFF} damage!")

        if limb.hp <= 0:
            defender.remove_limb(limb)
            print(f"The {BC.CYAN}{limb.name}{BC.OFF} is severed from {C.RED}{defender.name}{C.OFF}'s body!")
            
            self.throw_limb(defender, limb)
            # TODO-DONE update defender status- drop weapon, fall over

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
                    # TODO refactor to use place.drop_item()
                    lands_at.vis_inv.append(hand.grasped)
                    print(f"{BC.CYAN}The {hand.grasped.name} slips from the {hand.name} and lands on the {lands_at.name}.{BC.OFF}")
                    hand.grasped = None
            # Limb lands
            lands_at.vis_inv.append(limb)
            print(f"{BC.CYAN}The {limb.name} lands on the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}The limb flies off and disappears out of sight.{BC.OFF}")
