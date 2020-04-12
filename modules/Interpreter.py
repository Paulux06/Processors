import time, sys, importlib
home = None
def getMain():
    return home

class Interpreter:
    def __init__(self, main):
        self.main = main
        global home
        home = main
        self.KEYWORDS = ['if', 'for', 'switch', 'break', 'case', 'default', 'while', 'var']
        self.NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.FUNCTIONS = ['forward ', 'backward ', 'turnLeft ', 'turnRight ', 'isAppleNear ', 'isMonsterNear ', 'random ']
        self.code = ''
        self.compiledCode = None
        self.lapse = 1
        self.deltaTime = 0
        self.step = 0
    
    def compile(self, code):
        cd = code.split('\r\n')
        self.code = 'from modules.tempHelp import *\ndef run():\n'
        progress = 0
        for line in cd:
            if len(line) > 0:
                self.code += '    ' + line + '\n'
                i = 0
                while line[i] == ' ':
                    i += 1
                p = len(line)-1
                while line[p] == ' ':
                    p -= 1
                if line[p] == ':':
                    i += 4
                self.code += ' '*(i+4) + 'yield '+str(progress)+'\n'
            progress += 1
        self.code += '    return True'
        f = open('./modules/temp.py', 'w')
        f.write(self.code)
        f.close()

    def openCode(self):
        try:
            import modules.temp
            self.compiledCode = modules.temp.run()
            f = open('./modules/temp.py', 'r')
            s = f.read()
            f.close()
            s = s[42:len(s)].split('\n')
            for e in range(len(s)):
                s[e] = s[e][4:len(s[e])]
            s = s[0:len(s)-1]
            s = s[0:len(s):2]
            self.main.screen.rightPanel.textEditor.data = s
        except:
            pass

    def refresh(self, dt):
        self.deltaTime += dt
        if self.deltaTime > self.lapse:
            self.deltaTime = 0
            try:
                self.step = next(self.compiledCode)
            except:
                try:
                    import modules.temp
                    importlib.reload(modules.temp)
                    self.compiledCode = modules.temp.run()
                    self.step = 0
                except:
                    print('Erreur de compilation !')
                    self.compiledCode = self.demo()

    def demo(self):
        print('Interpreter waiting ...')
        yield 1
        print('1 ...')
        yield 1
        print('2 ...')
        yield 1
        print('3 ...')
        yield 1