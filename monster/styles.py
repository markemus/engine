import monster.places

from engine.styles import LevelStyle, GameStyle, wall, floor

from colorist import BrightColor as BC, Color as C


class LabL1:
    level_text = f"""{BC.BLUE}You are a monster. Once you might have been human, but the experiments have turned you into something else entirely. Now however your chance for vengeance has arrived, and you will make them rue the day they kidnapped you from your peaceful home and turned you into this... thing.\n\nYou can never go back. You might as well become the monster they wanted you to be.{BC.OFF}"""
    room_classes = []
    start_room = monster.places.Laboratory
    end_room = monster.places.GuardRoom
    algorithm = "labyrinth"
    creature_classes = []

LevelStyle.register(LabL1)

class Monster:
    # levels will spawn in this order
    levelorder = [LabL1]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""
    ------------------------
    |       {C.RED}They Made{C.OFF}       |
    |          {C.RED}a{C.OFF}          |   
    |       {C.RED}Mistake{C.OFF}      |
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

GameStyle.register(Monster)
