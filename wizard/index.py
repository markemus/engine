from assets import human, cat, giant_spider, places, suits

from engine.styles import LevelStyle, GameStyle
from engine import game, interface

from colorist import BrightColor as BC, Color as C


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "prisoner"
    suits = [suits.plainsuit]

class Home:
    level_text = f"""{BC.BLUE}You are in your home, preparing to set off on your adventure.{BC.OFF}"""
    room_classes = [places.Bathroom, places.Bedroom, places.Parlor, places.Kitchen]
    start_room = places.Den
    end_room = places.DiningRoom
    creature_classes = []

LevelStyle.register(Home)

class Wizard:
    # levels will spawn in this order
    levelorder = [Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""Wizard Game"""
    death_splash = f"""YOU DIED"""

GameStyle.register(Wizard)


# This should go into engine
class Spell:
    name = "spell"
    rounds = None
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        # Spell is created when it is cast
        self._cast()
        # TODO-DECIDE how should we track cast spells? game object?

    def _cast(self):
        """Spells should define a cast effect."""
        pass

    def expire(self):
        """Spells should define an expire effect if they need one."""
        pass

class Light(Spell):
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

class SummonSpider(Spell):
    name = "Summon Spider"
    description = "Summon an enemy spider."
    rounds = 1
    targets = "friendly"

    def _cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        spider = giant_spider.GiantSpider(location=self.target.location)
        self.target.location.creatures.append(spider)
        print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} pops into existence!{BC.OFF}")


# Main
# Generate a game using the Wizard template.
t_game = game.Game("The Path to Wizardry", Wizard)
thisLevel = t_game.level_list[0]

player = PlayerHuman(location=thisLevel.start)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
familiar = cat.Cat(location=thisLevel.start)
familiar.name = input(f"{BC.CYAN}Enter the name of your familiar: {BC.OFF}")
player.companions.append(familiar)
thisLevel.start.creatures.append(player)
thisLevel.start.creatures.append(familiar)
t_game.set_char(player)

# Character setup
player.spellbook.append(Light)
player.spellbook.append(SummonSpider)

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO-DONE spell tracking
# TODO-DONE spell casting from interface
# TODO-DONE player party
# TODO exchange equipment with party?
