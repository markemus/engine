import monster.places
import monster.minotaur

from engine.styles import LevelStyle, GameStyle, wall, floor

from colorist import BrightColor as BC, Color as C


class LabL1:
    level_text = f"""{BC.BLUE}You are a monster. Once you were human, but the experiments have turned you into something else entirely. Now your chance for vengeance has arrived, and you will make them rue the day they kidnapped you from your peaceful home and turned you into this... thing.\n\nYou can never go back. You might as well become the monster they wanted you to be.\n\n(TIP: You can use your spellbook to graft enemy's limbs onto your character.){BC.OFF}"""
    room_classes = [monster.places.Laboratory, monster.places.Cell]
    start_room = monster.places.StarterLaboratory
    end_room = monster.places.GuardRoom
    algorithm = "labyrinth"
    creature_classes = []

LevelStyle.register(LabL1)

class MazeL2:
    level_text = f"""{BC.BLUE}You've escaped from the lab, but you find yourself trapped in an endless maze. Something strange is going on here...{BC.OFF}"""
    room_classes = [monster.places.MazeHallway, monster.places.MazeTreasure]
    start_room = monster.places.MazeEntrance
    end_room = monster.places.MazeHallway
    algorithm = "labyrinth"
    creature_classes = [monster.minotaur.Minotaur]

LevelStyle.register(MazeL2)

class Monster:
    # levels will spawn in this order
    levelorder = [LabL1, MazeL2]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1)]
    start_splash = f"""
    ------------------------
    |       {C.RED}They Made{C.OFF}      |
    |          {C.RED} A{C.OFF}          |   
    |        {C.RED}Mistake{C.OFF}       |
    |                      |
    |   {C.BLUE}an {BC.CYAN}EverRogue{BC.OFF} {C.BLUE}game{C.OFF}  |
    |      by Markemus     |
    ------------------------
        """
    # This will display on game over
    death_splash = f"""
    ------------------------
    |       {C.RED}YOU DIED{C.OFF}       |
    ------------------------
        """

GameStyle.register(Monster)
