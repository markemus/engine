import copy
import random

from colorist import Color as C
# End of Loading Zone

class place:
    """creature_classes structure: [[(creature11, weight11), (creature12, weight12)], [(creature21, weight21)]]"""
    name = "generic_place"
    elements = []
    borders = {"n": None, "s": None, "w": None, "e": None, ">": None}
    cantransfer = False
    area = "You are standing in"
    sprite = "R"
    creature_classes = []

    def __init__(self, name, level, extra_creatures=None):
        self.name = name
        self.elements = []
        self.borders = {"n": None, "s": None, "w": None, "e": None, ">": None}
        self.creatures = []
        # self.sprite = newsprite
        self.level = level
        # for anElem in newElements:
        #     self.elements.append(anElem)
        self._elementGen()
        self._populate(extra_creatures)
        self.get_borders()

    def desc(self, full=True, offset=0):
        """Basic describe function, always called desc."""
        text = (" "*offset) + "# " + self.name
        # if full:
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
            if issubclass(elemclass, furniture):
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
                # name = creature_type.name + " of " + self.name
                # creature = creature_type(name, location=self)
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
                    # TODO-DONE don't forget downwards rooms.
                    elif room.level != self.level:
                        self.borders[">"] = room

    def addElement(self, element):
        self.elements.append(element)

    def addCreature(self, creature):
        if not creature in self.creatures:
            self.creatures.append(creature)
        else:
            None

    def removeCreature(self, creature):
        if creature in self.creatures:
            self.creatures.remove(creature)
        else:
            None

    def get_creatures(self):
        return copy.copy(self.creatures)

    def get_level(self):
        return self.level


class element:
    name = "NO_NAME_ELEM"
    visible = True                  # element is shown during place's desc()
    color = "NO_COLOR"
    printcolor = C.YELLOW
    texture = "NO_TEXTURE"
    elements = []

    def __init__(self, color, texture):
        self.borders = []
        self.color = color
        self.texture = texture
        self.vis_inv = []
        self.invis_inv = []
        self.elements = []      # subelements

    # def desc(self):
    #     count = 0

    #     if self.visible == True:
    #         area = "You see a {} {} {}".format(self.color, self.texture, self.name)

    #         for subElem in self.elements:
    #             if count == 0:
    #                 if subElem.visible == True:
    #                     area = area + subElem.color + " " + subElem.name
    #                     count = count + 1
    #             elif count > 0:
    #                 if subElem.visible == True:
    #                     area = area + ", a " + subElem.color + " " + subElem.name

    #         for contents in self.vis_inv:
    #             if contents.visible == True:
    #                 area = area + " containing " + contents.color + " " + contents.name

    #         print(area + ".")

    #         for subElem in self.elements:
    #             if len(subElem.vis_inv) > 0:
    #                 print("The " + subElem.name + " contains the following items:")
    #                 for contents in subElem.vis_inv:
    #                     print(contents.name)
    #                 for contents in subElem.vis_inv:
    #                     contents.desc()
    #             else:
    #                 print("As far as you can tell the " + subElem.name + " contains no items.")

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"- {self.printcolor}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset=offset+1)
            for elem in self.elements:
                if elem.visible:
                    text += "\n" + elem.desc(offset=offset+1)

        return text

    def elem_check(self, tag):
        elem_total = []

        if hasattr(self, tag):
            elem_total.append(self)

        for subElem in self.elements:
            elem_total += subElem.elem_check(tag)

        return elem_total

    def addBorder(self, place):
        if not place in self.borders:
            self.borders.append(place)

    def add_vis_item(self, item):
        self.vis_inv.append(item)


class furniture(element):
    name = "NO_NAME_FURN"
    visible = True  # element is shown during place's desc()
    color = "NO_COLOR"
    printcolor = C.MAGENTA
    texture = "NO_TEXTURE"
    elements = []
