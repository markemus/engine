import place, copy, levelmap, random, math, creature, creatureGenerator

class levelGenerator(object):

    def __init__(self, game):
        self.game = game
        self.doors = []
        self.walls = []
        self.floors = []
        self.windows = []
        self.ceilings = []
        self.elemTypes = {"door" : self.doors, "wall" : self.walls, "floor" : self.floors, "window" : self.windows, "ceiling" : self.ceilings}

        self.door = place.element("door", "undefined")
        self.wall = place.element("wall", "undefined")
        self.floor = place.element("floor", "undefined")
        self.window = place.element("window", "undefined")

        self.colors = ["red", "orange", "green", "blue", "yellow", "purple", "black", "white"]

        #temporary list
        self.creatureTemplateList = [creatureGenerator.t_templateCreature]

    #populates elemTypes[] sublists
    #listOfElements example: ["door", "window", "floor"]
    #updates them in order of color, for easy later reference, eg elemTypes['wall'][0] will be a red wall
    def colorGenerator(self, listOfElements):                     
        for anElem in listOfElements:
            for aColor in self.colors:
                self.elemTypes[anElem].append(place.element(anElem,aColor))          

    #returns a room with chosen colors. For random, see randomRoomGenerator
    def roomGenerator(self, newname, floorColor, wallColor, wallNumber, sprite, level):
        localElements = []
        
        #floor
        localElements.append(copy.deepcopy(self.floors[self.colors.index(floorColor)]))

        #walls
        while wallNumber > 0:
            localElements.append(copy.deepcopy(self.walls[self.colors.index(wallColor)]))     #copies the appropriately colored wall into localElements
            wallNumber = wallNumber - 1

        gennedRoom = place.place(newname, localElements, sprite, level)
        return gennedRoom

    def randomRoomGenerator(self, level):

        firstNameList = ["Opal", "Serene", "Floating", "Orange", "Sinister"]
        secondNameList = ["Palace", "Dungeon", "Basement", "Tower", "Tomb"]

        floorColorIndex = random.randrange(len(self.colors)-1)
        wallColorIndex = random.randrange(len(self.colors)-1)
        floorColor = self.colors[floorColorIndex]
        wallColor = self.colors[wallColorIndex]

        #gen room name
        range_1 = len(firstNameList)
        range_2 = len(secondNameList)
        nameIndex_1 = random.randrange(range_1)
        nameIndex_2 = random.randrange(range_2)
        randomName = firstNameList[nameIndex_1] + " " + secondNameList[nameIndex_2]

        randomRoom = self.roomGenerator(randomName, floorColor, wallColor, 4, "O", level)

        return randomRoom

    def doorGen(self, newname, color, borders = []):

        newDoor = place.element(newname, color)
        for room in borders: 
            newDoor.addBorder(room)
        return newDoor

    def connectRooms(self, room_1, room_2):
        # add a door connecting room_1 to previous room (or to nothing if there is no previous room.)

        doorColorIndex = random.randrange(len(self.colors)-1)
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

    def populateRoom(self, room):
        templateIndex = random.randrange(len(self.creatureTemplateList))
        creatureTemplate = self.creatureTemplateList[templateIndex]
        gennedCreatureGenerator = creatureGenerator.creatureGenerator(creatureTemplate)
        gennedCreature = gennedCreatureGenerator.creatureGen("lizard of " + room.name)
        room.addCreature(gennedCreature)
        gennedCreature.location = room

    #generates levels
    def levelGen(self, newname, roomNum):

        roomList = []
        lastRoom = None
        #leadRoom is an index in roomList
        (x,y) = (0,0)

        #create level
        gennedLevel = levelmap.levelmap(newname, roomNum)
        levelmap.levels.append(gennedLevel)
        self.game.add_level(gennedLevel)

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

            #create a room
            gennedRoom = self.randomRoomGenerator(gennedLevel)
            gennedRoom.sprite = str(thisRoomNum)
            # gennedRoom.sprite = "O"

            #first room needs to be start, doesn't need to connect to previous room
            if len(roomList) != 0:
                lastRoom = roomList[lastRoomNum]
            else:
                gennedLevel.start = gennedRoom

            self.connectRooms(gennedRoom, lastRoom)
            self.populateRoom(gennedRoom)

            #add room to gennedLevel's levelMap and roomList
            gennedLevel.addRoom(x,y,gennedRoom)
            roomList.append(gennedRoom)

            #choose next room location
            #first we need a shift, which must be (2,0),(-2,0),(0,2),(0,-2).
            delta = [(2,0),(-2,0),(0,2),(0,-2)]
            #min and max stop us from checking the same shift twice
            deltaMin = 0
            deltaMax = len(delta)

            #do only if this isn't last room.
            #prevents error if this is last room and roomNum is perfect square (so no available slots)
            if (newRoom != roomNum -1):
                while True:
                    deltaIndex = random.randrange(deltaMin, deltaMax)
                    our_delta = delta[deltaIndex]

                    #now ensure that the room slot is empty
                    testx = x + our_delta[0]
                    testy = y + our_delta[1]
                    testIndex = gennedLevel.checkIndex(testx,testy)

                    #python allows negative indices to wrap around- we don't want that
                    #in this outcome, our room slot is available, so we assign it
                    #we save the last room's indices in case we need to backtrack
                    #we reset lastRoomNum in case we backtracked
                    if testIndex == 'X' and testx >= 0 and testy >= 0:
                        previousRoomList.append((x,y))
                        lastRoomNum = len(previousRoomList) - 1
                        (x,y) = (testx, testy)
                        deltaMin = 0
                        break
                        
                    #in this outcome, our room slot is not available, so we try the next adjacency
                    else:
                        delta[deltaMin], delta[deltaIndex] = delta[deltaIndex], delta[deltaMin]
                        deltaMin += 1

                    #in this outcome, no adjacent room slots are available, so we backtrack
                    #we negatively iterate lastRoomNum in case we have to do so again
                    if deltaMin == deltaMax:
                        deltaMin = 0
                        previousRoom = previousRoomList[lastRoomNum]
                        lastRoomNum = lastRoomNum -1
                        x = previousRoom[0]
                        y = previousRoom[1]

        #borders aren't updated until rooms are populated- they have doors now.
        for room in roomList:
            room.get_borders()
        print(previousRoomList)