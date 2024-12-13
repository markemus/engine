"""Items are used by creatures as clothing, weapons, jewelry etc. Furniture is a special type of
item that is used to fill rooms. Items have an inventory that can hold other items."""
from collections import defaultdict

from colorist import Color as C, BrightColor as BC


# TODO not all items need inventories.
# TODO interior and exterior inventories.
class Item:
    """name: Item's displayed name.
    canwear: Item can be worn on Limbs with this 'wears' tag.
    printcolor: display color.
    requires: (tag, amount)- if Item requires a tag on a Limb to be equipped.
    level: each Limb can only wear one Item per level (eg undershirt=1 and shirt=2)."""
    name = "item"
    canwear = defaultdict(lambda: False)
    printcolor = C.BLUE
    # requires = (tag, amount) if needed- eg (grasp, 1)
    requires = None
    level = 1

    def __init__(self, color, texture):
        """Copies over mutable objects for objects so they don't share them with other objects (dereference)."""
        # Subclasses should copy Item.canwear and then modify in class definition (before instantiation).
        self.canwear = self.canwear.copy()
        self.color = color
        self.texture = texture

    # TODO it would be nice to replace this function with one that gives more info on wherefrom and whereto to the player.
    def transfer(self, who, wherefrom, whereto):
        """A creature moves an item from one inventory to another."""
        if self in wherefrom:
            # Determines that 'who' is able to grasp the item.
            if who.grasp(self):               
                whereto.append(self)
                wherefrom.remove(self)
                who.ungrasp(self)
                print(f"{BC.CYAN}{who.name} puts away the {self.name}.{BC.OFF}")
            else:
                print(f"{C.RED}The {who.name} cannot pick up the {self.name}.{C.OFF}")
        else:
            print(f"{C.RED}The {self.name} is not there.{C.OFF}")

    def desc(self, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"* {C.BLUE}{self.color} {self.texture} {self.name}{C.OFF}"

        return text


# TODO function to allow char to check invis_inv. For now just use vis_inv.
class Container(Item):
    """Containers contain hidden inventories."""
    def __init__(self, color, texture):
        super().__init__(color=color, texture=texture)
        self.invis_inv = []


class Holder(Item):
    """Holders have a visible inventory."""
    def __init__(self, color, texture):
        super().__init__(color=color, texture=texture)
        self.vis_inv = []

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" " * offset) + f"* {C.BLUE}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset=offset + 1)

        return text


class Potion(Item):
    name = "potion"
    edible = True
    def __init__(self):
        super().__init__(color="gray", texture="murky")
    def eat(self, creature):
        """Subclasses should define an effect on creature when creature drinks the potion."""
        print(f"{BC.CYAN}The {self.name} has no effect.{BC.OFF}")
