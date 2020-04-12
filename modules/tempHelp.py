from modules.Interpreter import getMain
from random import randint as rd
import asyncio
main = getMain()

def forward():
    main.gameMaster.player.forward()
    return True

def backward():
    main.gameMaster.player.backward()
    return True

def turnLeft():
    main.gameMaster.player.turnLeft()
    return True

def turnRight():
    main.gameMaster.player.turnRight()
    return True

def isAppleNear():
    return main.gameMaster.player.isAppleNear()

def isMonsterNear():
    return main.gameMaster.player.isMonsterNear()

def random(min, max):
    return rd(min, max)