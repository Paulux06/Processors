import pygame
from modules.TextEditor import TextEditor

class Info:
    def __init__(self, main, x, y, xSize, ySize):
        self.main = main
        self.x, self.y = x, y
        self.xSize, self.ySize = xSize, ySize
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]
    
    def resize(self):
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]

    def refresh(self, dt):
        pygame.draw.rect(
            self.main.screen.window,
            [44, 62, 80],
            [self.sPos[0], self.sPos[1], self.sPos[2]+2, self.sPos[3]+2])

class RightPanel:
    def __init__(self, main, x, y, xSize, ySize):
        self.main = main
        self.x, self.y = x, y
        self.xSize, self.ySize = xSize, ySize
        self.curLevel = 0 #Level entre 0 et 1 (panneau déplié [1] ou non [0])
        self.level = 0.1  #target du level (pour faire les animations)
        self.toogleButtonArea = [0, 0] #Xmin, Xmax
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]
        self.textArea = [0, 0, 0, 0] #Xmin, Ymin, Xmax, Ymax
        self.compileArea = [0, 0, 0, 0]
        self.fontSize = 20
        self.textEditor = TextEditor(self.sPos[2]*0.85, self.sPos[3]*0.8, [44, 62, 80], self.fontSize, self.main)
        self.compileButton = pygame.Surface([self.sPos[2]*0.3, self.sPos[3]*0.08])
        self.compileHover = False
        self.setCompileButton(False)

    def testForCompile(self):
        if self.compileHover:
            print('compilation...')
            self.main.interpreter.compile(self.textEditor.getText())
            print('fait')

    def setCompileButton(self, hovered):
        self.compileHover = hovered
        self.compileButton.fill([39, 174, 96])
        if not hovered:
            pygame.draw.rect(self.compileButton, [46, 204, 113], [5, 5, self.compileButton.get_width()-10, self.compileButton.get_height()-10])
            text = pygame.font.SysFont('Calibri', 20, True).render('Compiler', True, [40, 40, 40])
        else:
            pygame.draw.rect(self.compileButton, [46, 204, 113], [7, 7, self.compileButton.get_width()-14, self.compileButton.get_height()-14])
            text = pygame.font.SysFont('Calibri', 20, True).render('Compiler', True, [20, 20, 20])
        self.compileButton.blit(text, [self.compileButton.get_width()/2-text.get_width()/2, self.compileButton.get_height()/2-text.get_height()/2])

    def tooglePanel(self):
        if self.level == 1:
            self.level = 0.1
        else:
            self.level = 1

    def resize(self):
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]
        self.toogleButtonArea = [self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2]-self.sPos[2]*0.05, self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2]+self.sPos[2]*0.05] #minimum / maximum
        self.textEditor.setSize(self.sPos[2]*0.85, self.sPos[3]*0.8)
        self.textArea = [
            self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2],
            self.sPos[1]+self.sPos[3]*0.05,
            self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85,
            self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8] #Xmin, Ymin, Xmax, Ymax
        self.compileArea = [
            self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85-self.compileButton.get_width(),
            self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8+10,
            self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85,
            self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8+10+self.compileButton.get_height()] #Xmin, Ymin, Xmax, Ymax

    def refresh(self, dt):
        if not(self.curLevel > self.level-0.001 and self.curLevel < self.level+0.001):
            self.curLevel += (self.level-self.curLevel)*dt*8
            self.toogleButtonArea = [self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2]-self.sPos[2]*0.05, self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2]+self.sPos[2]*0.05] #minimum / maximum
            self.textArea = [
                self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2],
                self.sPos[1]+self.sPos[3]*0.05,
                self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85,
                self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8] #Xmin, Ymin, Xmax, Ymax
            self.compileArea = [
                self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85-self.compileButton.get_width(),
                self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8+10,
                self.sPos[0]+self.sPos[2]*1.1-self.curLevel*self.sPos[2]+self.sPos[2]*0.85,
                self.sPos[1]+self.sPos[3]*0.05+self.sPos[3]*0.8+10+self.compileButton.get_height()] #Xmin, Ymin, Xmax, Ymax
        pygame.draw.ellipse(
            self.main.screen.window,
            [52, 73, 94],
            [self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2]-self.sPos[2]*0.05, self.sPos[3]*0.4, self.sPos[2]*0.2, self.sPos[3]*0.2])
        pygame.draw.rect(
            self.main.screen.window,
            [52, 73, 94],
            [self.sPos[0]+self.sPos[2]-self.curLevel*self.sPos[2], self.sPos[1], self.curLevel*self.sPos[2]+2, self.sPos[3]+2])
        self.main.screen.window.blit(self.textEditor.getSurface(dt), [self.sPos[0]+1+self.sPos[2]*1.1-self.curLevel*self.sPos[2], self.sPos[1]+self.sPos[3]*0.05])
        self.main.screen.window.blit(self.compileButton, [self.sPos[0]+1+self.sPos[2]*1.95-self.curLevel*self.sPos[2]-self.compileButton.get_width(), self.sPos[1]+self.sPos[3]*0.85+10])

class LeftPanel:
    def __init__(self, main, x, y, xSize, ySize):
        self.main = main
        self.x, self.y = x, y
        self.xSize, self.ySize = xSize, ySize
        self.curLevel = 0 #Level entre 0 et 1 (panneau déplié [1] ou non [0])
        self.level = 0.1  #target du level (pour faire les animations)
        self.toogleButtonArea = [0, 0]
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]

    def tooglePanel(self):
        if self.level == 1:
            self.level = 0.1
        else:
            self.level = 1

    def resize(self):
        self.sPos = [
            self.x*self.main.screen.dimensions[0], self.y*self.main.screen.dimensions[1],
            self.xSize*self.main.screen.dimensions[0], self.ySize*self.main.screen.dimensions[1]]
        self.toogleButtonArea = [self.sPos[0]+self.curLevel*self.sPos[2]-self.sPos[2]*0.05, self.sPos[0]+self.curLevel*self.sPos[2]+self.sPos[2]*0.05] #minimum / maximum

    def refresh(self, dt):
        if not(self.curLevel > self.level-0.001 and self.curLevel < self.level+0.001):
            self.curLevel += (self.level-self.curLevel)*dt*8
            self.toogleButton = [self.sPos[0]+self.curLevel*self.sPos[2]-self.sPos[2]*0.05, self.sPos[0]+self.curLevel*self.sPos[2]+self.sPos[2]*0.05] #minimum / maximum
        pygame.draw.ellipse(
            self.main.screen.window,
            [52, 73, 94],
            [self.sPos[0]+self.curLevel*self.sPos[2]-self.sPos[2]*0.15, self.sPos[3]*0.4, self.sPos[2]*0.2, self.sPos[3]*0.2])
        pygame.draw.rect(
            self.main.screen.window,
            [52, 73, 94],
            [self.sPos[0]-2, self.sPos[1], self.curLevel*self.sPos[2]+2, self.sPos[3]+2])
        pygame.draw.rect(
            self.main.screen.window,
            [44, 62, 80],
            [self.sPos[0]-self.sPos[2]*0.95+self.sPos[2]*self.curLevel, self.sPos[1]+self.sPos[3]*0.05, self.sPos[2]*0.85, self.sPos[3]*0.9])