import random

import engine.effectsbook as eff

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
        if (actor.limb_count("see") >= 1) and actor.limb_count("grasp"):
            invs = actor.location.find_invs()
            for inv in invs:
                # isinstance is to stop enemies from wielding their own severed hands.
                weapons = [x for x in inv.vis_inv if isinstance(x, item.Item) and hasattr(x, "damage")]
                if weapons:
                    weapon = max(weapons, key=lambda x: x.damage)
                    current_weapon = max(actor.limb_check("damage"), key=lambda x: x.damage[0])
                    if weapon.damage > current_weapon.damage[0]:
                        graspHand = actor.grasp_check()
                        if graspHand:
                            inv.vis_inv.remove(weapon)
                            graspHand.grasped = weapon
                            print(f"{BC.CYAN}{actor.name} grabs the {weapon.name} from the {inv.name}!")

    def fullCombat(self, include_char=True):
        """Full combat round for all creatures."""
        creatures = self.char.location.get_creatures()
        # Neutral creatures will not attack (and will be ignored by combat ai, and not available to player).
        # Non-aggressive creatures will not attack but can still be attacked.
        creatures = [creature for creature in creatures if (creature.team != "neutral")]
        random.shuffle(creatures)

        # Blockers must be reset each round.
        self.blockers = {}
        for actor in creatures:
            self.blockers[actor] = self.get_blockers(actor)

        # only one weapon per combat round
        for actor in creatures:
            if actor is self.char and not include_char:
                # Skip player round if for some reason they're not supposed to get one.
                continue
            if actor.aggressive and not actor.dead and not actor.afraid and not actor.stunned:
                # select best weapon
                if actor is not self.char:
                    # Check the room for a better weapon
                    self.grab_weapon(actor)

                weapons = self.get_weapons(actor)
                if weapons:
                    if actor is self.char:
                        weapon = self.cont.pick_weapon(weapons)
                    else:
                        weapon = actor.ai.pick_weapon(weapons)

                    # Attack
                    used = self.combatRound(actor, weapon)
                else:
                    print(f"\n{C.RED}{actor.name}{C.OFF} has no weapons to attack with!")


    def combatRound(self, actor, weapon):
        """Single attack + defense + damage round."""
        used = False

        if actor is self.char:
            print(f"{C.RED}\nYou prepare to strike with your {weapon.name}.{C.OFF}")
            target = self.cont.pick_target(weapon)
        else:
            # Selects a nearby enemy at random
            target = actor.ai.target_creature(weapon)

        if target:
            if actor.limb_count("see") >= 1:
                if actor is self.char:
                    limb = self.cont.pick_limb(target, weapon)
                else:
                    limb = actor.ai.target_limb(target, weapon)
            else:
                # blind fighting
                print(f"\n{C.RED}{actor.name}{C.OFF} attacks blindly with their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF}!")
                entanglements = [e for e in weapon.active_effects if isinstance(e, eff.Entangled)]
                if entanglements:
                     target_limbs = actor.ai.target_entangling_limbs(target, weapon)
                else:
                    target_limbs = [x for x in target.subelements[0].limb_check("isSurface") if x.isSurface]
                limb = random.choices(target_limbs, weights=[l.size for l in target_limbs], k=1)[0]
        else:
            limb = None

        if limb:
            if actor.limb_count("see") >= 1:
                print("") # we don't need the paragraph break if we already got one for blind fighting above.
            print(f"{C.RED}{actor.name}{C.OFF} attacks "
                  f"{BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} "
                  f"with their {BC.RED}{weapon.name}{BC.OFF} {C.BLUE}({weapon.damage[1].name}){C.OFF}!")
            print(f"It will deal up to {C.RED}{self.check_damage(weapon, actor, limb)}{C.OFF} damage if not blocked ({C.RED}{limb.hp} hp{C.OFF}, {C.BLUE}{limb.armored} armor{C.OFF}).")

            # Blocking
            is_entangled_together = sum([isinstance(x, eff.Entangled) and ((x.casting_limb is weapon) or (x.limb is weapon)) for x in limb.active_effects])
            if (target.limb_count("see") >= 1) and not target.stunned and not is_entangled_together:
                if weapon.damage[1].blockable:
                    blockers = self.blockers[target].copy()
                    # Can't block with webbed or entangled blocker
                    blockers = [b for b in blockers if not sum([isinstance(e, eff.Webbed) for e in b.active_effects]) and not sum([isinstance(e, eff.Entangled) for e in b.active_effects])]
                    # Confirm all blockers are still attached to the body
                    blockers = [b for b in blockers if target.subelements[0].is_subelement(b)]
                    if target is self.char:
                        blocker = self.cont.pick_blocker(blockers)
                    else:
                        blocker = actor.ai.block(blockers, limb)

                    if blocker and limb is not blocker:
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
            elif is_entangled_together:
                print(f"{BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} is entangled with {C.RED}{weapon.name}{C.OFF} and cannot be helped!")
            elif target.stunned:
                print(f"{BC.YELLOW}{target.name}{BC.OFF} is stunned and cannot stop the blow.")
            elif target.limb_count("see") < 1:
                print(f"{BC.YELLOW}{target.name}{BC.OFF} cannot see the blow coming.")

            # Masters have a higher to-hit roll
            mastery = actor.mastery
            if weapon.limb_count("mastery") > mastery:
                mastery = weapon.limb_count("mastery")
            if mastery > 1:
                print(f"{C.RED}{actor.name}{C.OFF}{BC.CYAN} aims shrewdly.{BC.OFF}")

            # To hit roll- smaller limbs are harder to hit
            if actor.limb_count("see") < 1:
                # Blind fighting
                roll = -3 + random.randint(0, 8) + limb.size + mastery
            elif ((target.limb_count("amble") < 1) and (target.limb_count("flight") < 1)) and ((actor.limb_count("amble") >= 1) or actor.limb_count("flight") >= 1):
                # easier to hit prone enemies
                print(f"{C.RED}{target.name} is prone!{C.OFF}")
                roll = 3 + random.randint(0, 2) + limb.size + mastery
            elif ((target.limb_count("amble") >= 1) or (target.limb_count("flight") >= 1)) and ((actor.limb_count("amble") < 1) and (actor.limb_count("flight") < 1)):
                print(f"{C.RED}{actor.name} is prone!{C.OFF}")
                roll = -3 + random.randint(0, 8) + limb.size + mastery
            else:
                roll = random.randint(0, 5) + limb.size + mastery

            # Add extra_vision effects to roll
            extra_vision = False
            for eye in actor.limb_check("see"):
                if eye.limb_check("extra_vision"):
                    extra_vision_effects = []
                    if hasattr(eye, "extra_vision"):
                        extra_vision_effects.extend(eye.extra_vision)
                    for equipment in eye.equipment:
                        if hasattr(equipment, "extra_vision"):
                            extra_vision_effects.extend(equipment.extra_vision)

                    for effect in extra_vision_effects:
                        if sum([isinstance(limb_effect, effect) for limb_effect in limb.active_effects]):
                            extra_vision = True

            if extra_vision:
                print(f"{C.RED}{target.name}'s {limb.name} is highlighted in {actor.name}'s vision!{C.OFF}")
                roll += 1

            if roll >= 5:
                limb = limb
                print(f"{C.RED}{actor.name}{C.OFF}'s attack is swift and sure.")
                self.attack(actor, target, limb, weapon)
            elif roll >= 3:
                limb = random.choice(target.get_neighbors(limb))
                print(f"{C.RED}{actor.name}{C.OFF}'s attack misses narrowly and strikes {BC.YELLOW}{target.name}{BC.OFF}'s {BC.CYAN}{limb.name}{BC.OFF}.")
                self.attack(actor, target, limb, weapon)
            else:
                print(f"{C.RED}{actor.name}{C.OFF}'s attack misses!")
            used = True
        else:
            print(f"\n{C.RED}{actor.name}{C.OFF} withholds their blow.")

        return used

    def get_weapons(self, actor, include_webbed=False):
        """Any limb that can cause damage directly or wield a weapon."""
        weapons = actor.subelements[0].limb_check("damage")

        unwebbed_weapons = []
        for weapon in weapons:
            if (not (hasattr(weapon, "webbed") and weapon.webbed)) or include_webbed:
                unwebbed_weapons.append(weapon)

        return unwebbed_weapons

    def check_damage(self, weapon, actor, target):
        # No weapon
        if not weapon:
            return 0

        # Weapon damage
        try:
            damage = weapon.damage[0]
        except AttributeError:
            damage = 0

        # Adjust for armor
        if hasattr(target, "armored"):
            # damage = (damage - target.armor) if damage > target.armor else 0
            damage = (damage / target.armored)

        # Adjust for strength.
        # This attribute on a parent limb can modify damage positively or negatively (troll vs hobbit eg).
        parent_strength = [p.strength for p in actor.get_parents(weapon) if hasattr(p, "strength")]
        if parent_strength:
            strength = max(parent_strength)
        else:
            strength = 1
        damage = damage * strength

        return round(damage, 2)

    def apply_damage(self, defender, limb, damage):
        cutoff = False
        can_amble = defender.limb_count("amble") >= 1
        can_fly = defender.limb_count("flight") >= 1

        limb.hp -= damage
        print(f"It deals {C.RED}{damage}{C.OFF} damage!")

        if limb.hp <= 0:
            # creature may already be dead, in which case we don't need to update defender regardless
            if defender.subelements:
                # core limb needs to be treated differently- it will drop when creature dies and we don't want to duplicate that.
                if limb is not defender.subelements[0]:
                    # limb may already be detached if damage is DOT
                    if defender.subelements[0].is_subelement(limb):
                        # Apply a bleed to the parent limb
                        parent_limb = defender.get_parents(limb)[-2]
                        defender.remove_limb(limb)
                        print(f"The {BC.CYAN}{limb.name}{BC.OFF} is severed from {BC.YELLOW}{defender.name}{BC.OFF}'s body!")
                        self.throw_limb(defender, limb)

                        if not defender.dead:
                            size = limb.size if not hasattr(limb, "orig_size") else limb.orig_size
                            bleed = eff.Bleed(casting_limb=limb, limb=parent_limb, controller=self.cont, amount=size * 2)
                            bleed.cast()

                        # check if target falls over
                        if not defender.dead:
                            if (limb.limb_count("amble") and can_amble) or (limb.limb_count("flight") and can_fly):
                                if (defender.limb_count("amble") < 1) and (defender.limb_count("flight") < 1):
                                    print(f"{C.RED}{defender.name} collapses to the ground!{C.OFF}")

                else:
                    # Just remove the core limb, the creature class will handle the rest.
                    defender.remove_limb(limb)

            cutoff = True

        return cutoff

    def apply_weapon_effects(self, defender, limb, weapon):
        """Applies weapon effects to the limb."""
        true_weapon = weapon.damage[1]
        effects = true_weapon.weapon_effects
        for Effect in effects:
            e = Effect(casting_limb=weapon, limb=limb, controller=self.cont)
            e.cast()

    def apply_impact_effects(self, defender, limb, weapon):
        """Applies impact effects to the attacking limb."""
        for Effect in limb.impact_effects:
            e = Effect(casting_limb=limb, limb=weapon, controller=self.cont)
            e.cast()

    def attack(self, actor, defender, limb, weapon):
        damage = self.check_damage(weapon, actor, limb)
        # Damage roll
        damage = round(random.random() * damage, 2)
        cutoff = self.apply_damage(defender, limb, damage)
        self.apply_weapon_effects(defender, limb, weapon)
        self.apply_impact_effects(defender, limb, weapon)

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
