"""An example style- from lowest to highest, build a hierarchy.

This dark castle harbors many deadly creatures. But perhaps great treasure is hidden here?"""
import engine.place as pl

from colorist import BrightColor as BC

from castle.animated_armor import AnimatedArmor
from castle.beholder import Beholder
from castle.cat import Cat
from castle.dog import Dog, Cerberus
from castle.dwarf import Dwarf, PrisonerDwarf
from castle.elf import Elf, PrisonerElf
from castle import furniture as fur
from castle.goblin import Goblin, ServantGoblin, GoblinCook
from castle.hobbit import Hobbit, PrisonerHobbit
from castle.human import Human, PrisonerHuman, HumanKing
from castle.orc import Orc
from engine.styles import LevelStyle, GameStyle, wall, floor, pillar


# Creature classes with probability of spawning.
# Don't forget engine.styles.weight_list() to rebalance creature classes when merging sets.
cc = {
    "goblinkin": [(Orc, 1), (Goblin, 3), (None, 3)],
    "servants": [(ServantGoblin, 1)],
    "fantasy_city": [(Dwarf, 2), (Elf, 2), (Hobbit, 2), (Human, 2), (None, 3)],
    "fantasy_prisoners": [(PrisonerDwarf, 2), (PrisonerElf, 2), (PrisonerHuman, 2), (PrisonerHobbit, 2), (None, 3)],
    "castle": [(AnimatedArmor, 3), (None, 1)],
    "kitchen": [(ServantGoblin, 3), (None, 1)],
    "animals_indoor": [(Cat, 2), (Dog, 2), (None, 3)],
    # "monsters": [(Beholder, 1), (None, 8)]
    # "animals_outdoor": [("Sheep", 5), ("Cow", 3), ("Horse", 1), (None, 3)]
}

# Rooms
class Ballroom(pl.Place):
    name = "ballroom"
    sprite = "D"
    count = (0, 2)
    colors = ["gold", "white", "silver"]
    textures = ["marble", "granite", "limestone"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class Bathroom(pl.Place):
    name = "bathroom"
    sprite = "T"
    count = (1, 3)
    colors = ["white", "blue", "black", "marble"]
    textures = ["tiled"]
    creature_classes = []
    furniture_classes = [fur.Toilet, fur.CabinetMetal]
    subelement_classes = [wall, floor]

class Bedroom(pl.Place):
    name = "bedroom"
    sprite = "B"
    count = (2, 5)
    colors = ["blue", "brown", "egg white", "beige"]
    textures = ["painted", "wallpapered"]
    creature_classes = [cc["fantasy_city"], cc["castle"]]
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

# TODO inventory redo- add pillowcase to PlayerCell and remove inventory from player. (can carry in left hand or third hand)
# TODO re-enable first combat
class PlayerCell(Cell):
    """Spawning room for player."""
    creature_classes = [[(Goblin, 1)]]
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
    furniture_classes = [fur.Carpet, fur.Table, fur.Chair, fur.CabinetElegant]
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
    creature_classes = [[(GoblinCook, 1)], [(Cat, 1)]]
    furniture_classes = [fur.Stove, fur.CabinetElegant]
    subelement_classes = [wall, floor]

class Den(pl.Place):
    name = "office"
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
    room_classes = [Bedroom, Bathroom]
    end_room = Den
    creature_classes = [[(Orc, 1), (Goblin, 1), (None, 3)]]

LevelStyle.register(BedroomFloor)


class Dungeon:
    level_text = f"""{BC.BLUE}This is it then. The one who came for you says he only wants your arm... but you've heard enough screams down here to know that it's only the beginning. You've made your preparations... it's time to put an end to this abomination.{BC.OFF}"""
    room_classes = [TortureChamber, Cell]
    start_room = PlayerCell
    end_room = Guardroom
    creature_classes = [[(Goblin, 3), (None, 3)]]

LevelStyle.register(Dungeon)


class MainFloor:
    level_text = f"""{BC.BLUE}You escape up the stairs and out of the dungeon. But it looks like you might have gone out of the frying pan... and into the fire.{BC.OFF}"""
    room_classes = [DiningRoom, Parlor, Ballroom, Bathroom]
    start_room = Kitchen
    end_room = ThroneRoom
    creature_classes = [[(Orc, 3), (None, 3)]]

LevelStyle.register(MainFloor)

class RoofTop:
    level_text = f"""{BC.BLUE}Exhausted from battle, you escape onto the rooftop. Above you, the stars are shining in a beautiful night sky. The evil king lies dead, and you will rule now... but will you rule benevolently, or recreate the evil you have seen here? Only time will tell.\n\nTHE END{BC.OFF}"""
    room_classes = []
    start_room = Roof

# And finally, the game itself.
class Castle:
    levelorder = [Dungeon, MainFloor, BedroomFloor, RoofTop]
    links = [(0, 1), (1, 2), (2, 3)]

# TODO-DECIDE why is registration necessary? Couldn't we just get rid of it?
GameStyle.register(Castle)

# TODO prisoners should be injured and "abominized" (extra limbs)
