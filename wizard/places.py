import engine.place as pl
from engine.styles import wall, floor, pillar, door

import assets.furniture as fur

import wizard.furniture


class MagicFoyer(pl.Place):
    name = "foyer"
    sprite = "F"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Carpet]
    subelement_classes = [wall, floor, wizard.furniture.MagicDoor]
