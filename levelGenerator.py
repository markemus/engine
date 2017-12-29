import copy
import math
import random

import place 
import levelmap

class levelGenerator(object):
    """
    Generates a single level from a template.
    """
    def __init__(self):
        pass

    #generates levels
    def levelGen(self, levelname, levelstyle):
        roomList = []
        lastRoom = None
        #leadRoom is an index in roomList
        (x,y) = (0,0)

        #get room counts
        roomcounts = self.count_rooms(levelstyle)
        roomNum = sum(roomcounts.values())
        # roomGenerators = self.get_room_generators(levelstyle)

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
            # gennedRoom = roomGenerators[roomType].random_room_generator(gennedLevel)
            gennedRoom = roomType(str(roomType), gennedLevel)
            gennedRoom.sprite = str(thisRoomNum)

            #first room needs to be start, doesn't need to connect to previous room
            if len(roomList) == 0:
                gennedLevel.start = gennedRoom
            else:
                lastRoom = roomList[lastRoomNum]

            # roomGenerators[roomType].connectRooms(gennedRoom,lastRoom)
            self.connectRooms(gennedRoom,lastRoom)

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

    def count_rooms(self, levelstyle):
        roomcounts = {}

        for room_class in levelstyle.room_classes:
            roomrange = room_class.count
            count = random.randrange(*roomrange)
            roomcounts[room_class] = count

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

    def connectRooms(self, room1, room2):
        """
        Add a door connecting room_1 to previous room room_2 (or to nothing if there is no previous room).
        """
        color = random.choice(room1.colors)
        texture = random.choice(room1.textures)

        door = place.door(color, texture)
        
        door.addBorder(room1)
        room1.addElement(door)

        # if first room generated (DOOR SHOULD CONNECT TO PREVIOUS LEVEL)
        if room2 == None:
            pass
        else:
            door.addBorder(room2)
            room2.addElement(door)