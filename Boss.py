from board import *
from bullet import *
import time

#polymorphism and inheritance


class bossBull(Bullet):
    def __init__(self, x, y, a, Mando):
        super().__init__(x, y, a, Mando)
        self.__shape = ['(', ')', ' ']
        self.startTime = 0
        self.__xc = x
        self.__yc = y
        self.__cord = set()
        self.__boss = Mando
        self.__obj = a

    def set_position(self, obj, x, y):
        self.__xc = x
        self.__yc = y
        self.__cord = set()

        obj.removeCollisionList((x, y))
        for i in range(y, y+3):
            try:
                obj.grid[x][i] = self.__shape[i-y]
                self.__cord.add((x, i))
                temp = set()
                temp.add((x, i))
                length = len(temp.intersection(obj.colisionList()))
                if(length > 0):
                    obj.removeCollisionList((x, i))
                    #length = len(temp.intersection(self.__boss.mandopos()))
                    # if(length > 0):
                    #   self.__boss.decreaseLives()
                    #  if self.__boss.lives() <=0  or self.__boss.lives()==33:
                    #     quit()
                    temp.discard((x, i))

            except IndexError:
                self.remove(obj)

    def move(self):
        now = time.time()
        if (int(now - self.startTime) <= 10):
            self.remove(self.__obj)
            self.set_position(self.__obj, self.__xc, self.__yc-2)
        else:
            self.remove(self.__obj)

    def shoot(self, obj, x, y):
        self.startTime = time.time()
        self.set_position(obj, x, y)

    def remove(self, obj):
        for i in range(self.__yc, self.__yc+3):
            try:
                obj.grid[self.__xc][i] = " "
            except:
                pass

    def bulletcord(self):
        return self.__cord


class Bossman():
    def __init__(self, x, y, groundobj, mando):
        self.__xc = x
        self.__yc = y
        # self.__shape = [ ["-", '-', "|"],
        #                [" -", "\\", "|"],
        #               ["A", "A", "-"]
        #             ]
        self.__shape = [[' ', ' ', '\\', ' ', ' ', ' ', '/'],
                        [' ', ' ', ')', '\\', '_', '/', '(', ' ', ' '],
                        [' ', '(', '/', '\\', '|', '/', '\\', ')'],
                        [' ', ' ', '\\', '`', '|', "'", '/', ],
                        [' ', ' ', ' ', '\\', '|', '/', ],
                        [' ', ' ', ' ', ' ', 'V', ]]

        self.set_position(groundobj, self.__xc, self.__yc)
        self._cord = set()
        self.__lives = 3
        self.__starttime = 0
        self.__snowballs = []
        self.__mando = mando
        self.__obj = groundobj

    def set_position(self, obj, x, y):
        self.__xc = x
        self.__yc = y
        self._cord = set()
        if(self.__xc <= 3):
            self.__xc = 3

        for i in range(6):
            for j in range(len(self.__shape[i])):
                obj.grid[i+self.__xc][j+self.__yc] = self.__shape[i][j]
                self._cord.add((i+self.__xc, j+self.__yc))

    def disappear(self, obj):
        for i in range(6):
            for j in range(len(self.__shape[i])):
                obj.grid[i+self.__xc][j+self.__yc] = " "
        '''
         for i in range (self.__xc-1,self.__xc+3):
            for j in range(self.__yc-1,self.__yc+4,1):
                obj.grid[i][j] =" "
                #print(obj.grid[i][j])
        '''

    def coordinates(self):
        return self._cord

    def decreaseLives(self):
        if(time.time()-self.__starttime < 2):
            pass
        else:
            self.__starttime = time.time()
            self.__lives -= 1
        return self.__lives

    def bossShoot(self):
        snow = bossBull(self.__xc, self.__yc, self.__obj, self.__mando)
        snow.shoot(self.__obj, self.__xc, self.__yc - 3)
        self.__snowballs.append(snow)
        # for x in self.__snowballs:
        #   x.move()

    def bullmove(self):
        for x in self.__snowballs:
            x.move()

    @property
    def xco(self):
        return self.__xc

    @xco.setter
    def xco(self, a):
        self.__xc = a

    @property
    def yco(self):
        return self.__yc

    @yco.setter
    def yco(self, a):
        self.__yc = a

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
# b.disappear_mando(a)
# a.printit()
