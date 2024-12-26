import engine.place as pl
from engine.styles import wall, floor, pillar, door

import assets.furniture as fur


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
    creature_classes = []
    furniture_classes = [fur.Bed, fur.Dresser]
    subelement_classes = [wall, floor]

class Cell(pl.Place):
    name = "cell"
    sprite = "C"
    count = (5, 10)
    colors = ["unpainted", "grimy", "grey"]
    textures = ["stone", "concrete"]
    creature_classes = []
    furniture_classes = [fur.Manacles, fur.Puddle, fur.Toilet]
    subelement_classes = [wall, floor]

class Den(pl.Place):
    name = "den"
    sprite = "D"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Table, fur.Chair, fur.Carpet, fur.Bookcase]
    subelement_classes = [wall, floor]

class DiningRoom(pl.Place):
    name = "dining room"
    sprite = "D"
    count = (1, 3)
    colors = ["purple", "red", "gold", "silver"]
    textures = ["draped", "marble", "painted", "lit"]
    creature_classes = []
    furniture_classes = [fur.Carpet, fur.DiningTable, fur.DiningChair, fur.CabinetElegant]
    subelement_classes = [wall, floor]

class Parlor(pl.Place):
    name = "parlor"
    sprite = "P"
    count = (1, 3)
    colors = ["blue", "white", "salmon", "gold", "silver"]
    textures = ["painted", "draped", "sunlit"]
    creature_classes = []
    furniture_classes = [fur.Carpet, fur.Chair]
    subelement_classes = [wall, floor]

class Kitchen(pl.Place):
    name = "kitchen"
    sprite = "K"
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted", "gray", "beige"]
    textures = ["brick", "stone"]
    creature_classes = []
    furniture_classes = [fur.Stove, fur.CabinetElegant, fur.KitchenCounter]
    subelement_classes = [wall, floor]
