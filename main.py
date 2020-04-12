from modules.Screen import Screen
from modules.GameMaster import GameMaster
from modules.Interpreter import Interpreter

class Main:
    def __init__(self):
        self.gameMaster = GameMaster(self)
        self.screen = Screen(self)
        self.screen.createGameInterface()
        self.interpreter = Interpreter(self)

        self.mainrun = True
        while self.mainrun:
            self.screen.processEvents()
            self.screen.waitForFrame()
            self.screen.refresh()
            self.interpreter.refresh(self.screen.deltaTime)
            
        self.screen.shutdown()

main = Main()