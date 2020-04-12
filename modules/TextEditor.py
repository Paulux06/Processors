import pygame, clipboard

class TextEditor:
    def __init__(self, xSize, ySize, bg, fontSize, main):
        self.xSize, self.ySize = xSize, ySize
        self.main = main
        self.bg = bg
        self.fontSize = fontSize
        self.data = ["#Ecris ton code ici ! (En python)"]
        self.font = pygame.font.SysFont('Consolas', self.fontSize)
        self.fontHeight = self.font.size(' ')[1]
        self.fontWidth = self.font.size(' ')[0]
        self.surf = pygame.Surface([xSize, ySize])
        self.lastHighlight = 0
        #              x  y
        self.scroll = [0, 0]
        self.curScroll = [0, 0]
        self.cursor = [0, 0, True]
        #                x1 y1 x2 y2
        self.selected = [0, 0, 0, 0]
        self.deltaTime = 0
        self.shiftPressed = False
        self.compiled = True

    def setSize(self, xSize, ySize):
        self.xSize, self.ySize = xSize, ySize
        self.surf = pygame.Surface([xSize, ySize])
        self.draw()

    def setShift(self, pressed=False):
        self.shiftPressed = pressed
        if pressed:
            self.selected[2] = self.cursor[0]
            self.selected[3] = self.cursor[1]
            self.selected[0] = self.cursor[0]
            self.selected[1] = self.cursor[1]

    def addLetter(self, letter):
        self.compiled = False
        self.cursor[2] = False
        self.deltaTime = 1
        if not letter == '':
            if not self.selected[0:2] == self.selected[2:4]:
                self.eraseSeletedContent()
            self.data[self.cursor[1]] = self.data[self.cursor[1]][0:self.cursor[0]] + letter + self.data[self.cursor[1]][self.cursor[0]:len(self.data[self.cursor[1]])]
            self.cursor[0] += len(letter)
        self.draw()

    def removeLetter(self):
        self.compiled = False
        if self.selected[0:2] == self.selected[2:4]:
            self.cursor[2] = False
            self.deltaTime = 1
            if self.cursor[0] > 0:
                self.data[self.cursor[1]] = self.data[self.cursor[1]][0:self.cursor[0]-1] + self.data[self.cursor[1]][self.cursor[0]:len(self.data[self.cursor[1]])]
                self.cursor[0] -= 1
            else:
                if self.cursor[1] > 0:
                    self.data[self.cursor[1]-1] += self.data[self.cursor[1]]
                    for i in range(len(self.data[self.cursor[1]])+1):
                        self.moveCursor([-1, 0])
                    self.data.pop(self.cursor[1]+1)
            self.draw()
        else:
            self.eraseSeletedContent()

    def enter(self):
        if not self.selected[0:2] == self.selected[2:4]:
            self.eraseSeletedContent()
        self.data.insert(self.cursor[1]+1, self.data[self.cursor[1]][self.cursor[0]:len(self.data[self.cursor[1]])])
        self.data[self.cursor[1]] = self.data[self.cursor[1]][0:self.cursor[0]]
        self.moveCursor([1, 0])
        self.draw()

    def eraseSeletedContent(self):
        if not self.selected[0:2] == self.selected[2:4]:
            if self.selected[1] == self.selected[3]:
                self.data[self.selected[1]] = self.data[self.selected[1]][0:min(self.selected[0], self.selected[2])] + self.data[self.selected[1]][max(self.selected[0], self.selected[2]):len(self.data[self.selected[1]])]

            if self.selected[1] < self.selected[3]:
                self.data[self.selected[1]] = self.data[self.selected[1]][0:self.selected[0]]
                self.data[self.selected[1]] += self.data[self.selected[3]][self.selected[2]:len(self.data[self.selected[3]])]
                for e in range(self.selected[1]+1, self.selected[3]+1):
                    self.data.remove(self.data[self.selected[1]+1])

            if self.selected[1] > self.selected[3]:
                self.data[self.selected[3]] = self.data[self.selected[3]][0:self.selected[2]]
                self.data[self.selected[3]] += self.data[self.selected[1]][self.selected[0]:len(self.data[self.selected[1]])]
                for e in range(self.selected[3]+1, self.selected[1]+1):
                    self.data.remove(self.data[self.selected[3]+1])

            self.cursor[0], self.cursor[1] = min(self.selected[0], self.selected[2]), min(self.selected[1], self.selected[3])
            self.selected = [0, 0, 0, 0]

    def resetSelection(self):
        self.selected = [0, 0, 0, 0]
        self.shiftPressed = False

    def getText(self):
        self.compiled = True
        temp = self.data.copy()
        for l in range(len(self.data)):
            i = 0
            for char in self.data[l]:
                if char == '#':
                    self.data[l] = self.data[l][0:i]
                    break
                i += 1
        t = ''
        for l in range(0, len(self.data)):
            t += self.data[l]
            if l < len(self.data)-1:
                t += '\r\n'
        self.data = temp.copy()
        del temp
        return t

    def supprLetter(self):
        self.moveCursor([1, 0])
        self.removeLetter()
        self.draw()

    def cursorEnd(self):
        self.cursor[2] = False
        self.deltaTime = 1
        self.cursor[0] = len(self.data[self.cursor[1]])
        if self.shiftPressed:
            self.setSelection()
        self.draw()

    def cursorStart(self):
        self.cursor[2] = False
        self.deltaTime = 1
        self.cursor[0] = 0
        if self.shiftPressed:
            self.setSelection()
        self.draw()

    def copy(self):
        s = ''
        #copier le texte selectionné + clipboard.copy(s)

    def paste(self):
        s = clipboard.paste()
        try:
            s = s.split('\r\n')
            for line in s:
                l = line.split(' ')
                for word in l:
                    for letter in word:
                        self.addLetter(letter)
                    self.addLetter(' ')
                self.enter()
        except:
            pass

    def cut(self):
        self.copy()
        self.eraseSeletedContent()

    def selectAll(self):
        self.selected = [0, 0, 0, 0]
        self.cursor[0:2] = [0, 0]
        self.shiftPressed = True
        self.moveCursor([0, -(len(self.data)-1)])
        self.cursorEnd()
        self.shiftPressed = False

    def setSelection(self):
        self.selected[2] = self.cursor[0]
        self.selected[3] = self.cursor[1]

    def moveCursor(self, vector=[0, 0]):
        self.cursor[2] = False
        self.deltaTime = 1
        self.cursor[0] += vector[0]
        self.cursor[1] -= vector[1]
        if self.cursor[1] < 0: self.cursor[1] = 0
        if self.cursor[1] > len(self.data)-1: self.cursor[1] = len(self.data)-1
        if self.cursor[0] < 0: 
            if self.cursor[1] > 0:
                self.cursor[1] -= 1
                self.cursorEnd()
            else:
                self.cursor[0] = 0
        if self.cursor[0] > len(self.data[self.cursor[1]]):
            if not vector[1] == 0:
                self.cursorEnd()
            elif self.cursor[1] < len(self.data)-1:
                self.cursor[1] += 1
                self.cursorStart()
            else:
                self.cursorEnd()
        if self.shiftPressed:
            self.setSelection()
        return True
    
    def draw(self):
        self.surf.fill(self.bg)
        if not self.selected[0:2] == self.selected[2:4]:
            if self.selected[1] == self.selected[3]:
                pygame.draw.rect(self.surf, [41, 128, 185], [
                    self.fontWidth*len(self.data[self.selected[1]][0:min(self.selected[0], self.selected[2])])+self.curScroll[0], self.selected[1]*self.fontHeight+self.curScroll[1],
                    self.fontWidth*len(self.data[self.selected[1]][min(self.selected[0], self.selected[2]):max(self.selected[0], self.selected[2])]),
                    self.fontHeight])

            if self.selected[1] < self.selected[3]:
                pygame.draw.rect(self.surf, [41, 128, 185], [ #haut
                    self.fontWidth*len(self.data[min(self.selected[1], self.selected[3])][0:self.selected[0]])+self.curScroll[0], self.fontHeight*min(self.selected[1], self.selected[3])+self.curScroll[1],
                    self.fontWidth*len(self.data[min(self.selected[1], self.selected[3])][self.selected[0]:len(self.data[min(self.selected[1], self.selected[3])])]),
                    self.fontHeight])
                for e in range(self.selected[1]+1, self.selected[3]):
                    pygame.draw.rect(self.surf, [41, 128, 185], [ #milieu
                        self.curScroll[0], self.fontHeight*e+self.curScroll[1],
                        self.fontWidth*len(self.data[e][0:len(self.data[e])]), self.fontHeight])
                pygame.draw.rect(self.surf, [41, 128, 185], [ #bas
                    self.curScroll[0], self.fontHeight*max(self.selected[1], self.selected[3])+self.curScroll[1],
                    self.fontWidth*len(self.data[max(self.selected[1], self.selected[3])][0:self.selected[2]]),
                    self.fontHeight])

            if self.selected[1] > self.selected[3]:
                pygame.draw.rect(self.surf, [41, 128, 185], [ #haut
                    self.fontWidth*len(self.data[min(self.selected[1], self.selected[3])][0:self.selected[2]])+self.curScroll[0], self.fontHeight*min(self.selected[1], self.selected[3])+self.curScroll[1],
                    self.fontWidth*len(self.data[min(self.selected[1], self.selected[3])][self.selected[2]:len(self.data[min(self.selected[1], self.selected[3])])]),
                    self.fontHeight])
                for e in range(self.selected[3]+1, self.selected[1]):
                    pygame.draw.rect(self.surf, [41, 128, 185], [ #milieu
                        self.curScroll[0], self.fontHeight*e+self.curScroll[1],
                        self.fontWidth*len(self.data[e][0:len(self.data[e])]), self.fontHeight])
                pygame.draw.rect(self.surf, [41, 128, 185], [ #bas
                    self.curScroll[0], self.fontHeight*max(self.selected[1], self.selected[3])+self.curScroll[1],
                    self.fontWidth*len(self.data[max(self.selected[1], self.selected[3])][0:self.selected[0]]),
                    self.fontHeight])
        y = 0
        for txt in self.data:
            self.surf.blit(
                self.font.render(txt, True, [255, 255, 255]),
                [self.curScroll[0], self.curScroll[1]+y*self.fontHeight])
            y += 1

    def refresh(self, dt):
        if self.curScroll[0] < self.scroll[0]-1 or self.curScroll[0] > self.scroll[0]+1:
            self.curScroll[0] += (self.scroll[0]-self.curScroll[0])/5
            self.draw()
        if self.curScroll[1] < self.scroll[1]-1 or self.curScroll[1] > self.scroll[1]+1:
            self.curScroll[1] += (self.scroll[1]-self.curScroll[1])/5
            self.draw()
        self.deltaTime += dt
        if self.deltaTime > 0.5:
            self.deltaTime = 0
            self.cursor[2] = not self.cursor[2]
            if self.cursor[2]:
                col = [255, 255, 255]
            else:
                col = self.bg
            pygame.draw.rect(self.surf, col, [
                self.curScroll[0] + self.fontWidth*len(self.data[ self.cursor[1] ][0:self.cursor[0]]),
                self.curScroll[1] + self.fontHeight*self.cursor[1], 2, self.fontHeight])
        if False:
            try:
                self.surf.blit(self.font.render(self.data[self.lastHighlight], True, [255, 255, 255], self.bg), [self.scroll[0], self.scroll[1]+self.fontHeight*self.lastHighlight])
                self.lastHighlight = self.main.interpreter.step
                s = self.font.render(self.data[self.lastHighlight], True, [255, 255, 255], [255, 44, 80])
                self.surf.blit(s, (0,self.lastHighlight*self.fontHeight+self.scroll[1]))
            except:
                pass

    def scrollBy(self, vector=[0, 0]):
        self.scroll[0] += vector[0]
        self.scroll[1] += vector[1]
        if self.scroll[0] > 0: self.scroll[0] = 0
        if self.scroll[1] > 0: self.scroll[1] = 0

    def getSurface(self, dt):
        self.refresh(dt)
        return self.surf