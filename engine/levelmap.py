import math

from colorist import Color as C
from colorist import BrightColor as BC


# Maps a single level
class levelmap:
    name = ''
    start = None
    end = None

    def __init__(self, newname, roomnum):
        self.name = newname
        # Take sqrt of roomnum, round up, cast as int. That gives us a map with enough room.
        # Then scale the map up.
        x = (2 * int(math.ceil(math.sqrt(roomnum)))) + 1
        # Dots are empty space
        self.layout = [["." for i in range(x)] for j in range(x)]
        self.roomLocations = {}

    def addRoom(self, x, y, room):
        self.layout[x][y] = room
        self.roomLocations[room] = (x, y)

    def addDoor(self, x, y, door):
        self.layout[x][y] = door

    def printMap(self, char):
        for row in self.layout:
            row_sprite = ""
            for x in row:
                if hasattr(x, "creatures") and char in x.creatures:
                        row_sprite += f"{char.printcolor}U{C.OFF}"
                elif hasattr(x, "sprite"):
                    row_sprite += str(x.sprite)
                else:
                    # row_sprite += str(x)
                    row_sprite += f"{C.GREEN}{x}{C.OFF}"
            print(row_sprite)

    def show_map(self):
        """This is a duplicate of printMap with very similar features. Difference is that char is not shown and map
        is returned instead of printed."""
        ourMap = ""
        for row in self.layout:
            row_sprite = ""
            for index in row:
                if hasattr(index, "sprite"):
                    row_sprite += str(index.sprite)
                else:
                    row_sprite += str(index)
            ourMap += "\n" + row_sprite
        return ourMap

    def checkIndex(self, x, y):
        try:
            index = self.layout[x][y]
            return index
        except:
            return False

    def getRoomIndex(self, room):
        return self.roomLocations[room]

    def get_rooms(self):
        return list(self.roomLocations.keys())