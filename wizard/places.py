import copy

import assets.places
import engine.place as pl
from engine.styles import wall, single_wall, floor, water, mirrored_water, lakebed, pillar, door, channel, gateway, dwarven_gateway

import assets.furniture as fur

import wizard.furniture

from wizard.arachne import Arachne, ArachneQueen
from wizard.cave_fish import BlindCaveFish
from wizard.death_knight import DeathKnight
from wizard.dwarven_snatcher import DwarvenSnatcher
from wizard.dwarven_cleaner import DwarvenCleaner
from wizard.dwarven_scorpion import DwarvenScorpion
from wizard.dwarven_security import DwarvenSecuritySystem
from wizard.dwarven_tank import DwarvenTank
from wizard.dwarven_turret import DwarvenTurret
from wizard.elf import DarkElfScout, DarkElfChampion, DarkElfGuard, DarkElfSmith
from wizard.fairy import DarkElfFairy
from wizard.giant_rat import GiantRat
from wizard.giant_bat import GiantBat
from wizard.giant_mosquito import GiantMosquito
from wizard.giant_shrimp import BlindCaveShrimp
from wizard.giant_spider import GiantSpider, ArmoredGiantSpider
from wizard.goblin import ShallowGoblinChief, GoblinPetDog, GoblinPetOwlbear, GreatGoblin
from wizard.jellyfish import Jellyfish
from wizard.necromancer import Necromancer
from wizard.octopus import CaveOctopus
from wizard.tunnel_worm import TunnelWorm
from wizard.tentacle_monster import TentacleMonster
from wizard.troll import Troll
from wizard.uruk import Uruk
from wizard.warg import Warg
from wizard.zombie import MeldedRandomZombie, RandomZombie, RandomExplodingZombie

from assets.goblin import ShallowGoblin, DeepGoblin

from colorist import BrightColor as BC, Color as C

cc = {
    "caverns_1": [(GiantRat, 3), (GiantBat, 3), (ShallowGoblin, 4), (None, 2)],
    "caverns_1_gobs": [(ShallowGoblin, 4), (None, 1)],
    "caverns_2": [(GiantSpider, 1), (DarkElfScout, 4), (ShallowGoblin, 4), (None, 2)],
    "caverns_2_gobs": [(ShallowGoblin, 4), (None, 1)],
    "caverns_2_elves": [(GiantSpider, 1), (DarkElfScout, 4), (None, 1)],
    "fish": [(BlindCaveFish, 1), (BlindCaveShrimp, 1), (None, 1)],
    "tunnels": [(TunnelWorm, 1)],
    "de_fortress_guards": [(ArmoredGiantSpider, 1), (DarkElfGuard, 3), (DarkElfFairy, 1), (None, 1)],
    "lake_4_big_fish": [(TentacleMonster, 1), (CaveOctopus, 5), (None, 1)],
    "lake_4_small_fish": [(BlindCaveFish, 1), (BlindCaveShrimp, 1), (None, 1)],
    "lake_4_pests": [(GiantMosquito, 1), (Jellyfish, 1), (None, 1)],
    "goblintown": [(Troll, 2), (DeepGoblin, 3), (Uruk, 3), (Warg, 3), (None, 1)],
    "necromancer": [(RandomExplodingZombie, 2), (RandomZombie, 2), (MeldedRandomZombie, 2), (DeathKnight, 2), (None, 1)],
    "mountainhome": [(DwarvenSnatcher, 2), (DwarvenTurret, 2), (DwarvenTank, 1), (DwarvenScorpion, 2), (DwarvenCleaner, 1), (None, 1)],
    "mountainhome_security": [(DwarvenSecuritySystem, 1)],
}


# Player apartment
class MagicFoyer(pl.Place):
    name = "foyer"
    sprite = "F"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Carpet, wizard.furniture.Doormat]
    subelement_classes = [wall, floor, wizard.furniture.MagicDoor]


class PlayerBathroom(assets.places.Bathroom):
    count = (1, 2)


class PlayerParlor(assets.places.Parlor):
    count = (1, 2)


class PlayerBedroom(assets.places.Bedroom):
    count = (1, 2)
    furniture_classes = [wizard.furniture.Bed, fur.Dresser]


class TrophyRoom(pl.Place):
    name = "trophy room"
    sprite = "T"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    furniture_classes = [fur.Carpet, wizard.furniture.TrophyPlinth]
    subelement_classes = [wall, floor]


class Laboratory(pl.Place):
    name = "laboratory"
    sprite = "L"
    count = (1, 2)
    colors = ["white"]
    textures = ["tiled"]
    furniture_classes = [wizard.furniture.SummoningCircle, fur.TableWork]
    subelement_classes = [wall, floor]


class PlayerDen(assets.places.Den):
    furniture_classes = [wizard.furniture.DenTable, fur.Chair, fur.Carpet, fur.Bookcase]


# Cavern (L1)
class CavernEntrance(pl.Place):
    name = "cavern"
    sprite = "E"
    count = (1, 2)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]


class CavernOpen(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (3, 7)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = [cc["caverns_1"], cc["caverns_1"], cc["caverns_1"], cc["caverns_1"]]
    # creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]


class Tunnel(pl.Place):
    name = "tunnel"
    sprite = "T"
    count = (1, 3)
    colors = ["dark", "dripping"]
    textures = ["stone", "mud"]
    creature_classes = [cc["tunnels"]]
    furniture_classes = []
    subelement_classes = [wall, floor]


class GoblinCavernVillage(CavernOpen):
    """A goblin village in a cavern with some loot."""
    name = "goblin village"
    sprite = "G"
    count = (1, 4)
    furniture_classes = [wizard.furniture.Mattress, wizard.furniture.Firepit, wizard.furniture.L1Chest]
    creature_classes = [cc["caverns_1_gobs"], cc["caverns_1_gobs"], cc["caverns_1_gobs"]]


class GoblinChiefVillage(GoblinCavernVillage):
    """Village where the goblin chief resides."""
    name = "goblin chief village"
    sprite = "K"
    count = (1, 2)
    creature_classes = [[(ShallowGoblin, 1)], [(ShallowGoblin, 1)], [(ShallowGoblinChief, 1)], [(GoblinPetDog, 1)]]


# Cavern (L2)
class CavernOpenL2(CavernOpen):
    """An open cavern."""
    creature_classes = [cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"]]
    furniture_classes = [wizard.furniture.GiantMushroom, (wizard.furniture.GoblinGrave, wizard.furniture.DarkElfGrave, None, None)] + CavernOpen.furniture_classes.copy()


class GoblinCavernVillageL2(GoblinCavernVillage):
    creature_classes = [cc["caverns_2_gobs"], cc["caverns_2_gobs"], cc["caverns_2_gobs"], cc["caverns_2_gobs"]]
    furniture_classes = [wizard.furniture.GiantMushroom] + GoblinCavernVillage.furniture_classes.copy()


class DarkElfOutpost(CavernOpenL2):
    """A forward scouting base of the dark elves."""
    name = "dark elf outpost"
    sprite = "D"
    count = (1, 4)
    creature_classes = [cc["caverns_2_elves"], cc["caverns_2_elves"], cc["caverns_2_elves"], cc["caverns_2_elves"]]
    furniture_classes = [wizard.furniture.GiantMushroomWithHammock, wizard.furniture.PupTent, wizard.furniture.Firepit, wizard.furniture.L2Chest]


class CavernLake(pl.Place):
    name = "cave lake"
    sprite = "L"
    count = (1, 5)
    colors = ["slate", "black", "wet"]
    textures = ["dark"]
    creature_classes = [cc["fish"], cc["fish"], cc["fish"], cc["fish"]]
    # creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, water, lakebed, wizard.furniture.Stalactite]
    # Fire spells will fail here
    wet = True


class DarkElfGuardtower(pl.Place):
    name = "guard tower"
    sprite = "T"
    count = (1, 2)
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    creature_classes = [[(DarkElfChampion, 1)], [(ArmoredGiantSpider, 1)], [(DarkElfChampion, 1)], [(ArmoredGiantSpider, 1)]]
    furniture_classes = [wizard.furniture.L2Chest]
    subelement_classes = [wall, floor]


# Dark Elf (L3)
class DarkElfHollowedStalagmite(pl.Place):
    name = "stalagmite quarters"
    sprite = "S"
    count = (5, 10)
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    creature_classes = [cc["de_fortress_guards"], cc["de_fortress_guards"], cc["de_fortress_guards"], cc["de_fortress_guards"]]
    subelement_classes = [wizard.furniture.FrescoWall, floor]
    furniture_classes = [fur.Carpet, fur.Bed, fur.DiningTable, fur.DiningChair, fur.Stove]


class DarkElfWorkshop(pl.Place):
    name = "workshop"
    sprite = "W"
    count = (1, 3)
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    creature_classes = [cc["de_fortress_guards"], cc["de_fortress_guards"], cc["de_fortress_guards"], [(DarkElfSmith, 1)]]
    subelement_classes = [wizard.furniture.FrescoWall, floor]
    furniture_classes = [fur.TableWork, fur.Chair, wizard.furniture.L3Chest]


class ArachneNest(pl.Place):
    name = "nest"
    sprite = "N"
    count = (1, 3)
    colors = ["cobwebbed", "silken", "woven"]
    textures = ["white", "gray"]
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]
    furniture_classes = []
    creature_classes = [[(Arachne, 1)], [(Arachne, 1)]]


class DarkElfEntrance(pl.Place):
    name = "Entryway"
    sprite = "E"
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]
    creature_classes = []
    furniture_classes = []


class QueensNest(pl.Place):
    name = "queen's lair"
    sprite = "Q"
    count = (1, 2)
    colors = ["cobwebbed", "silken", "woven"]
    textures = ["white", "gray"]
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]
    furniture_classes = [wizard.furniture.L3Chest]
    creature_classes = [[(ArachneQueen, 1)], [(DarkElfChampion, 1)], [(Arachne, 1)], [(DarkElfFairy, 1)]]


# Lake (L4)
class LakeShore(pl.Place):
    name = "lake shore"
    sprite = "S"
    count = (1, 2)
    colors = ["black", "white"]
    textures = ["sandy"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [single_wall, floor]


class LakeTile(pl.Place):
    name = "cave lake"
    sprite = "L"
    count = (5, 10)
    colors = ["black", "wet", "murky"]
    textures = ["dark"]
    creature_classes = [cc["lake_4_big_fish"], cc["lake_4_big_fish"], cc["lake_4_small_fish"], cc["lake_4_pests"]]
    furniture_classes = [wizard.furniture.WithyMushrooms, wizard.furniture.PadMushroom]
    subelement_classes = [water, lakebed, wizard.furniture.Stalactite]
    # Fire spells will fail here
    wet = True
    door_class = channel


# TODO-DONE spell to summon Excalibur
class MirrorLake(pl.Place):
    name = "mirror lake"
    sprite = "M"
    count = (1, 2)
    colors = ["glassy"]
    textures = ["mirrored"]
    creature_classes = []
    furniture_classes = [wizard.furniture.ExcaliburChest]
    subelement_classes = [mirrored_water]
    wet = True
    door_class = channel
    mirrored_creatures = []

    def addCreature(self, creature):
        """Creates mirror fight."""
        if creature not in self.creatures:
            self.creatures.append(creature)
            if creature not in self.mirrored_creatures:
                copied = copy.deepcopy(creature)
                copied.team = "mirrored"
                self.creatures.append(copied)
                self.mirrored_creatures.append(creature)
                copied.location = self
                copied.classname = "reflected " + copied.classname
                copied.name = copied.name + "'s reflection"
                print(f"{BC.MAGENTA}{creature.name}'s reflection rises up from the mirrored surface!{BC.OFF}")


# Goblintown (L5)
class GoblinTownGateway(pl.Place):
    name = "Welcome to Goblintown!"
    sprite = "G"
    count = (5, 10)
    colors = ["brown", "gray", "tan"]
    textures = ["hide", "leather"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor]
    door_class = gateway


class GoblinTownShack(pl.Place):
    name = "goblin shack"
    sprite = "S"
    count = (5, 10)
    colors = ["brown", "gray", "tan"]
    textures = ["hide", "leather"]
    creature_classes = [cc["goblintown"], cc["goblintown"], cc["goblintown"], cc["goblintown"]]
    furniture_classes = []
    subelement_classes = [wall, floor]


class GoblinTownFirepit(pl.Place):
    name = "goblin barbecue"
    sprite = "P"
    count = (2, 3)
    colors = ["dark", "gray", "black"]
    textures = ["stone"]
    creature_classes = [cc["goblintown"], cc["goblintown"], cc["goblintown"], cc["goblintown"]]
    furniture_classes = [wizard.furniture.Firepit, wizard.furniture.SittingRock]
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]


class GreatGoblinsHall(pl.Place):
    name = "Great Goblin's hall"
    sprite = "H"
    count = (1, 2)
    colors = ["dark", "gray", "black"]
    textures = ["stone"]
    creature_classes = [[(GoblinPetOwlbear, 1)], [(GoblinPetOwlbear, 1)], [(Troll, 1)], [(Troll, 1)], [(GreatGoblin, 1)]]
    furniture_classes = [wizard.furniture.Firepit, wizard.furniture.SittingRock, wizard.furniture.Mattress, wizard.furniture.L3Chest]
    subelement_classes = [wall, floor, pillar]


# Necromancer (L6)
class DwarvenEntranceHall(pl.Place):
    name = "Entrance to Zugalbash"
    sprite = "E"
    count = (1, 2)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, pillar]
    door_class = dwarven_gateway


class DwarvenHomeNecromancer(pl.Place):
    name = "dwarven home"
    sprite = "H"
    count = (5, 10)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = [cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"]]
    furniture_classes = [wizard.furniture.StoneBed, wizard.furniture.StoneTable, wizard.furniture.StoneChair]
    subelement_classes = [wall, floor]


class DwarvenWorkshopNecromancer(pl.Place):
    name = "dwarven workshop"
    sprite = "W"
    count = (1, 4)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = [cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"], cc["necromancer"]]
    furniture_classes = [wizard.furniture.Anvil, wizard.furniture.StoneTableWork]
    subelement_classes = [wall, floor]


class DwarvenAleHallNecromancer(pl.Place):
    name = "dwarven ale hall"
    sprite = "A"
    count = (1, 2)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = [[(Necromancer, 1)], cc["necromancer"], cc["necromancer"]]
    furniture_classes = [wizard.furniture.StoneTable, wizard.furniture.StoneChair, wizard.furniture.StoneTable, wizard.furniture.StoneChair, wizard.furniture.StoneTable, wizard.furniture.StoneChair, wizard.furniture.StoneTable, wizard.furniture.StoneChair, wizard.furniture.L3Chest]
    subelement_classes = [wall, floor, pillar]


# Mountainhome (L7)

class DwarvenStairway(pl.Place):
    name = "dwarven stairway"
    sprite = "S"
    count = (1, 2)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, pillar]

class DwarvenHomeL7(pl.Place):
    name = "dwarven home"
    sprite = "H"
    count = (5, 10)
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]
    creature_classes = [cc["mountainhome"], cc["mountainhome"], cc["mountainhome"], cc["mountainhome"], cc["mountainhome_security"]]
    furniture_classes = [wizard.furniture.StoneBed, wizard.furniture.StoneTable, wizard.furniture.StoneChair]
    subelement_classes = [wall, floor]
