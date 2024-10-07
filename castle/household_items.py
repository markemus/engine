from engine import item as it


class Blanket(it.Item):
    name = "blanket"

class CandleStick(it.Item):
    name = "candlestick"

class Goblet(it.Item):
    name = "goblet"

class Hammer(it.Item):
    name = "hammer"

class Pillow(it.Item):
    name = "pillow"

class Plate(it.Item):
    name = "plate"

class Pliers(it.Item):
    name = "pliers"

class Screwdriver(it.Item):
    name = "screwdriver"

class Sheet(it.Item):
    name = "sheet"

class Utensils(it.Item):
    name = "utensils"

# Collections
candles = {
    "contains": [CandleStick],
    "color": ["shiny", "tarnished"],
    "color_scheme": "same",
    "texture": ["copper", "silver", "gold"],
    "texture_scheme": "same",
}

linens = {
    "contains": [Pillow, Blanket, Sheet],
    "color": ["blue", "green", "silver", "brown"],
    "color_scheme": "distinct",
    "texture": ["quilted", "patterned", "wool", "linen"],
    "texture_scheme": "same",
}

silver = {
    "contains": [Plate, Utensils, Goblet],
    "color": ["shiny", "tarnished"],
    "color_scheme": "same",
    "texture": ["copper", "silver", "gold"],
    "texture_scheme": "same",
}
tools = {
    "contains": [Hammer, Pliers, Screwdriver],
    "color": ["black", "gray"],
    "color_scheme": "distinct",
    "texture": ["metal", "iron"],
    "texture_scheme": "distinct",
}