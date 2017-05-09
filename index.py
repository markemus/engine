import imp, levelmap, combat, game, gui

creature = imp.load_source("creature", "creature.py")
place = imp.load_source("place", "place.py")
item = imp.load_source("item", "item.py")
levelGenerator = imp.load_source("levelGenerator", "levelGenerator.py")
man = imp.load_source("man", "man.py")

# End of Loading Zone
t_game = game.Game("The Howling Manor")
t_levelGenerator = levelGenerator.levelGenerator(t_game)

t_levelGenerator.colorGenerator(["door", "window", "floor", "wall"])

t_levelGenerator.levelGen("The Saintly Hollows", 9)

thisLevel = levelmap.levels[0]
# thisGame = game.Game("The Canticles of Darkness")
# thisGame.add_level(thisLevel)
t_game.set_current_level(0)

adam = creature.creature("Adam")
torso = creature.limb("torso")
torso.isSurface = True
torso.damage = 10
adam.subelements.append(torso)
t_game.set_char(adam)

adam.subelements[0].amble = 1
adam.location = thisLevel.start
adam.team = "player"
t_game.set_char(adam)

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

gui = gui.Gui(t_game)
# gui.keyboard.game = thisGame
gui.mainloop()