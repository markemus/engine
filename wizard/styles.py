from engine.styles import LevelStyle, GameStyle, wall, floor

import assets.places

from wizard import human
import wizard.places

from colorist import BrightColor as BC, Color as C


class PlayerDen(assets.places.Den):
    subelement_classes = [wall, floor]

class HomeCell(assets.places.Cell):
    count = (1, 2)
    creature_classes = [[(human.SpecimenHuman, 1)]]

class Home:
    level_text = f"""{BC.BLUE}You are in your home, preparing to set off on your adventure.{BC.OFF}"""
    room_classes = [assets.places.Bathroom, assets.places.Bedroom, assets.places.Parlor, assets.places.Kitchen, assets.places.Den]
    start_room = wizard.places.MagicFoyer
    end_room = PlayerDen
    creature_classes = []

LevelStyle.register(Home)

class Wizard:
    # levels will spawn in this order
    levelorder = [Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""The Tomb of the Dwarven King"""
    death_splash = f"""YOU DIED"""

GameStyle.register(Wizard)

