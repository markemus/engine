import math
import random

from . import place
from . import levelmap


class levelGenerator:
    """Generates a single level from a Style."""
    def __init__(self):
        pass

    def levelGen(self, levelname, levelstyle):
        roomList = []
        lastRoom = None
        # leadRoom is an index in roomList
        # x, y = 0, 0

        # Get room counts
        roomcounts = self.count_rooms(levelstyle)
        roomNum = sum(roomcounts.values())
        # roomGenerators = self.get_room_generators(levelstyle)

        # Create level
        gennedLevel = levelmap.levelmap(levelname, roomNum)

        # Choose starting room index
        # First calculate the number of potential room locations
        upperLimit = int(math.ceil(math.sqrt(roomNum)))
        x = (random.randrange(upperLimit) * 2) + 1
        y = (random.randrange(upperLimit) * 2) + 1

        thisRoomNum = 0
        lastRoomNum = 0
        previousRoomList = []

        for newRoom in range(roomNum):
            thisRoomNum += 1

            # Choose a room
            roomType = random.choice(list(roomcounts.keys()))
            
            if roomcounts[roomType] > 1:
                roomcounts[roomType] -= 1
            else:
                del roomcounts[roomType]

            # Create a room
            # gennedRoom = roomGenerators[roomType].random_room_generator(gennedLevel)
            # TODO better room names
            gennedRoom = roomType(str(roomType), gennedLevel)
            gennedRoom.sprite = str(thisRoomNum)

            # First room needs to be start, doesn't need to connect to previous room
            if len(roomList) == 0:
                gennedLevel.start = gennedRoom
            else:
                lastRoom = roomList[lastRoomNum]

            # roomGenerators[roomType].connectRooms(gennedRoom,lastRoom)
            self.connectRooms(gennedRoom, lastRoom)

            # Add room to gennedLevel's levelMap and roomList
            gennedLevel.addRoom(x, y, gennedRoom)
            roomList.append(gennedRoom)

            # Do only if this isn't last room.
            # Prevents error if this is last room and roomNum is perfect square (so no available slots).
            if newRoom != roomNum - 1:
                x, y = self.find_slot(gennedLevel, x, y, previousRoomList)
                previousRoomList.append((x, y))
                lastRoomNum = len(previousRoomList) - 1

        # Borders aren't updated until rooms are populated- they have doors now.
        for room in roomList:
            room.get_borders()
        
        return gennedLevel

    def count_rooms(self, levelstyle):
        roomcounts = {}

        for room_class in levelstyle.room_classes:
            roomrange = room_class.count
            count = random.randrange(*roomrange)
            roomcounts[room_class] = count

        return roomcounts

    def find_slot(self, gennedLevel, x, y, previousRoomList):
        """Choose next room location."""
        # First we need a shift, which must be (2,0),(-2,0),(0,2),(0,-2).
        delta = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        # min and max stop us from checking the same shift twice
        deltaMin = 0
        lastRoomNum = len(previousRoomList) - 1

        while True:
            deltaIndex = random.randrange(deltaMin, len(delta))
            our_delta = delta[deltaIndex]

            # Now ensure that the room slot is empty
            testx = x + our_delta[0]
            testy = y + our_delta[1]
            testIndex = gennedLevel.checkIndex(testx, testy)

            # Python allows negative indices to wrap around- we don't want that.
            # In this outcome, our room slot is available, so we assign it
            # we save the last room's indices in case we need to backtrack
            # we reset lastRoomNum in case we backtracked
            if testIndex == 'X' and testx >= 0 and testy >= 0:
                (x, y) = (testx, testy)
                deltaMin = 0
                break
                
            # In this outcome, our room slot is not available, so we try the next adjacency
            else:
                # Swap current into lowest available slot, and check higher only
                delta[deltaMin], delta[deltaIndex] = delta[deltaIndex], delta[deltaMin]
                deltaMin += 1

            # In this outcome, no adjacent room slots are available, so we backtrack
            # We negatively iterate lastRoomNum in case we have to do so again
            if deltaMin == len(delta):
                previousRoom = previousRoomList[lastRoomNum]
                x = previousRoom[0]
                y = previousRoom[1]

                deltaMin = 0
                lastRoomNum = lastRoomNum - 1

        return x, y

    def connectRooms(self, room1, room2):
        """Add a door connecting room_1 to previous room room_2 (or to nothing if there is no previous room)."""
        color = random.choice(room1.colors)
        texture = random.choice(room1.textures)

        door = place.door(color, texture)
        
        door.addBorder(room1)
        room1.addElement(door)

        # if first room generated
        # TODO DOOR SHOULD CONNECT TO PREVIOUS LEVEL
        if room2 is None:
            pass
        else:
            door.addBorder(room2)
            room2.addElement(door)
