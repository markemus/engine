from engine.styles import LevelStyle, GameStyle, wall, floor

import assets.places

from wizard import human
import wizard.places

from colorist import BrightColor as BC, Color as C


# TODO level 7- mechanical enemies and dragon boss (tomb of the dwarven king).
class Home:
    level_text = f"""{BC.BLUE}You step into your home and a sense of warmth and security washes over you. Nothing very bad could ever happen to you here.{BC.OFF}"""
    room_classes = [wizard.places.PlayerBathroom, wizard.places.PlayerBedroom, wizard.places.TrophyRoom, assets.places.Parlor, assets.places.Kitchen, wizard.places.Laboratory]
    start_room = wizard.places.MagicFoyer
    end_room = wizard.places.PlayerDen
    creature_classes = []


LevelStyle.register(Home)


class CavernL1:
    level_text = f"""{BC.BLUE}The caves stretch before you, beckoning you on towards your first big adventure. You seek the burial chamber of the great dwarven king, Naarumsin, which lies deep underground somewhere beneath your feet. Legend has it that he was buried with an immense treasure, and his tomb has never been found. Many dangers lie before you, but fame and fortune will be yours, if you can rise to the challenge. Into the depths!"""
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

# TODO add sharks! blind cave sharks
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


# TODO playtest necromancer level
class NecromancerL6:
    level_text = f"""{BC.BLUE}Behind the Great Goblin's throne there stands a great gateway, the ancient hinges nearly rusted shut. You push them apart with a deep creaking sound and press onwards into the ancient dwarven fortress of Zugalbash. But an ancient evil has taken root in these once homely halls, and you must face it if you are to win through to the tomb of Naarumsin.{BC.OFF}"""
    room_classes = [wizard.places.DwarvenHomeNecromancer, wizard.places.DwarvenWorkshopNecromancer]
    start_room = wizard.places.DwarvenEntranceHall
    end_room = wizard.places.DwarvenAleHallNecromancer
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(NecromancerL6)


class MountainhomeL7:
    level_text = f"""{BC.BLUE}You continue deeper into the dwarven mountain halls. The dwarves are long gone from here, but their mechanical creations still linger on in the halls around you. You can sense that you are drawing near to your goal. The treasure of Naarumsin will soon be yours- hurry now, and claim your destiny.{BC.OFF}"""
    room_classes = [wizard.places.DwarvenHomeL7, wizard.places.DwarvenPubL7]
    start_room = wizard.places.DwarvenStairway
    algorithm = "labyrinth"
    creature_classes = []


LevelStyle.register(MountainhomeL7)


class Wizard:
    # levels will spawn in this order
    levelorder = [CavernL1, CavernL2, DarkElfL3, LakeL4, GoblintownL5, NecromancerL6, MountainhomeL7, Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
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

