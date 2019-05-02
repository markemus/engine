import styles as st

# TODO is this the old version or the new version? Put the newest version in here. And organize this sort of stuff better.
#example
class TortureChamber():
    count = (1,3)
    colors = ["black", "gray"]
    textures = ["stone", "iron", "dirt", "timber"]
    furniture = []
    creatures = []
st.RoomStyle.register(TortureChamber)

class Cell():
    count = (5,10)
    colors = ["unpainted", "grimy"]
    textures = ["stone", "concrete"]
    furniture = []
    creatures = []
st.RoomStyle.register(Cell)

class Dungeon():
    roomstyles = [TortureChamber, Cell]
    creatures = []
st.LevelStyle.register(Dungeon)




class ThroneRoom():
    count = (1, 2)
    colors = ["gold", "red"]
    textures = ["brick", "stone"]
    furniture = []
    creatures = []
st.RoomStyle.register(ThroneRoom)

class Kitchen():
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted"]
    textures = ["brick", "stone"]
    furniture = []
    creatures = []
st.RoomStyle.register(Kitchen)

class MainFloor():
    roomstyles = [ThroneRoom, Kitchen]
    creatures = []
st.LevelStyle.register(MainFloor)




class Castle():
    levelorder = [Dungeon, MainFloor]
    links = [(0,1)]
st.GameStyle.register(Castle)