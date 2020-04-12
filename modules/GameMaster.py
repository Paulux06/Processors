from modules.GameMasterModules import World, Player
from random import randint as rd

class GameMaster:
    def __init__(self, main):
        self.world = World(50, 50)
        self.player = Player(main, self.world, int(self.world.size[0]/2), int(self.world.size[1]/2))
        for x in range(self.world.size[0]):
            for y in range(self.world.size[1]):
                if rd(1, 10) == 1:
                    self.world.setItem(x, y, self.world.constants.APPLE)