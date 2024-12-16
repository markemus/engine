"""Game is used to build a game from a GameStyle. See the Castle index.py file to see how it's all put together."""
from . import levelGenerator
from . import styles


class Game(object):
    """See, it's really very simple."""
    def __init__(self, name, gamestyle):
        """Levels are created using the levelGenerator object, which generates rooms and creatures according to the
        specifications in the gamestyle."""
        self.name = name
        self.char = None
        self.level_list = []
        self.current_level = None

        self.levelGenerator = levelGenerator.levelGenerator()
        
        # Generate
        self.start_splash = gamestyle.start_splash
        self.death_splash = gamestyle.death_splash
        print(self.start_splash)

        self._generate(gamestyle)
        self.set_current_level(0)

    def _generate(self, gamestyle):
        assert issubclass(gamestyle, styles.GameStyle)

        for levelstyle in gamestyle.levelorder:
            levelname = "level {}".format(str(levelstyle))
            gennedLevel = self.levelGenerator.levelGen(levelname, levelstyle)
            gennedLevel.level_text = levelstyle.level_text
            self.level_list.append(gennedLevel)

        # TODO-DECIDE allow multiple exits from a level and other algorithm options (hallways?)
        # Connect levels to one another.
        for (l1, l2) in zip([None, ] + self.level_list, self.level_list):
            # Skip first level
            if l1 is not None:
                self.levelGenerator.connectRooms(l2.start, l1.end)
                l2.start.get_borders()
                l1.end.get_borders()

    def set_char(self, char):
        """Sets the player character for the game."""
        self.char = char

    def add_level(self, level):
        self.level_list.append(level)

    def set_current_level(self, index):
        self.current_level = self.level_list[index]
        if not self.current_level.level_text_printed:
            print(self.current_level.level_text)
            self.current_level.level_text_printed = True

    def get_char(self):
        return self.char

    def get_level(self):
        return self.current_level
