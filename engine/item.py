"""Items are used by creatures as clothing, weapons, jewelry etc. Furniture is a special type of
item that is used to fill rooms. Items have an inventory that can hold other items."""
from collections import defaultdict
import random

from colorist import Color as C, BrightColor as BC


# TODO interior and exterior inventories.
class Item:
    """name: Item's displayed name.
    canwear: Item can be worn on Limbs with this 'wears' tag.
    covers: Item will cover lower Limbs with this 'wears' tag (eg glove is worn on hand and covers hand+fingers).
    printcolor: display color.
    requires: (tag, amount)- if Item requires a tag on a Limb to be equipped.
    level: each Limb can only wear one Item per level (eg undershirt=1 and shirt=2)."""
    name = "item"
    canwear = defaultdict(lambda: False)
    covers = defaultdict(lambda: False)
    printcolor = C.BLUE
    # requires = (tag, amount) if needed- eg (grasp, 1)
    requires = None
    level = 1

    def __init__(self, color, texture):
        """Copies over mutable objects for objects so they don't share them with other objects (dereference)."""
        # Subclasses should copy Item.canwear and then modify in class definition (before instantiation).
        self.canwear = self.canwear.copy()
        self.covers = self.covers.copy()
        self.color = color
        self.texture = texture

    # TODO it would be nice to replace this function with one that gives more info on wherefrom and whereto to the player.
    #  or just get rid of it entirely and just simply move the item
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

    def desc(self, offset=0, stats=True):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"* {C.BLUE}{self.color} {self.texture} {self.name}{C.OFF}"

        if hasattr(self, "damage"):
            text += f" {C.RED}({self.damage}){C.OFF}"
        if hasattr(self, "armor"):
            text += f" {BC.CYAN}({self.armor}){BC.OFF}"

        return text

    def find_invs(self):
        """Find all inventories lower than this item in the hierarchy."""
        invs = []

        # This will only occur if Item has a vis_inv, but we need it to not crash for all Items. Hacky.
        if hasattr(self, "vis_inv"):
            if self.vis_inv:
                invs.append(self)
            for item in self.vis_inv:
                invs += item.find_invs()

        return invs


# TODO function to allow char to check invis_inv. For now just use vis_inv.
class Container(Item):
    invis_collections = []
    """Containers contain hidden inventories."""
    def __init__(self, color, texture):
        super().__init__(color=color, texture=texture)
        self.invis_inv = []
        self._fill_invis()

    # TODO the _fill function should be a function, not a method, and should be generic for vis and invis_inv.
    #  Then we can use the same implementation for Items and Elements
    def _fill_invis(self):
        """Put items in furniture upon creation."""
        if self.invis_collections:
            for (item_collection, count) in self.invis_collections:
                for n in range(*count):
                    if item_collection["color_scheme"] == "distinct":
                        # print("\n", item_collection["contains"])
                        colors = {key: random.choice(item_collection["color"]) for key in item_collection["contains"]}
                    else:
                        # Single color for all items
                        c = random.choice(item_collection["color"])
                        colors = {key: c for key in item_collection["contains"]}

                    # Texture is same approach as color
                    if item_collection["texture_scheme"] == "distinct":
                        textures = {key: random.choice(item_collection["texture"]) for key in item_collection["contains"]}
                    else:
                        t = random.choice(item_collection["texture"])
                        textures = {key: t for key in item_collection["contains"]}

                    # Create items
                    item_classes = item_collection["contains"].copy()
                    if not item_collection["full"]:
                        random.shuffle(item_classes)
                        item_classes = item_classes[:random.randrange(0, len(item_classes))]

                    for item_class in item_classes:
                        c = colors[item_class]
                        t = textures[item_class]
                        if isinstance(item_class, tuple):
                            item_class = random.choice(item_class)

                        item = item_class(c, t)
                        self.invis_inv.append(item)



class Holder(Item):
    """Holders have a visible inventory."""
    vis_collections = []
    def __init__(self, color, texture):
        super().__init__(color=color, texture=texture)
        self.vis_inv = []
        self._fill_vis()

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" " * offset) + f"* {C.BLUE}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset=offset + 1)

        return text

    def _fill_vis(self):
        """Put items in furniture upon creation."""
        if self.vis_collections:
            for (item_collection, count) in self.vis_collections:
                for n in range(*count):
                    if item_collection["color_scheme"] == "distinct":
                        # print("\n", item_collection["contains"])
                        colors = {key: random.choice(item_collection["color"]) for key in item_collection["contains"]}
                    else:
                        # Single color for all items
                        c = random.choice(item_collection["color"])
                        colors = {key: c for key in item_collection["contains"]}

                    # Texture is same approach as color
                    if item_collection["texture_scheme"] == "distinct":
                        textures = {key: random.choice(item_collection["texture"]) for key in item_collection["contains"]}
                    else:
                        t = random.choice(item_collection["texture"])
                        textures = {key: t for key in item_collection["contains"]}

                    # Create items
                    for item_class in item_collection["contains"]:
                        c = colors[item_class]
                        t = textures[item_class]
                        if isinstance(item_class, tuple):
                            item_class = random.choice(item_class)

                        item = item_class(c, t)
                        self.vis_inv.append(item)



class Potion(Item):
    name = "potion"
    edible = True
    def __init__(self, color="gray", texture="murky"):
        """Color and texture are accepted but ignored."""
        super().__init__(color=color, texture=texture)

    def eat(self, creature):
        """Subclasses should define an effect on creature when creature drinks the potion."""
        print(f"{BC.CYAN}The {self.name} has no effect.{BC.OFF}")
