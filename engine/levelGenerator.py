"""Levels are generated from Styles- see styles.py for more info. The levelGenerator object is attached to
a Game object, and uses the game's GameStyle as a configuration file. A GameStyle contains LevelStyles, which
in turn contain room information."""
import math
import random

from . import levelmap
from . import styles


class levelGenerator:
    """Generates a single level from a Style."""
    def __init__(self):
        pass

    def levelGen(self, levelname, levelstyle):
        """Generates a level. """
        roomList = []
        lastRoom = None

        # Get room counts for level
        roomcounts = self.count_rooms(levelstyle)
        roomNum = sum(roomcounts.values())
        if hasattr(levelstyle, "start_room"): roomNum += 1
        if hasattr(levelstyle, "end_room"): roomNum += 1

        # Create level (map will hold the room locations and is displayable by the player).
        gennedLevel = levelmap.levelmap(levelname, roomNum)

        # Choose starting room index on the map
        # First calculate the number of potential room locations
        upperLimit = int(math.ceil(math.sqrt(roomNum)))
        x = (random.randrange(upperLimit) * 2) + 1
        y = (random.randrange(upperLimit) * 2) + 1

        thisRoomNum = 0
        lastRoomNum = 0
        previousRoomList = []

        for newRoom in range(roomNum):
            thisRoomNum += 1

            # Choose a room type
            # Start and end rooms
            if hasattr(levelstyle, "start_room") and thisRoomNum == 1:
                roomType = levelstyle.start_room
            elif hasattr(levelstyle, "end_room") and thisRoomNum == roomNum:
                roomType = levelstyle.end_room
            else:
                roomType = random.choice(list(roomcounts.keys()))
                # Keep track of how many of each room type we need
                if roomcounts[roomType] > 1:
                    roomcounts[roomType] -= 1
                else:
                    del roomcounts[roomType]

            # Create a room- populate with level creatures if not a special room
            if (hasattr(levelstyle, "start_room") and thisRoomNum == 1) or (hasattr(levelstyle, "end_room") and thisRoomNum == roomNum):
                gennedRoom = roomType(gennedLevel)
            else:
                gennedRoom = roomType(gennedLevel, extra_creatures=levelstyle.creature_classes)
            # First room needs to be start, doesn't need to connect to a previous room
            if len(roomList) == 0:
                gennedLevel.start = gennedRoom
            else:
                lastRoom = roomList[lastRoomNum]

            # Link the room to the previous room
            if lastRoom:
                door = self.connectRooms(gennedRoom, lastRoom)
            # Add room to gennedLevel's levelMap and roomList
            gennedLevel.addRoom(x, y, gennedRoom)
            roomList.append(gennedRoom)
            # Add door to map
            if lastRoom is not None:
                (x1, y1) = gennedLevel.roomLocations[gennedRoom]
                (x2, y2) = gennedLevel.roomLocations[lastRoom]
                doorx = int((x1 + x2) / 2)
                doory = int((y1 + y2) / 2)
                gennedLevel.addDoor(doorx, doory, door)

            # Do only if this isn't last room.
            # Prevents error if this is last room and roomNum is perfect square (so no available slots).
            if newRoom != roomNum - 1:
                # Find a spot on the map for the room.
                x, y, lastRoomNum = self.find_slot(gennedLevel, x, y, previousRoomList)
                previousRoomList.append((x, y))
                lastRoomNum = lastRoomNum + 2

            # Set end room
            gennedLevel.end = roomList[-1]

        # Borders aren't updated until rooms are doored.
        for room in roomList:
            room.get_borders()

        return gennedLevel

    def count_rooms(self, levelstyle):
        """Number of rooms of each type required for the level."""
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
        # Our x,y are for current room- we are calculating next room,
        # and we are saving last room in case we are at a dead end.
        lastRoomNum = len(previousRoomList) - 2

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
            if testIndex == '.' and testx >= 0 and testy >= 0:
                (x, y) = (testx, testy)
                # print("done")
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

        return x, y, lastRoomNum

    def connectRooms(self, room1, room2):
        """Add a door connecting room_1 to previous room room_2 (or to nothing if there is no previous room)."""
        color = random.choice(room1.colors)
        texture = random.choice(room1.textures)

        door = styles.door(color, texture)
        
        door.addBorder(room1)
        room1.addElement(door)

        # if first room generated
        if room2 is None:
            pass
        else:
            door.addBorder(room2)
            room2.addElement(door)

        return door
