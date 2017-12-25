import fsm 
import levelGenerator
import styles

class Game(object):

    def __init__(self, name, gamestyle):
        self.name = name
        self.char = None
        self.level_list = []
        self.current_level = None
        self.clock = fsm.clock(self)
        
        self.levelGenerator = levelGenerator.levelGenerator()
        
        #generate
        self._generate(gamestyle)
        # for i in range(levelcount):
        #     levelName = "level {}".format(str(i))
        #     gennedLevel = lg.levelGen(levelName, roomNum=10)
        #     self.level_list.append(gennedLevel)
        
        self.set_current_level(0)

    def _generate(self, gamestyle):
        assert issubclass(gamestyle, styles.GameStyle)

        for levelstyle in gamestyle.levelorder:
            levelname = "level {}".format(str(levelstyle))
            gennedLevel = self.levelGenerator.levelGen(levelname, levelstyle)
            self.level_list.append(gennedLevel)
        
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
    x = Game("testGame", styles.Castle)

    for level in x.level_list:
        for room in level.roomLocations.keys():
            room.desc()