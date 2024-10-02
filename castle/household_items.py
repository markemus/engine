from engine import item as it

class Fork(it.Item):
    name = "fork"

class Knife(it.Item):
    name = "knife"
class Plate(it.Item):
    name = "plate"

class Spoon(it.Item):
    name = "spoon"


# sets
place_setting = [Plate, Fork, Knife, Spoon]