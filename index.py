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
# thisLevel.start.addCreature(adam)
t_game.set_char(adam)
adam.team = "player"

# cr = combat.CombatRound(adam)




thisLevel.printMap(adam)
print(adam.location.name)
adam.location.desc()
adam.speak("hello world", adam.location.creatures[0])

print("adam.location.borders.keys(): ", adam.location.borders.keys())

def tryDirections():
    for direction in adam.location.borders.keys():
        if adam.location.borders[direction] != None:
            print(direction)
            return direction

def desc_all():
    print("\n\nadam.desc():")
    print(adam.desc())

    print("\n\nadam.location.desc()")
    print(adam.location.desc())

adam.leave(tryDirections())
adam.speak("Stand and deliver!", adam.location.creatures[0])

adam.leave(tryDirections())
# combat.round(adam)
adam.leave(tryDirections())

# t_game.clock.combat_handler()

desc_all()



# gui = gui.Gui(t_game)
# gui.keyboard.game = thisGame
# gui.mainloop()