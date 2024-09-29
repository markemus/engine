import pytest

class TestCastle():
    def test_style_inheritance(self):
        """Tests that Castle game is an abstract subclass of GameStyle."""
        import castle.castle as c
        import engine.styles as s

        assert issubclass(c.Castle, s.GameStyle)
        assert issubclass(c.MainFloor, s.LevelStyle)

        assert isinstance(c.Castle(), s.GameStyle)
        assert isinstance(c.MainFloor(), s.LevelStyle)

    def test_game_setup(self):
        """Tests that basic game setup results in predicted state."""
        from engine import game
        from engine import interface
        from engine import place
        from engine import styles

        from castle import castle
        from castle import man

        # Game generation
        t_game = game.Game("The Howling Manor", castle.Castle)
        thisLevel = t_game.level_list[0]

        # Character creation
        adam = man.Man("Adam", location=thisLevel.start)
        thisLevel.start.creatures.append(adam)
        t_game.set_char(adam)
        adam.team = "player"
        i = interface.Interface(t_game)
        assert i.state == "move"
        # Check creatures
        assert adam in thisLevel.start.creatures
        assert len(thisLevel.start.creatures) > 1
        # Check organs
        assert len(adam.subelements[0].limb_check("grasp")) == 2
        assert len(adam.subelements[0].limb_check("amble")) == 2
        # Check room
        assert isinstance(adam.location, place.place)
        borders = [x for x in adam.location.borders.values() if isinstance(x, place.place)]
        assert len(borders) >= 1
        # Check border between first two rooms exists and is on map
        r1 = adam.location
        r2 = borders[0]
        xy1 = thisLevel.roomLocations[r1]
        xy2 = thisLevel.roomLocations[r2]
        dxy = (int((xy1[0] + xy2[0]) / 2), int((xy1[1] + xy2[1]) / 2))
        assert isinstance(thisLevel.layout[dxy[0]][dxy[1]], styles.door)
        