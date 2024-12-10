import random


# TODO-DECIDE multiple ai types? Styles?
class CombatAI:
    def __init__(self, creature):
        self.creature = creature

    def target_creature(self):
        targets = []

        # Gather
        # TODO should only target opposing teams
        for creature in self.get_target_creatures():
            if creature.team != self.creature.team:
                targets.append(creature)

        # Pick
        if len(targets) > 0:
            # TODO choice should be semi persistent
            target = random.choice(targets)
        else:
            target = False

        return target

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
        else:
            chosen = False

        return chosen

    # TODO limb not needed?
    # TODO select_blockers(self)
    def block(self, blockers):
        if len(blockers) > 0:
            # blocker = blockers[0]
            blocker = max(blockers, key=lambda x: x.armor)
        else:
            blocker = False

        return blocker

    def get_target_creatures(self):
        targets = self.creature.location.get_creatures()

        if self.creature in targets:
            targets.remove(self.creature)

        return targets
