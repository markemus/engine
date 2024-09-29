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
        from engine import game
        from engine import interface
        from castle import man
        from castle import castle

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
