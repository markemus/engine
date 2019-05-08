import random


class CombatAI:
    def __init__(self, creature):
        self.creature = creature

    def target_creature(self):
        targets = []

        # Gather
        for creature in self.get_target_creatures():
            if creature.team != self.creature.team:
                targets.append(creature)

        # Pick
        if len(targets) > 0:
            target = random.choice(targets)
        else:
            target = False

        return target

    def target_limb(self, target):
        limbs = target.subelements[0].limb_check("isSurface")

        if len(limbs) > 0:
            lowest = min(limbs, key=lambda x: x.hitpoints)
            allLowest = [limb for limb in limbs if limb.hitpoints == lowest.hitpoints]
            chosen = random.choice(allLowest)
            # print("chosen: ", chosen)
        else:
            # print("No surface limbs.")
            chosen = False

        return chosen

    # TODO limb not needed?
    # TODO select_blockers(self)
    def block(self, blockers):
        if len(blockers) > 0:
            blocker = blockers[0]
        else:
            blocker = False

        return blocker

    def get_target_creatures(self):
        targets = self.creature.location.get_creatures()

        if self.creature in targets:
            targets.remove(self.creature)

        return targets
