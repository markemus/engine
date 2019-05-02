import place

class Wall(place.element):
    color = "wall_color"
    def __init__(self):
        super().__init__("wall")

class TortureChamber(place.place):
    def __init__(self, level):
        super().__init__("torture chamber", [], "T", level)

if __name__ == "__main__":
    w = Wall()

    print(w.newcolor)
