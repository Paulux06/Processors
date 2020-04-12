import pygame

class GameView:
    def __init__(self, main, x, y, xSize, ySize):
        self.main = main
        self.x, self.y = x, y
        self.xSize, self.ySize = xSize, ySize
        self.objects = []
        #             cx cy  X                              Y
        self.camera = [0, 0, self.main.gameMaster.player.x, self.main.gameMaster.player.y]
        self.viewDist = 12

    def createMap(self):
        for x in range(self.main.gameMaster.world.size[0]):
            for y in range(self.main.gameMaster.world.size[1]):
                if self.main.gameMaster.world.getAt(x, y) == self.main.gameMaster.world.constants.APPLE:
                    self.objects.append(Apple(x, y, self.main))
        self.objects.append(Player(self.main))
    
    def resize(self):
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]

    def refresh(self, dt):
        self.camera[0] += (self.camera[2]-self.camera[0])/20
        self.camera[1] += (self.camera[3]-self.camera[1])/20
        pygame.draw.rect(
            self.main.screen.window,
            [40, 150, 40],
            [self.sPos[0], self.sPos[1], self.sPos[2]+2, self.sPos[3]+2])
        for obj in self.objects:
            if (abs(self.camera[2]-obj.x) < self.viewDist and abs(self.camera[3]-obj.y) < self.viewDist):
                obj.render(self)

    def drawPoly(self, coordList, color, obj):
        positions = []
        for coord in coordList: #convert from 0 center to 0 top left
            positions.append((
                ((coord[0]+1)/2)*self.sPos[2]+(obj.x-self.camera[0])*self.sPos[2]*0.05+(obj.y-self.camera[1])*self.sPos[2]*0.05, 
                ((coord[1]/2+1)/2)*self.sPos[2]+(self.sPos[3]/2-self.sPos[2]/2)-coord[2]*self.sPos[2]/4+(obj.x-self.camera[0])*self.sPos[2]*0.025-(obj.y-self.camera[1])*self.sPos[2]*0.025
                ))
        pygame.draw.polygon(self.main.screen.window, color, positions)
        
    def drawCircle(self, x, y, z, radius, color, obj):
        cx = ((x+1)/2)*self.sPos[2]+(obj.x-self.camera[0])*self.sPos[2]*0.05+(obj.y-self.camera[1])*self.sPos[2]*0.05
        cy = ((y/2+1)/2)*self.sPos[2]+(self.sPos[3]/2-self.sPos[2]/2)-z*self.sPos[2]/4+(obj.x-self.camera[0])*self.sPos[2]*0.025-(obj.y-self.camera[1])*self.sPos[2]*0.025
        pygame.draw.circle(self.main.screen.window, color, [int(cx), int(cy)], radius)

class Player:
    def __init__(self, main):
        self.main = main
        self.x, self.y = self.main.gameMaster.player.x, self.main.gameMaster.player.y
        self.polys = [
            Poly( [
                (-0.1, 0, 0.05), (0, 0.1, 0.05), (0.1, 0, 0.05), (0, -0.1, 0.05)
            ], [40, 40, 40]),
            Poly( [
                (-0.1, 0, 0.05), (0, 0.1, 0.05), (0, 0.1, 0), (-0.1, 0, 0)
            ], [80, 80, 80]),
            Poly( [
                (0.1, 0, 0.05), (0, 0.1, 0.05), (0, 0.1, 0), (0.1, 0., 0)
            ], [80, 80, 80])
        ]
        self.eyes = Circle(0.05, -0.05, 0.05, 5, [255, 255, 255])

    def render(self, scrn):
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.NORTH:
            self.eyes.x, self.eyes.y, self.eyes.z = 0.05, -0.05, 0.05
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.SUD:
            self.eyes.x, self.eyes.y, self.eyes.z = -0.05, 0.05, 0.05
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.EAST:
            self.eyes.x, self.eyes.y, self.eyes.z = 0.05, 0.05, 0.05
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.WEST:
            self.eyes.x, self.eyes.y, self.eyes.z = -0.05, -0.05, 0.05

        self.main.screen.gameView.camera[2:4] = [self.x, self.y]
        self.x, self.y = self.main.gameMaster.player.x, self.main.gameMaster.player.y
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.WEST or self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.NORTH:
            self.eyes.draw(scrn, self)
        for poly in self.polys:
            poly.draw(scrn, self)
        if self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.EAST or self.main.gameMaster.player.orient == self.main.gameMaster.player.constants.SUD:
            self.eyes.draw(scrn, self)

class Apple:
    def __init__(self, x, y, main):
        self.main = main
        self.x, self.y = x, y
        self.polys = [
            Poly( [
                (-0.05, 0, 0.05), (0, 0.05, 0.05), (0.05, 0, 0.05), (0, -0.05, 0.05)
            ], [250, 40, 40]),
            Poly( [
                (-0.05, 0, 0.05), (0, 0.05, 0.05), (0, 0.05, 0), (-0.05, 0, 0)
            ], [250, 80, 80]),
            Poly( [
                (0.05, 0, 0.05), (0, 0.05, 0.05), (0, 0.05, 0), (0.05, 0, 0)
            ], [250, 80, 80])
        ]

    def render(self, scrn):
        if not self.main.gameMaster.world.getAt(self.x, self.y) == self.main.gameMaster.world.constants.APPLE:
            self.main.screen.gameView.objects.remove(self)
            del self
            return False
        for poly in self.polys:
            poly.draw(scrn, self)

class Poly:
    def __init__(self, coordsList, color):
        self.coordsList = coordsList
        self.color = color

    def draw(self, screen, obj):
        screen.drawPoly(self.coordsList, self.color, obj)

class Circle:
    def __init__(self, x, y, z, radius, color):
        self.x, self.y, self.z = x, y, z
        self.radius = radius
        self.color = color

    def draw(self, screen, obj):
        screen.drawCircle(self.x, self.y, self.z, self.radius, self.color, obj)