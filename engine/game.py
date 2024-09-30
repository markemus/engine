from . import fsm
from . import levelGenerator
from . import styles


class Game(object):
    """See, it's really very simple."""
    def __init__(self, name, gamestyle):
        self.name = name
        self.char = None
        self.level_list = []
        self.current_level = None
        # self.clock = fsm.clock(self)
        
        self.levelGenerator = levelGenerator.levelGenerator()
        
        # Generate
        self._generate(gamestyle)
        self.set_current_level(0)

    def _generate(self, gamestyle):
        assert issubclass(gamestyle, styles.GameStyle)

        for levelstyle in gamestyle.levelorder:
            levelname = "level {}".format(str(levelstyle))
            gennedLevel = self.levelGenerator.levelGen(levelname, levelstyle)
            self.level_list.append(gennedLevel)

        # Connect levels to one another.
        for (l1, l2) in zip([None, ] + self.level_list, self.level_list):
            # Skip first level
            if l1 is not None:
                self.levelGenerator.connectRooms(l2.start, l1.end)
                l2.start.get_borders()
                l1.end.get_borders()

    def set_char(self, char):
        self.char = char

    def add_level(self, level):
        self.level_list.append(level)

    def set_current_level(self, index):
        self.current_level = self.level_list[index]

    def get_char(self):
        return self.char

    def get_level(self):
        return self.current_level


if __name__ == '__main__':
    # TODO castle has been moved to its own subpackage. Maybe we should put tests in one location.
    x = Game("testGame", styles.Castle)

    for level in x.level_list:
        for room in level.roomLocations.keys():
            print(room.desc(full=False))
