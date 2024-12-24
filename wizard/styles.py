from engine.styles import LevelStyle, GameStyle, wall, floor

import assets.places

from wizard import human
import wizard.places

from colorist import BrightColor as BC, Color as C





# TODO add trophy room.
# TODO level 2- goblins and dark elf scouts fighting
# TODO level 3- dark elf home caverns (with spider-human hybrid creatures in secondary rooms)
class Home:
    level_text = f"""{BC.BLUE}You step into your home and a sense of warmth and security washes over you. Nothing very bad could ever happen to you here.{BC.OFF}"""
    room_classes = [wizard.places.PlayerBathroom, wizard.places.PlayerBedroom, wizard.places.TrophyRoom, assets.places.Parlor, assets.places.Kitchen]
    start_room = wizard.places.MagicFoyer
    end_room = assets.places.Den
    creature_classes = []

class CavernL1:
    level_text = f"""{BC.BLUE}The caves stretch before you, beckoning you on towards your first big adventure. You seek the burial chamber of the great dwarven king, Naarumsin, who lies deep underground somewhere beneath your feet. Legend has it that he was buried with an immense treasure, and his tomb has never been found. Many dangers lie before you, but fame and fortune will be yours, if you can rise to the challenge. Into the depths!"""
    room_classes = [wizard.places.CavernOpen, wizard.places.GoblinCavernVillage, wizard.places.Tunnel]
    start_room = wizard.places.CavernEntrance
    end_room = wizard.places.GoblinChiefVillage
    algorithm = "labyrinth"
    creature_classes = []

LevelStyle.register(CavernL1)

class CavernL2:
    level_text = f"""{BC.BLUE}The goblin chieftain defeated, you descend further into the caverns. Here the goblins and the dark elves battle for supremacy, dark elf raiding parties headed towards the surface and goblin raiders headed into the deep. You seem to have stumbled into the middle of an endless battle.{BC.OFF}"""
    room_classes = [wizard.places.CavernOpenL2, wizard.places.GoblinCavernVillageL2, wizard.places.DarkElfOutpost]
    start_room = wizard.places.CavernEntrance
    algorithm = "labyrinth"
    creature_classes = []

LevelStyle.register(CavernL2)

class Wizard:
    # levels will spawn in this order
    levelorder = [CavernL1, CavernL2, Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1)]
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

LevelStyle.register(Home)

