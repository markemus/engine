from engine import item as it


class Blanket(it.Item):
    name = "blanket"

class CandleStick(it.Item):
    name = "candlestick"

class Pillow(it.Item):
    name = "pillow"

class Plate(it.Item):
    name = "plate"

class Sheet(it.Item):
    name = "sheet"

class Utensils(it.Item):
    name = "utensils"

# Collections
linens = {
    "contains": [Pillow, Blanket, Sheet],
    "color": ["blue", "green", "silver", "brown"],
    "color_scheme": "distinct",
    "texture": ["quilted", "patterned", "wool", "linen"],
    "texture_scheme": "same",
}

silver = {
    "contains": [CandleStick, Plate, Utensils],
    "color": ["shiny", "tarnished"],
    "color_scheme": "same",
    "texture": ["silver"],
    "texture_scheme": "same",
}
