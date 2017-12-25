import imp, math

creature = imp.load_source("creature", "creature.py")
place = imp.load_source("place", "place.py")
item = imp.load_source("item", "item.py")

#contains all levels in order
levels = []

#maps a single level
class levelmap():
    name = ''
    start = None
    end = None

    def __init__(self, newname, roomnum):
        self.name = newname
        #take sqrt of roomnum, round up, cast as int. That gives us a map with enough room.
        #Then scale the map up.
        x = (2 * int(math.ceil(math.sqrt(roomnum)))) + 1
        self.layout = [["X" for i in range(x)] for j in range(x)]
        self.roomLocations = {}

    def addRoom(self, x, y, room):
        self.layout[x][y] = room
        self.roomLocations[room] = (x,y)

    def printMap(self):
        for row in self.layout:
            row_sprite = ""
            for index in row:
                if hasattr(index,"sprite"):
                    row_sprite += str(index.sprite)
                else:
                    row_sprite += str(index)
            print(row_sprite)

    def show_map(self):
        ourMap = ""
        for row in self.layout:
            row_sprite = ""
            for index in row:
                if hasattr(index,"sprite"):
                    row_sprite += str(index.sprite)
                else:
                    row_sprite += str(index)
            ourMap += "\n" +row_sprite
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