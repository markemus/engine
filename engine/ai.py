import random


# TODO-DECIDE multiple ai types? Styles?
class CombatAI:
    def __init__(self, creature):
        self.creature = creature
        self.target = None

    def target_creature(self):
        targets = []

        if not self.target or self.target.dead:
            # Gather targets
            for creature in self.get_target_creatures():
                if creature.team and (creature.team != self.creature.team) and (creature.team != "neutral"):
                    targets.append(creature)

            # Pick
            if len(targets) > 0:
                # choice is random but persistent
                self.target = random.choice(targets)
            else:
                self.target = None

        return self.target

    # TODO add minor chance a random limb will be targeted.
    def target_limb(self, target):
        best_weapon = None
        easiest_vital = None
        limbs = target.subelements[0].limb_check("isSurface")
        weapons = [x for x in limbs if hasattr(x, "damage")]
        vitals = [x for x in limbs if (hasattr(x, "vital"))]

        if weapons:
            best_weapon = max(weapons, key=lambda x: x.damage[0])
        if vitals:
            easiest_vital = min(vitals, key=lambda x: x.armor * x.hp)

        if best_weapon and not easiest_vital:
            chosen = best_weapon
        elif easiest_vital and not best_weapon:
            chosen = easiest_vital
        elif best_weapon and easiest_vital:
            # This way enemies will switch targets instead of relentlessly hammering down the best target
            chosen = random.choice([best_weapon, easiest_vital])
        elif limbs:
            # No weapons, no vitals, so attack a random limb
            chosen = random.choice(limbs)
        else:
            chosen = False

        return chosen

    # TODO-DONE ai should pick a smart blocking limb (most hp*armor? least damage?)
    # TODO-DONE select_blockers(self)
    # TODO I think we can still do better on the blocking decision making.
    def block(self, blockers, target_limb):
        """Calculates a block value. The algorithm tries to minimize damage taken while maximizing damage potential."""
        if len(blockers) > 0:
            blocker = blockers[0]
            current_block_value = -float("inf")
            current_damage = 0

            # Find target limb's descendant damage
            target_descendant_damagers = target_limb.limb_check("damage")
            if target_descendant_damagers:
                limb_descendant_damage = max(target_descendant_damagers, key=lambda x: x.damage[0]).damage[0]
            else:
                limb_descendant_damage = 0

            for limb in blockers:
                descendant_damagers = limb.limb_check("damage")
                block_value = (limb.armor * limb.hp)
                if descendant_damagers:
                    descendant_damage = max(descendant_damagers, key=lambda x: x.damage[0]).damage[0]
                    block_value -= descendant_damage
                else:
                    descendant_damage = 0
                if block_value > current_block_value:
                    blocker = limb
                    current_block_value = block_value
                    current_damage = descendant_damage

            # Decide whether to block with blocker. We will still block if target_limb is vital, otherwise, tank the hit.
            if limb_descendant_damage < current_damage:
                if len(target_limb.limb_check("vital")):
                    pass
                else:
                    blocker = False
        else:
            blocker = False

        return blocker

    def get_target_creatures(self):
        targets = self.creature.location.get_creatures()

        # Remove self
        if self.creature in targets:
            targets.remove(self.creature)
        # Remove friendly creatures
        targets = [c for c in targets if c.team != self.creature.team and c.team != "neutral"]

        return targets
