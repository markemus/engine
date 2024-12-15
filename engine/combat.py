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
            # TODO-DONE allow player to select their own weapon
            weapons = self.get_weapons(actor)
            if weapons:
                if actor is self.char:
                    weapon = self.cont.pick_weapon(weapons)
                else:
                    weapon = max(weapons, key=lambda x: x.damage[0])

                # Attack
                used = self.combatRound(actor, weapon)
                # Can't block with weapons used to attack
                if used and (weapon in self.blockers[actor]):
                    self.blockers[actor].remove(weapon)
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
            if actor is self.char:
                limb = self.cont.pick_limb(target)
            else:
                limb = actor.ai.target_limb(target)
        else:
            limb = None

        if limb:
            # TODO allow near misses (should hit neighboring limb on the pick_limb() list. Or neighboring on the tree would be better)
            # TODO target color should change based on relationship to player (or team). Aggressor too.
            # TODO don't allow player to target allies
            print(f"\n{C.RED}{actor.name}{C.OFF} attacks "
                  f"{C.YELLOW}{target.name}{C.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} "
                  f"with their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF}!")
            print(f"It will deal {C.RED}{self.check_damage(weapon, limb)}{C.OFF} damage if not blocked.")

            # Blocking
            blockers = self.blockers[target].copy()
            if target is self.char:
                blocker = self.cont.pick_blocker(blockers)
            else:
                blocker = actor.ai.block(blockers)

            if blocker:
                limb = blocker
                self.blockers[target].remove(blocker)
                print(f"{C.YELLOW}{target.name}{C.OFF} blocks the blow with their {BC.RED}{blocker.name}{BC.OFF}!")
            else:
                print(f"{C.YELLOW}{target.name}{C.OFF} accepts the blow.")
            
            self.attack(target, limb, weapon)
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
        cutoff = False
        
        limb.hp -= damage
        print(f"It deals {C.RED}{damage}{C.OFF} damage!")

        if limb.hp <= 0:
            defender.remove_limb(limb)
            print(f"The {BC.CYAN}{limb.name}{BC.OFF} is severed from {C.RED}{defender.name}{C.OFF}'s body!")
            
            self.throw_limb(defender, limb)

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
            lands_at.vis_inv.append(limb)
            print(f"{BC.CYAN}The {limb.name} lands on the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}The limb flies off and disappears out of sight.{BC.OFF}")
