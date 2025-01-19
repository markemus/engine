import random

import engine.spells as sp
import autobattler.golem

from assets.dwarf import Dwarf
from assets.hobbit import Hobbit
from assets.human import Human
from assets.elf import Elf
from assets.goblin import ServantGoblin

from colorist import BrightColor as BC, Color as C


class Commencement(sp.Effect):
    rounds = 1
    def _cast(self):
        print(f"{BC.MAGENTA}Welcome back to the arena! We have an exciting show lined up for you today.{BC.OFF}")
        owner, golem = autobattler.golem.generate_golem_l0(self.casting_limb.creature.location)
        print(f"{BC.MAGENTA}We are about to witness a fight between {owner.name}'s golem {golem.name} and {self.cont.game.char.name}'s golem {self.cont.game.char.golem.name}. Who's ready for a show?{BC.OFF}")
        print(f"{BC.MAGENTA}The match will begin when you are both ready.{BC.OFF}")


gamesmaster_race = random.choice([Dwarf, Hobbit, Human, Elf, ServantGoblin])

class Gamesmaster(gamesmaster_race):
    team = "neutral"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subelements[0].passive_effects.append(Commencement)
