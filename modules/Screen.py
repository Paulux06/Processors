import pygame, os, time
from modules.HUD import *
from modules.GameView import GameView
pygame.init()

class Screen:
    def __init__(self, main):
        self.window = pygame.display.set_mode()
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(int(self.window.get_width()*0.1))+","+str(int(self.window.get_height()*0.1))
        self.dimensions = [int(self.window.get_width()*0.8), int(self.window.get_height()*0.8)]
        self._dimensions = [self.window.get_width(), self.window.get_height()]
        self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        del os.environ['SDL_VIDEO_WINDOW_POS']
        self.main = main
        self.clock = pygame.time.Clock()
        self.fullscreen = False

        self.alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.keyboard = 'azerty'
        pygame.key.set_repeat(200, 30)

        self.scene = []
        self.deltaTime = 0
        self.lastTime = time.time()
        self.mPos = [0, 0] #position de souris
        self.mMvs = [0, 0] #mouvements de souris
        self.sensibility = 10
        self.shiftPressed = False
        self.ctrlPressed = False
        self.AltPressed = False

    def createGameInterface(self):
        self.leftPanel = LeftPanel(self.main, 0, 0, 0.4, 0.92)
        self.rightPanel = RightPanel(self.main, 0.6, 0, 0.4, 0.92)
        self.info = Info(self.main, 0, 0.92, 1, 0.08)
        self.gameView = GameView(self.main, 0, 0, 1, 1)
        self.scene.append(self.gameView)
        self.scene.append(self.leftPanel)
        self.scene.append(self.rightPanel)
        self.scene.append(self.info)
        self.gameView.createMap()

    def resize(self, w, h):
        if not self.fullscreen:
            self.dimensions = [w, h]
            self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
        for obj in self.scene:
            obj.resize()

    def getTime(self):
        return time.time()

    def getDeltaTime(self):
        return self.deltaTime

    def waitForFrame(self):
        self.clock.tick()
        return True

    def refresh(self):
        temps = time.time()
        self.deltaTime = temps-self.lastTime
        self.lastTime = temps
        self.window.fill([0, 0, 0])
        for obj in self.scene:
            obj.refresh(self.deltaTime)
        pygame.display.flip()
        return True

    def shutdown(self):
        pygame.quit()
        return True

    def processEvents(self):
        self.mPos = pygame.mouse.get_pos()
        self.mMvs = pygame.mouse.get_rel()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.main.mainrun = False
            if e.type == pygame.VIDEORESIZE:
                self.resize(e.w, e.h)
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LCTRL or e.key == pygame.K_RCTRL:
                    self.ctrlPressed = True
                if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                    self.shiftPressed = True
                    if self.mPos[0] > self.rightPanel.textArea[0] and self.mPos[0] < self.rightPanel.textArea[2] and self.mPos[1] > self.rightPanel.textArea[1] and self.mPos[1] < self.rightPanel.textArea[3]:
                        self.rightPanel.textEditor.setShift(True)
                if e.key == pygame.K_LALT or e.key == pygame.K_RALT:
                    self.AltPressed = True
                if e.key == pygame.K_CAPSLOCK:
                    self.shiftPressed = not self.shiftPressed

                if self.mPos[0] > self.rightPanel.textArea[0] and self.mPos[0] < self.rightPanel.textArea[2] and self.mPos[1] > self.rightPanel.textArea[1] and self.mPos[1] < self.rightPanel.textArea[3]:
                    self.doArrowStuff(e.key, 'right')
                    self.rightPanel.textEditor.addLetter(self.getKeyLetter(e.key))

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LCTRL or e.key == pygame.K_RCTRL:
                    self.ctrlPressed = False
                if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                    self.shiftPressed = False
                    if self.mPos[0] > self.rightPanel.textArea[0] and self.mPos[0] < self.rightPanel.textArea[2] and self.mPos[1] > self.rightPanel.textArea[1] and self.mPos[1] < self.rightPanel.textArea[3]:
                        self.rightPanel.textEditor.setShift(False)
                if e.key == pygame.K_LALT or e.key == pygame.K_RALT:
                    self.AltPressed = False      

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: #left click
                    if self.mPos[0] > self.rightPanel.toogleButtonArea[0] and self.mPos[0] < self.rightPanel.toogleButtonArea[1]:
                        self.rightPanel.tooglePanel()
                    self.rightPanel.testForCompile()
                    if self.mPos[0] > self.leftPanel.toogleButtonArea[0] and self.mPos[0] < self.leftPanel.toogleButtonArea[1]:
                        self.leftPanel.tooglePanel()
                if e.button == 2: #middle click
                    pass
                if e.button == 3: #right click
                    pass
                if e.button == 4: #up
                    if self.mPos[0] > self.rightPanel.textArea[0] and self.mPos[0] < self.rightPanel.textArea[2] and self.mPos[1] > self.rightPanel.textArea[1] and self.mPos[1] < self.rightPanel.textArea[3]:
                        if self.shiftPressed:
                            self.rightPanel.textEditor.scrollBy([self.sensibility, 0])
                        else:
                            self.rightPanel.textEditor.scrollBy([0, self.sensibility])
                if e.button == 5: #down
                    if self.mPos[0] > self.rightPanel.textArea[0] and self.mPos[0] < self.rightPanel.textArea[2] and self.mPos[1] > self.rightPanel.textArea[1] and self.mPos[1] < self.rightPanel.textArea[3]:
                        if self.shiftPressed:
                            self.rightPanel.textEditor.scrollBy([-self.sensibility, 0])
                        else:
                            self.rightPanel.textEditor.scrollBy([0, -self.sensibility])

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_F11:
                    a = self.dimensions
                    self.dimensions = self._dimensions
                    self._dimensions = a
                    if not self.fullscreen:
                        self.window = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
                    else:
                        self.window = pygame.display.set_mode(self.dimensions, pygame.RESIZABLE)
                    self.fullscreen = not self.fullscreen
        if self.mPos[0] < self.rightPanel.compileArea[2] and self.mPos[0] > self.rightPanel.compileArea[0] and self.mPos[1] < self.rightPanel.compileArea[3] and self.mPos[1] > self.rightPanel.compileArea[1]:
            if not self.rightPanel.compileHover: self.rightPanel.setCompileButton(True)
        else:
            if self.rightPanel.compileHover: self.rightPanel.setCompileButton(False)
        return True

    def doArrowStuff(self, key, side='right'):
        if side == 'right':
            if key == 8: #return
                self.rightPanel.textEditor.removeLetter()
            if key == 273: #up
                self.rightPanel.textEditor.moveCursor([0, 1])
            if key == 274: #down
                self.rightPanel.textEditor.moveCursor([0, -1])
            if key == 276: #left
                self.rightPanel.textEditor.moveCursor([-1, 0])
            if key == 275: #right
                self.rightPanel.textEditor.moveCursor([1, 0])
            if key == 279:
                self.rightPanel.textEditor.cursorEnd()
            if key == 278:
                self.rightPanel.textEditor.cursorStart()
            if key == 127:
                self.rightPanel.textEditor.supprLetter()
            if key == 13:
                self.rightPanel.textEditor.enter()
            if key == 27:
                self.rightPanel.textEditor.resetSelection()

    def getKeyLetter(self, key):
        l = ''
        print(key)
        if self.keyboard == 'qwerty':
            if key < 123 and key > 96:
                l = self.alphabet[key-97]
        if self.keyboard == 'azerty':
            if key == 113:
                l = 'a'
                if self.ctrlPressed:
                    self.rightPanel.textEditor.selectAll()
                    return ''
            if key == 119:
                l = 'z'
            if key == 122:
                l = 'w'
            if key == 97:
                l = 'q'
            if key == 59:
                l = 'm'
            if key > 97 and key < 123 and l == '':
                l = self.alphabet[key-97]
                if self.ctrlPressed:
                    if l == 'c':
                        l = ''
                        self.rightPanel.textEditor.copy()
                    if l == 'v':
                        l = ''
                        self.rightPanel.textEditor.paste()
                    if l == 'x':
                        l = ''
                        self.rightPanel.textEditor.cut()
        if key == 9:
            l = '    '
        if key == 32:
            l = ' '
        if key == 44:
            if self.shiftPressed:
                l = '.'
            else:
                l = ';'
        if key == 45:
            if self.shiftPressed:
                l = '°'
            else:
                if self.AltPressed:
                    l = ']'
                else:
                    l = ')'
        if key == 46:
            if self.shiftPressed:
                l = '/'
            else:
                l = ':'
        if key == 47:
            if self.shiftPressed:
                l = '§'
            else:
                l = '!'
        if key == 48:
            if self.shiftPressed:
                l = '0'
            else:
                if self.AltPressed:
                    l = '@'
                else:
                    l = 'à'
        if key == 49:
            if self.shiftPressed:
                l = '1'
            else:
                if self.AltPressed:
                    l = ''
                else:
                    l = '&'
        if key == 50:
            if self.shiftPressed:
                l = '2'
            else:
                if self.AltPressed:
                    l = '~'
                else:
                    l = 'é'
        if key == 51:
            if self.shiftPressed:
                l = '3'
            else:
                if self.AltPressed:
                    l = '#'
                else:
                    l = '"'
        if key == 52:
            if self.shiftPressed:
                l = '4'
            else:
                if self.AltPressed:
                    l = '{'
                else:
                    l = "'"
        if key == 53:
            if self.shiftPressed:
                l = '5'
            else:
                if self.AltPressed:
                    l = '['
                else:
                    l = '('
        if key == 54:
            if self.shiftPressed:
                l = '6'
            else:
                if self.AltPressed:
                    l = '|'
                else:
                    l = "-"
        if key == 55:
            if self.shiftPressed:
                l = '7'
            else:
                if self.AltPressed:
                    l = '`'
                else:
                    l = 'è'
        if key == 56:
            if self.shiftPressed:
                l = '8'
            else:
                if self.AltPressed:
                    l = '\\'
                else:
                    l = '_'
        if key == 57:
            if self.shiftPressed:
                l = '9'
            else:
                if self.AltPressed:
                    l = '^'
                else:
                    l = 'ç'
        if key == 60:
            if self.shiftPressed:
                l = '>'
            else:
                if self.AltPressed:
                    l = ''
                else:
                    l = '<'
        if key == 61:
            if self.shiftPressed:
                l = '+'
            else:
                if self.AltPressed:
                    l = '}'
                else:
                    l = '='
        if key == 92:
            if self.shiftPressed:
                l = '*'
            else:
                l = 'µ'
        if key == 109:
            if self.shiftPressed:
                l = '?'
            else:
                l = ','
        if self.shiftPressed:
            return l.upper()
        return l