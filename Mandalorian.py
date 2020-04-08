from board import *
import time


class Mando():
    def __init__(self, x, y, obj):
        self.xc = x
        self.yc = y
        self.__shape = [["/", 'O', "\\"], [" ", "M", " "], ["^", " ", "^"]]
        self.__shape2 = [["|", 'O', "|"], [" ", "S", " "], ["^", " ", "^"]]
        self.coins = 0
        self.__mandoPositions = set()
        self.__lives = 3
        self.__shield = 0  # boolean to tell if mando Has shield
        self.__shieldstartTime = 0  # shield start time
        self.__shielddownTime = 0  # shield downtime
        self.set_position(obj, self.xc, self.yc)

    def set_position(self, obj, x, y):
        if (x <= 2):
            self.__mandoPositions = set()
            for i in range(2, 2+3):
                for j in range(self.yc, self.yc+3, 1):
                    if(self.__shield == 0):
                        obj.grid[i][j] = self.__shape[i-self.xc][j-self.yc]
                    else:
                        obj.grid[i][j] = self.__shape2[i-self.xc][j-self.yc]
                    self.__mandoPositions.add((i, j))
                    # print(obj.grid[i][j])
            self.xc = 2
            self.yc = y
        else:
            self.__mandoPositions = set()

            for i in range(self.xc, self.xc+3):
                for j in range(self.yc, self.yc+3, 1):
                    if(self.__shield == 0):
                        obj.grid[i][j] = self.__shape[i-self.xc][j-self.yc]
                    else:
                        obj.grid[i][j] = self.__shape2[i-self.xc][j-self.yc]

                    self.__mandoPositions.add((i, j))
                    # print(obj.grid[i][j])
            self.xc = x
            self.yc = y

    def disappear_mando(self, obj):
        for i in range(self.xc-1, self.xc+3):
            for j in range(self.yc-1, self.yc+4, 1):
                obj.grid[i][j] = " "

                # print(obj.grid[i][j])

    def mandopos(self):
        return self.__mandoPositions

    def decreaseLives(self):
        if (self.__shield == 0):
            self.__lives -= 1

    def activateShield(self):
        self.__shield = 1
        self.__shieldstartTime = time.time()

    def deactivateShield(self):
        self.__shield = 0
        self.__shielddownTime = time.time()

    def startTime(self):
        return self.__shieldstartTime

    def downTime(self):
        return self.__shielddownTime

    def shield(self):
        return self.__shield

    @property
    def xco(self):
        return self.xc

    @xco.setter
    def xco(self, a):
        self.xc = a

    @property
    def yco(self):
        return self.yc

    @yco.setter
    def yco(self, a):
        self.yc = a

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, a):
        self.__lives = a

#a = Generate(40,100)
# a.genGround()
# a.genBeams()

# a.printBoard()

#b = Mando(1,1,a)

# bounds
# right most on top of ground (35,97)
# right most highest point (1,97)
# leftmost on top of ground (35,1)
# leftmost on highest point (1,1)


# a.printit()
