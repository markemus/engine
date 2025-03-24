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
        if self.cont.game.char.golem:
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}Welcome back to the arena! We have an exciting show lined up for you today.{BC.OFF}"')
            owner, golem = autobattler.golem.generate_golem_l0(self.limb.creature.location)
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}We are about to witness a fight between {owner.name}\'s golem {golem.name} and {self.cont.game.char.name}\'s golem {self.cont.game.char.golem.name}. Who\'s ready for a show?{BC.OFF}"')
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}The match will begin when you are both ready.{BC.OFF}"')
        else:
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}Here comes our combatant... but where is his golem? Please come back when you\'re ready to fight."')


class Victory(sp.Effect):
    rounds = "forever"

    def _cast(self):
        if self.cont.game.char.golem:
            self.opponent = [c for c in self.limb.creature.location.creatures if isinstance(c, autobattler.golem.Golem) and c.team == "opponent"][0]
            self.combatant = [c for c in self.limb.creature.location.creatures if isinstance(c, autobattler.golem.Golem) and c.team == "combatant"][0]
            return True
        else:
            return False

    def update(self):
        if self.opponent.dead:
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}Congratulations to {self.combatant.owner.name} on their victory! Please collect your winnings.{BC.OFF}"')
            self.cont.game.char.level += 1
            print(f"{BC.CYAN}{self.cont.game.char.name} has leveled up!{BC.OFF}")
            self.expire()

        elif self.combatant.dead:
            print(f'{BC.RED}{self.limb.creature.name}{BC.OFF}: "{BC.MAGENTA}Congratulations to {self.opponent.owner.name} on their victory! Please collect your winnings.{BC.OFF}"')
            self.expire()

gamesmaster_race = random.choice([Dwarf, Hobbit, Human, Elf, ServantGoblin])

class Gamesmaster(gamesmaster_race):
    team = "neutral"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subelements[0].passive_effects.append(Commencement)
        self.subelements[0].passive_effects.append(Victory)
