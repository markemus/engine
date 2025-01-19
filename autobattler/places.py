import engine.place as pl

from engine.styles import wall, single_wall, floor, water, mirrored_water, lakebed, pillar, door, channel, gateway, dwarven_gateway, staircase
from autobattler.shopkeeper import Shopkeeper


class ChangingRooms(pl.Place):
    name = "changing room"
    sprite = "C"
    count = (1, 2)
    colors = ["white", "brown", "yellow", "gray"]
    textures = ["tiled"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor]


class Arena(pl.Place):
    name = "arena"
    sprite = "A"
    count = (1, 2)
    colors = ["white", "brown", "yellow", "gray"]
    textures = ["brick"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor]


class GolemStore(pl.Place):
    name = "Everything Golems"
    sprite = "S"
    count = (1, 2)
    colors = ["white", "brown", "yellow", "gray"]
    textures = ["tiled"]
    creature_classes = [[(Shopkeeper, 1)]]
    furniture_classes = []
    subelement_classes = [wall, floor]
