import combat
import creature
import place
import item
import levelGenerator
import game
import gui
import levelmap
import man
import styles

# End of Loading Zone
t_game = game.Game("The Howling Manor", styles.Castle)

thisLevel = t_game.level_list[0]

adam = man.man("Adam", location=thisLevel.start)
t_game.set_char(adam)
adam.team = "player"

thisLevel.printMap()
print(adam.location.name)
adam.location.desc()
adam.speak("hello world", adam.location.creatures[0])

print(adam.location.borders.keys())

def tryDirections():
    for direction in adam.location.borders.keys():
        if adam.location.borders[direction] != None:
            print(direction)
            return direction

adam.leave(tryDirections())
adam.location.desc()
adam.speak("Stand and deliver!", adam.location.creatures[0])

adam.leave(tryDirections())
adam.location.desc()
combat.round(adam)
adam.leave(tryDirections())

adam.location.creatures[0].desc()

print(adam.get_location())
adam.location.elements[0].canCatch = True
t_game.clock.combat_handler()

adam.location.creatures[0].desc()

adam.location.desc()
adam.desc()
# print(adam.desc())

print(adam.location.desc())
# gui = gui.Gui(t_game)
# gui.keyboard.game = thisGame
# gui.mainloop()