import random

from colorist import BrightColor as BC, Color as C
from transitions import Machine

#TODO replace with FSM, maybe?
class Combat:
    def __init__(self, char, cont):
        self.char = char
        self.cont = cont
        # TODO combatAI should be attached to each creature instead, and should be included in styles.
        # self.ai = CombatAI()
        self.blockers = None

    def fullCombat(self):
        """Full combat round for all creatures."""
        creatures = self.char.location.get_creatures()
        # Blockers must be reset each round.
        # TODO fix bug where blockers can be used to attack if block happens before attack.
        self.blockers = {}
        # print("fullCombat: creatures: ", creatures)

        for actor in creatures:
            # self.blockers[actor] = self.get_weapons(actor)
            self.blockers[actor] = self.get_blockers(actor)
            # print("fullCombat: blockers: ", self.blockers)

        # TODO only one weapon per combat round, blockers should be a separate list.
        for actor in creatures:
            # select best weapon
            weapons = self.get_weapons(actor)
            weapon = max(weapons, key=lambda x: x.damage)

            # for weapon in self.get_weapons(actor):
            used = self.combatRound(actor, weapon)
            # Can't block with weapons used to attack
            if used:
                # TODO this raised an exception: ValueError: list.remove(x): x not in list
                self.blockers[actor].remove(weapon)

        print("fullCombat: blockers: ", self.blockers)

    # TODO self.char can be replaced with a custom combatAI that calls controller methods
    def combatRound(self, actor, weapon):
        """Single attack + defense + damage round."""
        used = False

        if actor is self.char:
            print("\nYou prepare to strike with your " + weapon.name + ".")
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
            # TODO should print weapon name, not hand-holding-weapon's name. Get max damage?
            # TODO target color should change based on relationship to player. Aggressor too.
            print(f"{C.RED}{actor.name}{C.OFF} attacks "
                  f"{C.YELLOW}{target.name}{C.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} "
                  f"with their {BC.RED}{weapon.name}{BC.OFF}!")
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
                print(target.name, "blocks the blow with their", blocker.name + "!")
            
            self.attack(target, limb, weapon)
            
            used = True

        return used

    # TODO blockers should not be the same list as weapons! Blockers should be isSurface instead.
    def get_weapons(self, actor):
        """Any limb that can cause damage directly or wield a weapon."""
        claws = actor.subelements[0].limb_check("damage")
        hands = actor.subelements[0].limb_check("grasp")

        weapons = list(set(claws + hands))
        # print("get_weapons: weapons: ", weapons)

        return weapons

    def check_damage(self, weapon, target):
        # No weapon
        if not weapon:
            return 0

        # Weapon damage
        try:
            damage = weapon.damage
        except AttributeError:
            damage = 0

        # Adjust for armor
        if hasattr(target, "armor"):
            damage = (damage - target.armor) if damage > target.armor else 0 

        return damage

    def attack(self, defender, limb, weapon):
        damage = self.check_damage(weapon, limb)
        cutoff = False
        
        limb.hitpoints -= damage
        print("It deals", damage, "damage!") 

        if limb.hitpoints <= 0:
            defender.remove_limb(limb)
            print(limb.name, "is severed from", defender.name + "'s body!")
            
            self.throw_limb(defender, limb)

            cutoff = True

        return cutoff

    def get_blockers(self, actor):
        """Any limb that can block damage directly."""
        blockers = actor.subelements[0].limb_check("isSurface")
        return blockers

    def throw_limb(self, amputee, limb):
        """Arms have to land somewhere."""
        room = amputee.get_location()
        landings = room.elem_check("canCatch")
        
        if len(landings) > 0:
            lands_at = random.choice(landings)
            lands_at.add_vis_item(limb)
            print("The", limb.name, "lands on the", lands_at.name + ".")
        else:
            print("The limb flies off and disappears out of sight.")


# class CombatAI:
#     def target_creature(self, actor):
#         targets = []
#
#         # Gather
#         for creature in get_target_creatures(actor):
#             if creature.team != actor.team:
#                 targets.append(creature)
#
#         # Pick
#         if len(targets) > 0:
#             target = random.choice(targets)
#         else:
#             target = False
#
#         return target
#
#     def target_limb(self, target):
#         limbs = target.subelements[0].limb_check("isSurface")
#
#         if len(limbs) > 0:
#             lowest = min(limbs, key=lambda x: x.hitpoints)
#             allLowest = [limb for limb in limbs if limb.hitpoints == lowest.hitpoints]
#             chosen = random.choice(allLowest)
#             # print("chosen: ", chosen)
#         else:
#             # print("No surface limbs.")
#             chosen = False
#
#         return chosen
#
#     def block(self, limb, blockers):
#         if len(blockers) > 0:
#             blocker = blockers[0]
#         else:
#             blocker = False
#
#         return blocker


# def get_target_creatures(actor):
#     targets = actor.location.get_creatures()
#
#     if actor in targets:
#         targets.remove(actor)
#
#     return targets

# def get_target_limbs(defender):
#     limbs = defender.subelements[0].limb_check("isSurface")
#
#     return limbs


# if __name__ == "__main__":
#     # pass
#     # import item
#     from orc import orc
#
#     o = orc("o", location=None)
#     c = Combat(None, None)
#     hand = o.grasp_check()
#     print(hand.damage)
#     print(hand.armor)
#
#     print(c.check_damage(hand, hand))
