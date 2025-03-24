import random

from engine import ai
from engine import effectsbook as eff


class TorturerAI(ai.CombatAI):
    """Focuses on cutting off small limbs and extending the fight."""
    def target_limb(self, target, attacking_weapon):
        limbs = target.subelements[0].limb_check("isSurface")
        target_limbs = limbs

        entanglements = [e for e in attacking_weapon.active_effects if isinstance(e, eff.Entangled)]
        if entanglements:
            target_limbs = self.target_entangling_limbs(target, attacking_weapon)

        if target_limbs:
            smallest_limb = min(target_limbs, key=lambda x: x.size)
            smallest_limbs = [x for x in target_limbs if x.size == smallest_limb.size]
            weakest_smallest = min(smallest_limbs, key=lambda x: (x.hp * x.armored))
            chosen = weakest_smallest

        else:
            chosen = random.choice(limbs)

        # Small chance AI will target a random limb (just to keep things fun and give a purpose for armor everywhere)
        if not random.randint(0, 5) and not entanglements:
            # AI critical failure
            chosen = random.choice(limbs)

        return chosen
