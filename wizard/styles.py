from engine.styles import LevelStyle, GameStyle, wall, floor

import assets.places

from wizard import human
import wizard.places

from colorist import BrightColor as BC, Color as C




# TODO-DONE put cat in apartment den.
# TODO add trophy room
# TODO-DONE add "dont let the cat out or the monsters in" welcome mat to foyer
class Home:
    level_text = f"""{BC.BLUE}You step into your home and a sense of warmth and security washes over you. Nothing very bad could ever happen to you here.{BC.OFF}"""
    room_classes = [wizard.places.PlayerBathroom, wizard.places.PlayerBedroom, wizard.places.TrophyRoom, assets.places.Parlor, assets.places.Kitchen]
    start_room = wizard.places.MagicFoyer
    end_room = assets.places.Den
    creature_classes = []

LevelStyle.register(Home)

class Cavern:
    level_text = f"""{BC.BLUE}The caves stretch before you, beckoning you on towards your first big adventure. You seek the burial chamber of the great dwarven king, Naarumsin, who lies deep underground somewhere beneath your feet. Legend has it that he was buried with an immense treasure, and his tomb has never been found. Many dangers lie before you, but fame and fortune will yours, if you can rise to the challenge. Into the depths!"""
    room_classes = [wizard.places.CavernOpen, wizard.places.CavernVillage, wizard.places.Tunnel]
    start_room = wizard.places.CavernEntrance
    end_room = wizard.places.GoblinChiefVillage
    creature_classes = []

LevelStyle.register(Cavern)

class Wizard:
    # levels will spawn in this order
    levelorder = [Cavern, Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""
    ------------------------
    |       {C.RED}The Tomb{C.OFF}       |
    |        {C.RED}of the{C.OFF}        |   
    |     {C.RED}Dwarven King{C.OFF}     |
    |                      |
    |  {C.BLUE}an {BC.CYAN}EverRogue{BC.OFF} {C.BLUE}game{C.OFF}   |
    |     by Markemus      |
    ------------------------
        """
    # This will display on game over
    death_splash = f"""
    ------------------------
    |       {C.RED}YOU DIED{C.OFF}       |
    ------------------------
        """
GameStyle.register(Wizard)

