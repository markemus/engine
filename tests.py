class TestCastle():
    def test_style_inheritance(self):
        """Tests that Castle game is an abstract subclass of GameStyle."""
        import castle.castle_style as c
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

        from castle import castle_style
        from castle import human

        # Game generation
        t_game = game.Game("The Howling Manor", castle_style.Castle)
        thisLevel = t_game.level_list[0]

        # Character creation
        adam = human.Human(location=thisLevel.start)
        thisLevel.start.creatures.append(adam)
        t_game.set_char(adam)
        adam.team = "player"
        i = interface.Interface(t_game)
        assert i.state == "move"
        # Check creatures
        assert adam in thisLevel.start.creatures
        # Check that Adam has been clothed
        assert adam.subelements[0].equipment
        # TODO-DONE test that creatures exist
        assert len(thisLevel.start.creatures) > 1
        # Check organs
        assert len(adam.subelements[0].limb_check("grasp")) == 2
        assert len(adam.subelements[0].limb_check("amble")) == 2
        # Check room
        assert isinstance(adam.location, place.Place)
        borders = [x for x in adam.location.borders.values() if isinstance(x, place.Place)]
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
        import castle.castle_style as cs
        import castle.furniture as fur
        parlor = cs.Parlor("test_parlor", None)
        chairs = [x for x in parlor.elements if isinstance(x, fur.Chair)]
        # Proper number of chairs
        assert chairs[0].count[1] > len(chairs) >= chairs[0].count[0]
        # Chairs get their own color schema
        assert (chairs[0].color in fur.Chair.color) and (chairs[0].texture in fur.Chair.texture)

    def test_room_connections(self):
        """Rooms in a level should have doors connecting them, with a path throughout the level."""
        import castle.castle_style as cs
        from castle import goblin
        from engine import game

        visited = []

        def explore_depth(g, border):
            """We will send our goblin down each path until the end,
            at which point it will backtrack."""
            # Explore border
            orig_loc = g.location
            g.leave(border)
            new_loc = g.location
            # Goal is to visit every location in level.
            if new_loc not in visited:
                visited.append(new_loc)
            # Save return info
            return_path = [a[0] for a in new_loc.borders.items() if a[1] == orig_loc][0]

            # Explore each path from new location, except the one we came in on.
            for test_border in new_loc.borders.keys():
                test_loc = new_loc.borders[test_border]
                if (test_loc is not None) and (test_loc is not orig_loc):
                    # Go down each path until the end (recursion)
                    explore_depth(g, test_border)
            # Backtrack once paths are explored
            g.leave(return_path)

        # Run test
        t_game = game.Game("The Howling Manor", cs.Castle)
        thisLevel = t_game.level_list[0]
        g = goblin.Goblin(location=thisLevel.start)
        test_borders = [b for b in g.location.borders.keys() if g.location.borders[b] is not None]

        # Check each path leaving from the first room.
        visited.append(g.location)
        for border in test_borders:
            explore_depth(g, border)

        # Collect all rooms so we can ensure each was visited (pigeonhole principle).
        all_rooms = []
        for level in t_game.level_list:
            # print(level.show_map())
            all_rooms.extend(level.get_rooms())

        assert len(all_rooms) == len(visited)

    def test_grasp(self):
        """NPC grasps and ungrasps an item."""
        import castle.castle_style as cs
        import castle.suits as su

        from castle.goblin import ServantGoblin
        room = cs.PlayerCell(level=None)
        g = ServantGoblin(location=room)
        s = su.Shank(color="gray", texture="iron")
        g.grasp(s)
        assert g.grasp_check().grasped == s
        g.ungrasp(s)
        assert g.grasp_check().grasped is None

    def test_return_from_depth(self):
        from castle.goblin import Goblin
        g = Goblin(None)
        subelem_names = [x.name for x in g.subelements[0].return_from_depth(2)]
        assert "right hand" in subelem_names
        assert "finger" not in subelem_names

    def test_covers(self):
        """Tests that items cover lower limbs as they're supposed to."""
        import castle.castle_style as cs
        import castle.suits as su

        from castle.goblin import Goblin
        Goblin.suits = [su.testsuit]
        room = cs.PlayerCell(level=None)
        g = Goblin(location=room)
        head = g.subelements[0].subelements[0]
        assert head.equipment[0].descends == 2
        # Helm should cover teeth as well
        assert head.subelements[4].covers[0] == head.covers[0]


class TestGeneral:
    def test_dependencies(self):
        import colorist
        import transitions
        pass
