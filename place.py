import imp, copy

# End of Loading Zone

final = []

class place:
    name = ""
    elements = []
    borders = {"n" : None, "s" : None, "w" : None, "e" : None, ">" : None}
    cantransfer = False
    area = "You are standing in"
    sprite = "O"
    creatures = []

    def __init__(self, newname, newElements, newsprite, level):
        self.name = newname
        self.elements = copy.deepcopy(self.elements)
        self.borders = copy.copy(self.borders)
        self.creatures = copy.deepcopy(self.creatures)
        self.sprite = newsprite
        self.level = level
        for anElem in newElements:
            self.elements.append(anElem)

    def desc(self):
        """
        Basic describe function, always called desc.
        """
        count = 0
        area = "You are standing in " + self.name + " with a "

        #shows visible Elements only (eg not hidden doors)
        for roomElem in self.elements:
            if count == 0:
                if roomElem.visible == True:           
                    area = area + roomElem.color + " " + roomElem.name
                    count = count + 1
            elif count > 0:
                if roomElem.visible == True:
                    area = area + ", a " + roomElem.color + " " + roomElem.name
        print(area + ".")

        #show visible contents of Elements
        for roomElem in self.elements:             
            if len(roomElem.vis_inv) > 0:
                print("The " + roomElem.name + " contains the following items:")
                for contents in roomElem.vis_inv:
                    print(contents.name)
                for contents in roomElem.vis_inv:
                    contents.desc()

        for roomCreature in self.creatures:
            print("You see a: " + roomCreature.name + ".")

    def elem_check(self, tag):
        elem_total = []

        for elem in self.elements:
            elem_total += elem.elem_check(tag)

        return elem_total

    def get_borders(self):
        """
        Gives the Place its Elements' Borders.
        """
        for subElement in self.elements:
            subBorders = subElement.borders

            if len(subBorders) != 0:
                for room in subBorders:
                    if room != self and (room.level == self.level):
                        roomIndex = room.level.roomLocations[room]
                        selfIndex = self.level.roomLocations[self]
                        relativeIndex = (roomIndex[0]-selfIndex[0], roomIndex[1]-selfIndex[1])
                        
                        #we need to find where room is relative to self
                        if relativeIndex == (-2,0):
                            self.borders["n"] = room
                        if relativeIndex == (2,0):
                            self.borders["s"] = room
                        if relativeIndex == (0,-2):
                            self.borders["w"] = room
                        if relativeIndex == (0,2):
                            self.borders["e"] = room
                    elif (room.level != self.level):
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
        return self.creatures

    def get_level(self):
        return self.level



class element():
    name = "NO_NAME_PLACE"
    visible = True                  #element is shown during place's desc()
    moveable = False
    breakable = False               #can it be broken
    color = "NO_COLOR" 
    vis_inv = []                    #things on element
    invis_inv = []                  #things in element
    elements = []                   #elements in element
    area = "You see a "

    def __init__(self, newname, newcolor):
        self.borders = []
        self.name = newname
        self.color = newcolor
        self.vis_inv = copy.copy(self.vis_inv)
        self.invis_inv = copy.copy(self.invis_inv)
        self.elements = copy.copy(self.elements)

    def desc(self):
        count = 0

        if self.visible == True:
            self.area = self.area + self.color + " " + self.name
            
            for subElem in self.elements:
                if count == 0:
                    if subElem.visible == True:
                        self.area = self.area + subElem.color + " " + subElem.name
                        count = count + 1
                elif count > 0:
                    if subElem.visible == True:
                        self.area = self.area + ", a " + subElem.color + " " + subElem.name
           
            for contents in self.vis_inv:
                if contents.visible == True:
                    self.area = self.area + " containing " + contents.color + " " + contents.name

            print(self.area + ".")

            for subElem in self.elements:
                if len(subElem.vis_inv) > 0:
                    print("The " + subElem.name + " contains the following items:")
                    for contents in subElem.vis_inv:
                        print(contents.name)
                    for contents in subElem.vis_inv:
                        contents.desc()    
                else:
                    print("As far as you can tell the " + subElem.name + " contains no items.") 

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