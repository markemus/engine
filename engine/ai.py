import random


class CombatAI:
    def __init__(self, creature):
        self.creature = creature
        self.target = None

    def target_creature(self):
        targets = []

        if not self.target or self.target.dead:
            # Gather targets
            for creature in self.get_enemy_creatures():
                if creature.team and (creature.team != self.creature.team) and (creature.team != "neutral"):
                    targets.append(creature)

            # Pick
            if len(targets) > 0:
                # choice is random but persistent
                self.target = random.choice(targets)
            else:
                self.target = None

        return self.target

    def target_limb(self, target):
        best_weapon = None
        easiest_vital = None
        easiest_foot = None
        limbs = target.subelements[0].limb_check("isSurface")
        # print(limbs)
        weapons = [x for x in limbs if hasattr(x, "damage")]
        vitals = [x for x in limbs if (hasattr(x, "vital"))]
        feet = [x for x in limbs if (hasattr(x, "amble") or hasattr(x, "flight"))]

        # subelements[0] is always vital
        if target.subelements[0] not in vitals:
            vitals.append(target.subelements[0])

        # max and min return first if all are equal- we prefer a random one.
        random.shuffle(weapons)
        random.shuffle(vitals)
        random.shuffle(feet)

        # Assemble targets
        target_limbs = []

        if weapons:
            best_weapon = max(weapons, key=lambda x: x.damage[0])
            target_limbs.append(best_weapon)
        if vitals:
            easiest_vital = min(vitals, key=lambda x: x.armor * x.hp)
            target_limbs.append(easiest_vital)
        if feet:
            easiest_foot = min(feet, key=lambda x: x.armor * x.hp)
            # no point chopping off feet if target is already supine
            if target.limb_count("amble") >= 1:
                target_limbs.append(easiest_foot)

        if target_limbs:
            # This way enemies will switch targets instead of relentlessly hammering down the best target
            chosen = random.choice(target_limbs)
        else:
            # No weapons, no vitals, no feet, so attack a random limb
            chosen = random.choice(limbs)

        # Small chance AI will target a random limb (just to keep things fun and give a purpose for armor everywhere)
        if not random.randint(0, 5):
            # AI critical failure
            chosen = random.choice(limbs)

        return chosen

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
            # I disabled this check because it isn't obvious to the AI that it needs certain limbs (like fingers), so
            # it just blocks every attack now using its toughest blocker.
            # if limb_descendant_damage < current_damage:
            #     if len(target_limb.limb_check("vital")):
            #         pass
            #     else:
            #         blocker = False
        else:
            blocker = False

        return blocker

    def get_enemy_creatures(self):
        targets = self.creature.location.get_creatures()

        # Remove self
        if self.creature in targets:
            targets.remove(self.creature)
        # Remove friendly creatures
        targets = [c for c in targets if c.team != self.creature.team and c.team != "neutral"]

        return targets

    def get_friendly_creatures(self):
        targets = self.creature.location.get_creatures()

        # Remove unfriendly creatures
        targets = [c for c in targets if c.team == self.creature.team or c.team == "neutral"]

        return targets
