"""A gamestyle is used to generate a game. This is the gamestyle for Escape From Castle Black.
This dark castle harbors many deadly creatures. But perhaps great treasure is hidden here?

A gamestyle is composed of levelstyles. Levelstyles are composed of rooms.

# Example levelstyle
class Dungeon:
    level_text = "This is the intro text to the level. It will be displayed when the level is first entered."
    # Rooms that will spawn on the level
    room_classes = [TortureChamber, Cell]
    # The level will begin with start_room and end with end_room, if they are provided. They are optional.
    start_room = PlayerCell
    end_room = Guardroom
    # These creatures can spawn anywhere in the level, except for start_room and end_room.
    # The numbers in the tuple are the chance that the creature will be spawned per room- converted to a percentage chance.
    # Here there is a 50% chance of goblin, 50% chance of nothing. Note that creature_classes is a nested list. Multiple sets can be defined and one creature will be chosen from each.
    creature_classes = [[(Goblin, 3), (None, 3)]]

# Example gamestyle
class Castle:
    # levels will be spawned in this order
    levelorder = [Dungeon, MainFloor, BedroomFloor, RoofTop]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1), (1, 2), (2, 3)]
    # the splash screens will display at the beginning and end of the game.
    start_splash = "Welcome to Castle Black"
    death_splash = "YOU DIED"

register() your styles to ensure that all the parameters are set.
"""
import engine.place as pl

from colorist import BrightColor as BC, Color as C

from castle.animated_armor import AnimatedArmor
from castle.cat import Cat
from castle.dog import Dog, Cerberus
from castle.dwarf import Dwarf, PrisonerDwarf
from castle.elf import Elf, PrisonerElf
from castle import furniture as fur
from castle.goblin import Goblin, ServantGoblin, GoblinCook
from castle.hobbit import Hobbit, PrisonerHobbit
from castle.human import Human, GuardHuman, PrisonerHuman, HumanKing
from castle.orc import Orc
from engine.styles import LevelStyle, GameStyle, wall, floor, pillar


# Creature classes with probability of spawning.
# Don't forget engine.styles.weight_list() to rebalance creature classes when merging sets.
cc = {
    "goblinkin": [(Orc, 3), (Goblin, 3), (None, 1)],
    "servants": [(ServantGoblin, 1)],
    "fantasy_city": [(Dwarf, 2), (Elf, 2), (Hobbit, 2), (Human, 2), (None, 3)],
    "fantasy_prisoners": [(PrisonerDwarf, 2), (PrisonerElf, 2), (PrisonerHuman, 2), (PrisonerHobbit, 2), (None, 3)],
    "castle": [(AnimatedArmor, 3), (None, 1)],
    "kitchen": [(ServantGoblin, 3), (None, 1)],
    "animals_indoor": [(Cat, 2), (Dog, 2), (None, 3)],
}

# Rooms
class Ballroom(pl.Place):
    name = "ballroom"
    # The sprite for this room- will display on the map.
    sprite = "B"
    # count = range for number of this room that will be generated per level.
    count = (0, 2)
    # Room color will be chosen from this list. Same for texture.
    colors = ["gold", "white", "silver"]
    textures = ["marble", "granite", "limestone"]
    # Creatures that can spawn in this room.
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"]]
    # Furniture that will spawn in this room.
    furniture_classes = []
    # The subelements that will spawn for this room.
    subelement_classes = [wall, floor]

class Bathroom(pl.Place):
    name = "bathroom"
    sprite = "W"
    count = (1, 3)
    colors = ["white", "blue", "black", "marble"]
    textures = ["tiled"]
    creature_classes = []
    furniture_classes = [fur.Toilet, fur.BathroomCabinet]
    subelement_classes = [wall, floor]

class Bedroom(pl.Place):
    name = "bedroom"
    sprite = "B"
    count = (2, 5)
    colors = ["blue", "brown", "egg white", "beige"]
    textures = ["painted", "wallpapered"]
    creature_classes = [cc["castle"], cc["goblinkin"]]
    furniture_classes = [fur.Bed, fur.Dresser]
    subelement_classes = [wall, floor]

class Cell(pl.Place):
    name = "cell"
    sprite = "C"
    count = (5, 10)
    colors = ["unpainted", "grimy", "grey"]
    textures = ["stone", "concrete"]
    creature_classes = [cc["fantasy_prisoners"]]
    furniture_classes = [fur.Manacles, fur.Puddle, fur.Toilet]
    subelement_classes = [wall, floor]

class PlayerCell(Cell):
    """Spawning room for player."""
    creature_classes = [[(Goblin, 1)]]
    # creature_classes = [[(ServantGoblin, 1)]]
    # creature_classes = [[(Cerberus, 1)]]
    # creature_classes = []
    furniture_classes = [fur.BedPrison]

class DiningRoom(pl.Place):
    name = "dining room"
    sprite = "D"
    count = (1, 3)
    colors = ["purple", "red", "gold", "silver"]
    textures = ["draped", "marble", "painted", "lit"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"], cc["servants"], cc["animals_indoor"]]
    furniture_classes = [fur.Carpet, fur.DiningTable, fur.DiningChair, fur.CabinetElegant]
    subelement_classes = [wall, floor]

class Guardroom(pl.Place):
    """Boss fight for Dungeon."""
    name = "guardroom"
    sprite = "G"
    count = (1, 2)
    colors = ["gray", "eggwhite"]
    textures = ["painted", "peeling"]
    creature_classes = [[(Cerberus, 1)]]
    furniture_classes = [fur.Table, fur.Chair]
    subelement_classes = [wall, floor]

class Kitchen(pl.Place):
    name = "kitchen"
    sprite = "K"
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted", "gray", "beige"]
    textures = ["brick", "stone"]
    # note both creatures will spawn, since they're in separate lists.
    creature_classes = [[(GoblinCook, 1)], [(Cat, 1)]]
    furniture_classes = [fur.Stove, fur.CabinetElegant, fur.KitchenCounter]
    subelement_classes = [wall, floor]

class Den(pl.Place):
    name = "den"
    sprite = "D"
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = [[(HumanKing, 1)], [(Dog, 1)]]
    furniture_classes = [fur.Table, fur.Chair, fur.Carpet, fur.CabinetMetal]
    subelement_classes = [wall, floor]

class Parlor(pl.Place):
    name = "parlor"
    sprite = "P"
    count = (1, 3)
    colors = ["blue", "white", "salmon", "gold", "silver"]
    textures = ["painted", "draped", "sunlit"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"], cc["fantasy_city"], cc["servants"], cc["animals_indoor"]]
    furniture_classes = [fur.Carpet, fur.Chair]
    subelement_classes = [wall, floor]

class Roof(pl.Place):
    name = "rooftop"
    sprite = "R"
    count = (1, 2)
    colors = ["dark"]
    textures = ["slate"]
    creature_classes = []
    furniture_classes = [fur.Chair]
    subelement_classes = [floor]

class ThroneRoom(pl.Place):
    """Boss fight for main floor."""
    name = "throne room"
    sprite = "T"
    colors = ["gold", "red", "silver", "purple"]
    textures = ["brick", "stone", "marble"]
    creature_classes = [[(AnimatedArmor, 1)], [(AnimatedArmor, 1)]]
    furniture_classes = [fur.Throne]
    subelement_classes = [wall, floor, pillar]

class TortureChamber(pl.Place):
    name = "torture chamber"
    sprite = "T"
    count = (1, 3)
    colors = ["black", "gray", "streaked", "dirty"]
    textures = ["stone", "dirt", "timber"]
    creature_classes = [cc["fantasy_prisoners"], [(Goblin, 1)]]
    furniture_classes = [fur.Manacles, fur.TableWork, fur.Rack, fur.CabinetMetal]
    subelement_classes = [wall, floor]


# Levels
class BedroomFloor:
    level_text = f"""{BC.BLUE}You've made it to the top floor of the castle. Time to finally confront your captor and put an end to this evil once and for all!{BC.OFF}"""
    # The level will be populated with these floors
    room_classes = [Bedroom, Bathroom]
    end_room = Den
    # These creatures can spawn anywhere in the level, except for start_room and end_room
    creature_classes = [[(Orc, 3), (None, 3)]]

LevelStyle.register(BedroomFloor)


class Dungeon:
    level_text = f"""{BC.BLUE}This is it then. The one who came for you says he only wants your arm... but you've heard enough screams down here to know that it's only the beginning. You've made your preparations... it's time to put an end to this abomination.\n\nHINT: The first thing you should do is drink your potion. Don't forget to loot! Good luck.{BC.OFF}"""
    room_classes = [TortureChamber, Cell]
    start_room = PlayerCell
    # start_room = Kitchen
    end_room = Guardroom
    creature_classes = [[(Goblin, 3), (None, 3)]]

LevelStyle.register(Dungeon)


class MainFloor:
    level_text = f"""{BC.BLUE}You escape up the stairs and out of the dungeon. But it looks like you might have gone out of the frying pan... and into the fire.{BC.OFF}"""
    room_classes = [DiningRoom, Parlor, Ballroom, Bathroom]
    start_room = Kitchen
    end_room = ThroneRoom
    creature_classes = [[(GuardHuman, 3)]]

LevelStyle.register(MainFloor)

class RoofTop:
    level_text = f"""{BC.BLUE}Exhausted from battle, you escape onto the rooftop. Above you, the stars are shining in a beautiful night sky. The evil king lies dead, and you will rule now... but will you rule benevolently, or recreate the evil you have seen here? Only time will tell.\n\nTHE END{BC.OFF}"""
    room_classes = []
    start_room = Roof
    creature_classes = []

LevelStyle.register(RoofTop)

# And finally, the game itself.
class Castle:
    # levels will spawn in this order
    levelorder = [Dungeon, MainFloor, BedroomFloor, RoofTop]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = [(0, 1), (1, 2), (2, 3)]
    # This will display when game starts
    start_splash = f"""
------------------------
|     {C.RED}Escape From{C.OFF}      |
|    {C.RED}Castle  Black{C.OFF}     |
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


GameStyle.register(Castle)
