import engine.creature as cr

class Teeth(cr.Weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 15
    appendageRange = (1, 2)
    wears = "fang"
    base_hp = 20
    size = 1
    colors = ["white"]
    textures = ["sharp"]

class Maw(cr.Limb):
    name = "maw"
    subelement_classes = [Teeth]
    appendageRange = (1, 2)
    wears = "mouth"
    base_hp = 30
    size = 2
    strength = 1

class Tube(cr.Limb):
    name = "tube"
    subelement_classes = [Maw]
    appendageRange = (1, 2)
    wears = "animal_body"
    base_hp = 40
    size = 3
    amble = 1

class TunnelWorm(cr.creature):
    """A vicious creature that tunnels around looking for food."""
    classname = "tunnel worm"
    aggressive = True
    can_breathe = False
    can_stun = False
    can_poison = False
    team = "monster"
    namelist = ["tunnel worm"]
    baseElem = Tube
    colors = ["red", "yellow", "white"]
    textures = ["slimy"]
    suits = []
