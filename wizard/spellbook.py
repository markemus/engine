import engine.spells as sp
import engine.utils as utils

import wizard.zombie as z

from assets import giant_spider

from colorist import BrightColor as BC, Color as C


class Light(sp.Spell):
    name = "Light"
    description = "A luminous glow that surrounds a creature, making it easier to hit."
    rounds = 10
    targets = "enemy"
    # TODO-DECIDE mana costs for spells?
    def _cast(self):
        self.original_colors = {}
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            self.original_colors[limb] = limb.color
            limb.color = f"luminous {limb.color}"
            limb.size += 1
        print(f"{BC.MAGENTA}A luminous glow surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size -= 1
        print(f"{BC.MAGENTA}The glow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

class SummonSpider(sp.Spell):
    name = "Summon Spider"
    description = "Summon an enemy spider."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        spider = giant_spider.GiantSpider(location=self.target.location)
        self.target.location.creatures.append(spider)
        print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} pops into existence!{BC.OFF}")

class ReanimateLimb(sp.Spell):
    name = "Reanimate Limb"
    description = "Reanimate a zombie."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """Bring a limb in the room back to life."""
        if self.caster.humanity <= 1:
            invs = self.caster.location.find_invs()
            # Drop equipment
            invs = utils.listtodict(invs, add_x=True)
            utils.dictprint(invs)
            i = input(f"\n{BC.GREEN}Which inventory would you like to resurrect from?{BC.OFF} ")

            if i in invs.keys() and i != "x":
                limbs = utils.listtodict([item for item in invs[i].vis_inv if isinstance(item, cr.Limb)], add_x=True)
                utils.dictprint(limbs)
                j = input(f"\n{BC.GREEN}Select a limb to resurrect:{BC.OFF} ")

                if j in limbs.keys() and j != "x":
                    limb = limbs[j]
                    zombie = z.Zombie(limb=limb, location=self.caster.location)
                    zombie.team = self.caster.team
                    self.caster.location.addCreature(zombie)
                    self.caster.companions.append(zombie)
                    print(f"{C.RED}{zombie.name}{BC.MAGENTA} rises from the dead with a moan!{BC.OFF}")
