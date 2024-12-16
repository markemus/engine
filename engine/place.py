import copy
import random

from colorist import Color as C
from colorist import BrightColor as BC


class Place:
    """creature_classes structure: [[(creature11, weight11), (creature12, weight12)], [(creature21, weight21)]]"""
    name = "generic_place"
    elements = []
    borders = {"n": None, "s": None, "w": None, "e": None, ">": None}
    # cantransfer = False
    area = "You are standing in"
    sprite = "R"
    creature_classes = []

    def __init__(self, level, extra_creatures=None):
        # self.name = name
        self.elements = []
        self.borders = {"n": None, "s": None, "w": None, "e": None, ">": None}
        self.creatures = []
        # self.sprite = newsprite
        self.level = level
        # for anElem in newElements:
        #     self.elements.append(anElem)
        self._elementGen()
        self._populate(extra_creatures)
        # self.get_borders()

    def desc(self, full=True, offset=0):
        """Basic describe function, always called desc."""
        text = (" "*offset) + "# " + f"{C.RED}{self.name}{C.OFF}"

        for creature in self.creatures:
            text += "\n" + creature.desc(full=full, offset=offset + 1)
        for elem in self.elements:
            if elem.visible:
                text += "\n" + elem.desc(full=full, offset=offset + 1)

        return text

    def elem_check(self, tag):
        elem_total = []

        for elem in self.elements:
            elem_total += elem.elem_check(tag)

        return elem_total

    def _elementGen(self):
        for elemclass in self.subelement_classes + self.furniture_classes:
            # Choose
            if type(elemclass) == tuple:
                elemclass = random.choice(elemclass)

            # Furniture should have their own colors, while room elements should match the room.
            if issubclass(elemclass, Furniture):
                color = random.choice(elemclass.color)
                texture = random.choice(elemclass.texture)
            else:
                color = random.choice(self.colors)
                texture = random.choice(self.textures)

            # Count
            try:
                potentialRange = elemclass.count
            except AttributeError:
                raise AttributeError("'{0}' : {1} object has no attribute 'count'".format(elemclass.name, elemclass))
            countRange = random.randrange(potentialRange[0], potentialRange[1])
            # Create
            for count in range(countRange):
                elem = elemclass(color, texture)
                self.elements.append(elem)

    def _populate(self, extra_creatures=None):
        """Creates one creature per creature_class. extra_creatures allows creatures that are
        not included as part of the class definition.[[(c11, w11), (c12, w12)], [(c21, w21)]."""
        if extra_creatures:
            creature_classes = self.creature_classes + extra_creatures
        else:
            creature_classes = self.creature_classes

        # Pick one creature per creature_class
        for creature_class in creature_classes:
            creatures, weights = zip(*creature_class)
            creature_type = random.choices(creatures, weights, k=1)[0]

            # Selecting None means no creature is spawned for that creature_class
            if creature_type is not None:
                creature = creature_type(location=self)
                self.creatures.append(creature)

    def get_borders(self):
        """Gives the Place its Elements' Borders."""
        for subElement in self.elements:
            subBorders = subElement.borders

            if len(subBorders) != 0:
                for room in subBorders:
                    if room != self and (room.level == self.level):
                        roomIndex = room.level.roomLocations[room]
                        selfIndex = self.level.roomLocations[self]
                        relativeIndex = (roomIndex[0]-selfIndex[0], roomIndex[1]-selfIndex[1])
                        
                        # We need to find where room is relative to self
                        if relativeIndex == (-2,0):
                            self.borders["n"] = room
                        if relativeIndex == (2,0):
                            self.borders["s"] = room
                        if relativeIndex == (0,-2):
                            self.borders["w"] = room
                        if relativeIndex == (0,2):
                            self.borders["e"] = room
                    elif room.level != self.level:
                        self.borders[">"] = room

    def addElement(self, element):
        self.elements.append(element)

    def addCreature(self, creature):
        if not creature in self.creatures:
            self.creatures.append(creature)

    def removeCreature(self, creature):
        if creature in self.creatures:
            self.creatures.remove(creature)

    def get_creatures(self):
        return copy.copy(self.creatures)

    def get_level(self):
        return self.level

    def find_invs(self):
        """Find all inventories in the room (except creature inventories)."""
        invs = []

        for element in self.elements:
            invs += element.find_invs()

        return invs



class Element:
    name = "NO_NAME_ELEM"
    visible = True                  # element is shown during place's desc()
    color = "NO_COLOR"
    texture = "NO_TEXTURE"
    printcolor = C.YELLOW
    # elements = []

    def __init__(self, color, texture):
        self.borders = []
        self.color = color
        self.texture = texture
        self.subelements = []      # subelements

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"- {self.printcolor}{self.color} {self.texture} {self.name}{C.OFF}"
        # Indicate contents
        if self.subelements and not full:
            text = text + " *"
        if full:
            for elem in self.subelements:
                if elem.visible:
                    text += "\n" + elem.desc(offset=offset+1)

        return text

    # TODO doesn't check items. Just subelements. We should extend this search so that it can find
    #  the real characteristics of the element- eg table canCatch. Think about future variations in how this
    #  (sort of) function can work.
    def elem_check(self, tag):
        elem_total = []

        if hasattr(self, tag):
            elem_total.append(self)

        for subelem in self.subelements:
            elem_total += subelem.elem_check(tag)

        return elem_total

    def find_invs(self):
        """Find all inventories in the room (except creature inventories)."""
        invs = []

        for element in self.subelements:
            invs += element.find_invs()

        return invs

    def addBorder(self, place):
        if place not in self.borders:
            self.borders.append(place)


class Platform(Element):
    """Platforms have a visible inventory."""
    name = "platform"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vis_inv = []

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"- {self.printcolor}{self.color} {self.texture} {self.name}{C.OFF}"
        # Indicate contents
        if (self.vis_inv or self.subelements) and not full:
            text = text + " *"
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset=offset+1)
            for elem in self.subelements:
                if elem.visible:
                    text += "\n" + elem.desc(offset=offset+1)

        return text

    def find_invs(self):
        """Find all inventories in the room (except creature inventories)."""
        invs = []
        # Since Platforms have a vis_inv
        invs += [self]

        for element in self.subelements:
            invs += element.find_invs()

        for item in self.vis_inv:
            invs += item.find_invs()

        return invs

class Furniture(Element):
    visible = True
    printcolor = C.MAGENTA


class DisplayFurniture(Furniture, Platform):
    visible = True  # element is shown during place's desc()
    color = "NO_COLOR"
    printcolor = C.MAGENTA
    texture = "NO_TEXTURE"
    elements = []
    vis_collections = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fill()

    def _fill(self):
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
                    item_classes = item_collection["contains"].copy()
                    if not item_collection["full"]:
                        random.shuffle(item_classes)
                        item_classes = item_classes[:random.randrange(0, len(item_classes))]

                    for item_class in item_classes:
                        if item_collection["color_scheme"] == "unique":
                            color = random.choice(item_collection["color"])
                        else:
                            color = colors[item_class]
                        if item_collection["texture_scheme"] == "unique":
                            texture = random.choice(item_collection["texture"])
                        else:
                            texture = textures[item_class]
                        if isinstance(item_class, tuple):
                            # TODO-DECIDE should we use a fixed seed for this? To coordinate sets of shoes eg? Same by Item._fill_vis()
                            item_class = random.choice(item_class)

                        item = item_class(color, texture)
                        self.vis_inv.append(item)
