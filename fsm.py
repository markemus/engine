from transitions import Machine
import combat

class clock(object):
    states = ["move", "combat"]

    def __init__(self, game):
        self.game = game
        self.machine = Machine(states=clock.states, initial="move")
        self.machine.add_ordered_transitions()

    # def combat_handler(self):
    #     char = self.game.get_char()
    #     room = char.get_location()

    #     for creature in room.get_creatures():
    #         combat.round(creature)