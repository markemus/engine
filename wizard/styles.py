from engine.styles import LevelStyle, GameStyle, wall, floor

import assets.places

from wizard import human
import wizard.places

from colorist import BrightColor as BC, Color as C


class Home:
    level_text = f"""{BC.BLUE}You step into your home and a sense of warmth and security washes over you. Nothing very bad could ever happen to you here.{BC.OFF}"""
    room_classes = [wizard.places.PlayerBathroom, wizard.places.PlayerBedroom, wizard.places.TrophyRoom, assets.places.Parlor, assets.places.Kitchen, wizard.places.Laboratory]
    start_room = wizard.places.MagicFoyer
    end_room = wizard.places.PlayerDen
    creature_classes = []


LevelStyle.register(Home)


class CavernL1:
    level_text = f"""{BC.BLUE}The caves stretch before you, beckoning you on towards your first big adventure. You seek the burial chamber of the great dwarven king, Naarumsin, which lies deep underground somewhere beneath your feet. Legend has it that he was buried with an immense treasure, and his tomb has never been found. Many dangers lie before you, but fame and fortune will be yours, if you can rise to the challenge. Into the depths!{BC.OFF}"""
    room_classes = [wizard.places.CavernOpen, wizard.places.GoblinCavernVillage, wizard.places.Tunnel]
    start_room = wizard.places.CavernEntrance
    end_room = wizard.places.GoblinChiefVillage
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(CavernL1)


class CavernL2:
    level_text = f"""{BC.BLUE}The goblin chieftain defeated, you descend further into the caverns. Here the goblins and the dark elves battle for supremacy, dark elf raiding parties heading towards the surface and goblin raiders heading into the deep. You seem to have stumbled into the middle of an endless battle.{BC.OFF}"""
    room_classes = [wizard.places.CavernOpenL2, wizard.places.GoblinCavernVillageL2, wizard.places.DarkElfOutpost, wizard.places.CavernLake]
    start_room = wizard.places.CavernEntrance
    end_room = wizard.places.DarkElfGuardtower
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(CavernL2)


class DarkElfL3:
    level_text = f"""{BC.BLUE}You break into the guard tower and defeat the dark elf champion. Before you lies the gate of Albolobereth, a fortress of the dark elves built above the ruins of the old dwarven city. You will have to fight your way through if you want to reach the fabled hoard.{BC.OFF}"""
    room_classes = [wizard.places.DarkElfHollowedStalagmite, wizard.places.DarkElfWorkshop, wizard.places.ArachneNest]
    start_room = wizard.places.DarkElfEntrance
    end_room = wizard.places.QueensNest
    creature_classes = []


LevelStyle.register(DarkElfL3)


class LakeL4:
    level_text = f"""{BC.BLUE}Below the fortress of the dark elves you encounter a shallow lake. Mysterious colored lights flash in the distance as you wade out into the darkness. Whatever it is that is doing that, you hope you won't encounter them.{BC.OFF}"""
    room_classes = [wizard.places.LakeTile]
    start_room = wizard.places.LakeShore
    end_room = wizard.places.MirrorLake
    creature_classes = []


LevelStyle.register(LakeL4)


class GoblintownL5:
    level_text = f"""{BC.BLUE}You go through a mysterious gateway and leave the strange lake behind you. Ahead of you you hear strange sounds, hoots, howls, and drums, drums in the deep.{BC.OFF}"""
    room_classes = [wizard.places.GoblinTownShack, wizard.places.GoblinTownFirepit]
    start_room = wizard.places.GoblinTownGateway
    end_room = wizard.places.GreatGoblinsHall
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(GoblintownL5)


class NecromancerL6:
    level_text = f"""{BC.BLUE}Behind the Great Goblin's throne there stands a great gateway, the ancient hinges nearly rusted shut. You push them apart with a deep creaking sound and press onwards into the ancient dwarven fortress of Zugalbash. But an ancient evil has taken root in these once homely halls, and you must face it if you are to win through to the tomb of Naarumsin.{BC.OFF}"""
    room_classes = [wizard.places.DwarvenHomeNecromancer, wizard.places.DwarvenWorkshopNecromancer, wizard.places.DwarvenPubNecromancer]
    start_room = wizard.places.DwarvenEntranceHall
    end_room = wizard.places.DwarvenTempleNecromancer
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(NecromancerL6)


class TombL7:
    level_text = f"""{BC.BLUE}The necromancer defeated, you enter the ancient tomb of Naarumsin. The dwarves are long gone from this place, but their mechanical guardians still linger on in the halls around you. The treasure of Naarumsin will soon be yours- hurry now, and claim your destiny.{BC.OFF}"""
    room_classes = [wizard.places.GalleryL7, wizard.places.TreasureRoomL7]
    start_room = wizard.places.DwarvenStairway
    end_room = wizard.places.AntechamberL7
    creature_classes = []


LevelStyle.register(TombL7)


class InnerTombL8:
    level_text = f"""{BC.BLUE}The dragon is defeated and its hoard, the burial treasure of Naarumsin, is yours. Your epic adventure at last draws to a close, and you are looking forward to a quiet retirement. But perhaps other stories yet await you? The call of the road often reaches out to old burglars, and beckons them out of their peaceful homes and on to new adventures. Only time will tell.\n\nTHE END."""
    room_classes = []
    start_room = wizard.places.TombL8
    creature_classes = []

LevelStyle.register(InnerTombL8)


class Wizard:
    # levels will spawn in this order
    levelorder = [CavernL1, CavernL2, DarkElfL3, LakeL4, GoblintownL5, NecromancerL6, TombL7, InnerTombL8, Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
    start_splash = f"""
    ------------------------
    |       {C.RED}The Tomb{C.OFF}       |
    |          {C.RED}of{C.OFF}          |   
    |       {C.RED}Naarumsin{C.OFF}      |
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

