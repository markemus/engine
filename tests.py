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

    def test_furniture_creation(self):
        """Tests that furniture is added to rooms properly."""
        import castle.castle as cs
        import castle.furniture as fur
        parlor = cs.Parlor("test_parlor", None)
        chairs = [x for x in parlor.elements if isinstance(x, fur.Chair)]
        # Proper number of chairs
        assert chairs[0].count[1] > len(chairs) >= chairs[0].count[0]
        # Chairs get their own color schema
        assert (chairs[0].color in fur.Chair.color) and (chairs[0].texture in fur.Chair.texture)

    def test_room_connections(self):
        """Rooms in a level should have doors connecting them, with a path throughout the level."""
        import castle.castle as cs
        from engine import game
        from engine import styles
        t_game = game.Game("The Howling Manor", cs.Castle)
        thisLevel = t_game.level_list[0]
        roomList = thisLevel.get_rooms()

        # There should only be a single door in common (we can update test later if that changes).
        for r1, r2 in zip([None, ] + roomList, roomList):
            # First room has no backwards connection.
            if r1 is not None:
                shared_elems = [elem for elem in r1.elements if elem in r2.elements]
                assert len(shared_elems) == 1
                assert isinstance(shared_elems[0], styles.door)
