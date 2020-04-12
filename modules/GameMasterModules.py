import numpy as np

class World:
    def __init__(self, xSize, ySize):
        self.constants = WConst()
        self.data = np.zeros([xSize, ySize], np.uint8)
        self.size = [xSize, ySize]
        # Z: 0=SOL 1=ENVIRONNEMENT 2=CIEL

    def setItem(self, x, y, itemID):
        if x >= 0 and x < self.size[0]-1:
            if y >= 0 and y < self.size[1]-1:
                    self.data[x, y] = itemID

    def getAt(self, x, y):
        try:
            return self.data[x, y]
        except:
            return 99

class WConst:
    def __init__(self):
        # / \ [Y]
        #  |
        #  |
        #  |
        #  +---------> [X]
        self.AIR = 0
        self.GROUND = 1
        self.TREE = 2
        self.APPLE = 3
        self.PLAYER = 4
        self.MONSTER = 5

class Player:
    def __init__(self, main, world, Xpos, Ypos):
        self.constants = PConst()
        self.main = main
        self.x, self.y = Xpos, Ypos
        self.world = world
        self.orient = self.constants.NORTH

    def checkForAll(self):
        if self.world.getAt(self.x, self.y) == self.world.constants.MONSTER:
            print('death')
        if self.world.getAt(self.x, self.y) == self.world.constants.APPLE:
            self.main.interpreter.lapse *= 0.9

    def isItemAround(self, item):
        state = False
        if self.world.getAt(self.x+1, self.y) == item: state = True
        if self.world.getAt(self.x+1, self.y+1) == item: state = True
        if self.world.getAt(self.x, self.y+1) == item: state = True
        if self.world.getAt(self.x-1, self.y+1) == item: state = True
        if self.world.getAt(self.x-1, self.y) == item: state = True
        if self.world.getAt(self.x-1, self.y-1) == item: state = True
        if self.world.getAt(self.x, self.y-1) == item: state = True
        if self.world.getAt(self.x+1, self.y-1) == item: state = True
        return state

    def isAppleNear(self):
        self.checkForAll()
        return self.isItemAround(self.world.constants.APPLE)

    def isMonsterNear(self):
        self.checkForAll()
        return self.isItemAround(self.world.constants.MONSTER)

    def forward(self):
        self.world.setItem(self.x, self.y, self.world.constants.AIR)
        if self.orient == self.constants.NORTH:
            #verifier pour un arbre
            self.y += 1
        if self.orient == self.constants.SUD:
            self.y -= 1
        if self.orient == self.constants.EAST:
            self.x += 1
        if self.orient == self.constants.WEST:
            self.x -= 1
        self.checkForAll()
        self.world.setItem(self.x, self.y, self.world.constants.PLAYER)

    def backward(self):
        self.world.setItem(self.x, self.y, self.world.constants.AIR)
        if self.orient == self.constants.NORTH:
            self.y -= 1
        if self.orient == self.constants.SUD:
            self.y += 1
        if self.orient == self.constants.EAST:
            self.x -= 1
        if self.orient == self.constants.WEST:
            self.x += 1
        self.world.setItem(self.x, self.y, self.world.constants.PLAYER)
        self.checkForAll()
    
    def turnLeft(self):
        if self.orient == self.constants.NORTH:
            self.orient = self.constants.WEST
        elif self.orient == self.constants.SUD:
            self.orient = self.constants.EAST
        elif self.orient == self.constants.EAST:
            self.orient = self.constants.NORTH
        elif self.orient == self.constants.WEST:
            self.orient = self.constants.SUD
        self.checkForAll()
            
    def turnRight(self):
        if self.orient == self.constants.NORTH:
            self.orient = self.constants.EAST
        elif self.orient == self.constants.SUD:
            self.orient = self.constants.WEST
        elif self.orient == self.constants.EAST:
            self.orient = self.constants.SUD
        elif self.orient == self.constants.WEST:
            self.orient = self.constants.NORTH
        self.checkForAll()

class PConst:
    def __init__(self):
        #     N
        #  W  +  E
        #     S
        self.NORTH = 1
        self.SUD = 2
        self.EAST = 3
        self.WEST = 4