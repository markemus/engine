import fsm, levelGenerator

class Game(object):

    def __init__(self, name):
        self.name = name
        self.char = None
        self.level_list = []
        self.current_level = None
        self.clock = fsm.clock(self)

    def set_char(self, char):
        self.char = char

    def add_level(self, level):
        self.level_list.append(level)

    def set_current_level(self, index):
        worked = True
        try:
            self.current_level = self.level_list[index]
        except:
            worked = False

        return worked

    def get_char(self):
        return self.char

    def get_level(self):
        return self.current_level