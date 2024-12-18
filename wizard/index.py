from assets import human, cat, places, suits

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
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        self.rounds = 10
        # Spell is created when it is cast
        self.cast()

    def cast(self):
        """Spells should define a cast effect."""
        pass

    def expire(self):
        """Spells should define an expire effect."""
        pass

    def update(self):
        """Spell will update every combat round."""
        self.rounds -= 1
        if self.rounds <= 0:
            self.expire()

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

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO spell tracking
# TODO spell casting from interface
# TODO player party
