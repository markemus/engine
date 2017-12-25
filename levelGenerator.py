import place, copy, levelmap, random, math, creatureGenerator

import random

class levelGenerator(object):
    """
    Generates a single level from a template.
    """
    def __init__(self):
        pass
        #temporary list
        # self.creatureTemplateList = [creatureGenerator.t_templateCreature]
        # self.RoomGenerator = RoomGenerator()

    #generates levels
    def levelGen(self, levelname, levelstyle):
        roomList = []
        lastRoom = None
        #leadRoom is an index in roomList
        (x,y) = (0,0)

        #get room counts
        roomcounts = self.count_rooms(levelstyle)
        roomNum = sum(roomcounts.values())
        roomGenerators = self.get_room_generators(levelstyle)
        # for roomGenerator in roomGenerators:
        #     print(roomGenerator.colors)
        # print("levelGen: roomNum, roomcounts: ", roomNum, roomcounts)

        #create level
        gennedLevel = levelmap.levelmap(levelname, roomNum)

        #choose starting room index
        #first calculate the number of potential room locations
        upperLimit = int(math.ceil(math.sqrt(roomNum)))
        x = (random.randrange(upperLimit) * 2) + 1
        y = (random.randrange(upperLimit) * 2) + 1

        thisRoomNum = 0
        lastRoomNum = 0
        previousRoomList = []

        for newRoom in range(roomNum):
            thisRoomNum += 1

            #choose a room
            roomType = random.choice(list(roomcounts.keys()))
            
            if roomcounts[roomType] > 1:
                roomcounts[roomType] -= 1
            else:
                del roomcounts[roomType]

            #create a room
            gennedRoom = roomGenerators[roomType].random_room_generator(gennedLevel)
            gennedRoom.sprite = str(thisRoomNum)

            #first room needs to be start, doesn't need to connect to previous room
            if len(roomList) == 0:
                gennedLevel.start = gennedRoom
            else:
                lastRoom = roomList[lastRoomNum]

            roomGenerators[roomType].connectRooms(gennedRoom,lastRoom)

            #add room to gennedLevel's levelMap and roomList
            gennedLevel.addRoom(x,y,gennedRoom)
            roomList.append(gennedRoom)

            #do only if this isn't last room.
            #prevents error if this is last room and roomNum is perfect square (so no available slots)
            if (newRoom != roomNum -1):
                (x,y) = self.find_slot(gennedLevel, x, y, previousRoomList)
                previousRoomList.append((x,y))
                lastRoomNum = len(previousRoomList) - 1

        #borders aren't updated until rooms are populated- they have doors now.
        for room in roomList:
            room.get_borders()
        # print(previousRoomList)
        
        return gennedLevel

    def get_room_generators(self, levelstyle):
        roomgens = []
        for roomstyle in levelstyle.roomstyles:
            generator = StyleRoomGenerator(roomstyle)
            roomgens.append(generator)

        return roomgens

    def count_rooms(self, levelstyle):
        roomcounts = {}

        for i in range(len(levelstyle.roomstyles)):
            roomrange = levelstyle.roomstyles[i].count
            # print(roomrange)
            count = random.randrange(*roomrange)
            roomcounts[i] = count

        return roomcounts

    def find_slot(self, gennedLevel, x, y, previousRoomList):
        """
        Choose next room location.
        """
        #first we need a shift, which must be (2,0),(-2,0),(0,2),(0,-2).
        delta = [(2,0),(-2,0),(0,2),(0,-2)]
        #min and max stop us from checking the same shift twice
        deltaMin = 0
        lastRoomNum = len(previousRoomList) -1

        while True:
            deltaIndex = random.randrange(deltaMin, len(delta))
            our_delta = delta[deltaIndex]

            #now ensure that the room slot is empty
            testx = x + our_delta[0]
            testy = y + our_delta[1]
            testIndex = gennedLevel.checkIndex(testx,testy)

            #python allows negative indices to wrap around- we don't want that.
            #In this outcome, our room slot is available, so we assign it
            #we save the last room's indices in case we need to backtrack
            #we reset lastRoomNum in case we backtracked
            if testIndex == 'X' and testx >= 0 and testy >= 0:
                (x,y) = (testx, testy)
                deltaMin = 0
                break
                
            #in this outcome, our room slot is not available, so we try the next adjacency
            else:
                #swap current into lowest available slot, and check higher only
                delta[deltaMin], delta[deltaIndex] = delta[deltaIndex], delta[deltaMin]
                deltaMin += 1

            #in this outcome, no adjacent room slots are available, so we backtrack
            #we negatively iterate lastRoomNum in case we have to do so again
            if deltaMin == len(delta):
                previousRoom = previousRoomList[lastRoomNum]
                x = previousRoom[0]
                y = previousRoom[1]

                deltaMin = 0
                lastRoomNum = lastRoomNum -1

        return (x,y)

class RoomGenerator():
    """
    Generates rooms from a template.
    """
    def __init__(self, colors, textures, furniture, creatures):
        self.doors = {}
        self.walls = {}
        self.floors = {}
        self.windows = {}
        self.ceilings = {}
        self.elemTypes = {"door" : self.doors, "wall" : self.walls, "floor" : self.floors, 
                        "window" : self.windows, "ceiling" : self.ceilings}

        # self.colors = colors if colors != [] else ["red", "orange", "green", "blue", "yellow", "purple", "black", "white"]
        # self.textures = textures if textures != [] else ["wood", "stone", "brick"]
        # self.creatureTemplates = creatures if creatures != [] else [creatureGenerator.t_templateCreature]
        self.colors = colors
        self.textures = textures
        self.creatureTemplates = creatures
        
        self._color_generator()
    
    def _color_generator(self):
        """
        Populates elemTypes[] sublists.
        ListOfElements example: ["door", "window", "floor"]
        Updates them in order of color, for easy later reference, eg elemTypes['wall'][0] will be a red wall
        """
        for elem in list(self.elemTypes.keys()):
            for color in self.colors:
                self.elemTypes[elem][color] = {}
                for texture in self.textures:
                    self.elemTypes[elem][color][texture] = place.element(elem, color + " " + texture)
                    # self.elemTypes[anElem].append(place.element(anElem, aColor + " " + aTexture))

        # print("self.floors", self.floors)
        # print("self.colors", self.colors)
        # for elemlist in self.elemTypes.values():
        #     for elem in elemlist:
        #         elem.desc()
        
        # print(self.elemTypes)

    def random_room_generator(self, level):
        firstNameList = ["Opal", "Serene", "Floating", "Orange", "Sinister"]
        secondNameList = ["Palace", "Dungeon", "Basement", "Tower", "Tomb"]

        #colors
        floorColor = random.choice(self.colors)
        wallColor = random.choice(self.colors)

        #textures
        floorTexture = random.choice(self.textures)
        wallTexture = random.choice(self.textures)

        #name
        firstName = random.choice(firstNameList)
        secondName = random.choice(secondNameList)
        randomName = firstName + " " + secondName

        randomRoom = self.room_generator(randomName, floorColor, floorTexture, wallColor, wallTexture, 4, "O", level)
        self.populate_room(randomRoom)

        return randomRoom

    def room_generator(self, newname, floorColor, floorTexture, wallColor, wallTexture, wallNumber, sprite, level):
        """
        Returns a room with chosen colors. For random, see randomRoomGenerator.
        """
        localElements = []
        
        #floor
        localElements.append(copy.deepcopy(self.floors[floorColor][floorTexture]))

        #walls
        while wallNumber > 0:
            #copies the appropriately colored wall into localElements
            localElements.append(copy.deepcopy(self.walls[wallColor][wallTexture]))
            wallNumber = wallNumber - 1

        gennedRoom = place.place(newname, localElements, sprite, level)

        return gennedRoom

    def populate_room(self, room):
        templateIndex = random.randrange(len(self.creatureTemplates))
        creatureTemplate = self.creatureTemplates[templateIndex]
        gennedCreatureGenerator = creatureGenerator.creatureGenerator()
        gennedCreature = gennedCreatureGenerator.creatureGen(creatureTemplate.name + " of " + room.name, creatureTemplate)
        room.addCreature(gennedCreature)
        gennedCreature.location = room

    def doorGen(self, newname, color, borders = []):
        newDoor = place.element(newname, color)
        for room in borders: 
            newDoor.addBorder(room)

        return newDoor

    def connectRooms(self, room_1, room_2):
        """
        Add a door connecting room_1 to previous room room_2 (or to nothing if there is no previous room).
        """
        doorColorIndex = random.randrange(len(self.colors))
        doorColor = self.colors[doorColorIndex]

        # if first room generated (DOOR SHOULD CONNECT TO PREVIOUS LEVEL)
        if room_2 == None:
            borders = [room_1]
            currentDoor = self.doorGen("door", doorColor, borders)

        #if not first room
        else:
            borders = [room_1, room_2]
            currentDoor = self.doorGen("door", doorColor, borders)
            room_2.addElement(currentDoor)

        room_1.addElement(currentDoor)

class StyleRoomGenerator(RoomGenerator):
    """
    Generates rooms based on a specified RoomStyle.
    """
    def __init__(self, roomstyle, *args, **kwargs):
        colors = roomstyle.colors
        textures = roomstyle.textures
        furniture = roomstyle.furniture
        creatures = roomstyle.creatures

        super().__init__(colors, textures, furniture, creatures, *args, **kwargs)