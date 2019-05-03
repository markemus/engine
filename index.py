import game
import interface
import man
import styles


# Main
t_game = game.Game("The Howling Manor", styles.Castle)

thisLevel = t_game.level_list[0]

adam = man.Man("Adam", location=thisLevel.start)
t_game.set_char(adam)
adam.team = "player"

thisLevel.printMap(adam)
print(adam.location.name)
adam.location.desc()
adam.speak("hello world", adam.location.creatures[0])

# print("adam.location.borders.keys(): ", adam.location.borders.keys())
# def tryDirections():
#     for direction in adam.location.borders.keys():
#         if adam.location.borders[direction] is not None:
#             print(direction)
#             return direction
#
# def desc_all():
#     print("\n\nadam.desc():")
#     print(adam.desc())
#
#     print("\n\nadam.location.desc()")
#     print(adam.location.desc())
#
# adam.leave(tryDirections())
# adam.speak("Stand and deliver!", adam.location.creatures[0])
#
# adam.leave(tryDirections())
# adam.leave(tryDirections())
#
# desc_all()


# x = game.Game("testGame", styles.Castle)
# adam = man.Man("Adam", location=x.level_list[0].start)
# x.level_list[0].start.creatures = [adam] + x.level_list[0].start.creatures
# x.set_char(adam)
# adam.team = "player"
i = interface.Interface(t_game)
print(i.state)
print(adam.location.borders)
while True:
    i.command()
