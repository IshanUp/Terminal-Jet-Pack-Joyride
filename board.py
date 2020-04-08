from random import randint, seed
from shield import *
from magnet import *
from speed import *
from beam import *
from coin import *
import time
import os
import random
from colorama import *
init(autoreset=True)
# see how to make things into private variables


class Board:

    def __init__(self, rows, columns):
        self._rows = rows  # 40
        self._columns = columns  # 100
        self.grid = []

    def create(self):  # create the grid
        for i in range(self._rows):
            self.temp = []
            for j in range(self._columns):
                self.temp.append(" ")
            self.grid.append(self.temp)

    def printit(self, x):
        temp = ""
        for d in range(self._rows):
            for s in range(x, 100+x):
                temp += self.grid[d][s]
            temp += "\n"
        print(temp)

        # for i in range (self._rows):
        #   for j in range (self._columns):
        #      print(self.grid[i][j],end = " ")
        # print()
    def colnum(self):
        return self._columns  # actually rownum related to x axis
# inheritance


class Generate(Board):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        super().create()
        # array of locations where something in which we should not collide (like beams) are __placed
        self.__placed = set()
        self.__coins = set()  # array of locations where __coins are
        self.__boosts = set()  # array of locations where boosts are located
        self.__magnets = set()
        self.__rightmag = set()
        self.shields = []
        self.__speed = 0  # tells if speed booster is activated
        self.__speedTime = 0  # records time at which speed booster was activated
        # super().printit()

    def genGround(self):
        temp = []
        for i in range(self._columns):
            temp.append(Fore.GREEN + "Y")
        self.grid[self._rows-1] = temp
        self.grid[self._rows-2] = temp
        # print(*self.grid)
        # super().printit()

    def genSky(self):
        temp = []
        for i in range(self._columns):
            temp.append(Fore.BLUE+"@"+Fore.RESET)
        self.grid[1] = temp

    def genBeams(self):
        symbol = '\33[36m\33[1m' + '\\' + '\033[39m'
        it = 0
        # placing horizontal beams
        horbeam = []
        with open("./bg/horbeam.txt") as obj:
            for line in obj:
                line = line.strip("\n").split(" ")
                for x in line:
                    horbeam.append(x)
        beamobj = beam()

        while (it < randint(8, 12)):
            it += 1
            # print(*self.__placed)
            rowVal = randint(4, self._rows - 10)
            colVal = randint(4, self._columns - 10)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(self.__placed.intersection(temp))
            if(length > 0):
                continue
            else:
                for i in range(0, len(horbeam)):
                    self.__placed.add((rowVal, colVal+i))
                    self.grid[rowVal][colVal+i] = beamobj.horbeam()  # "-"
            temp.discard((rowVal, colVal))
            #print(rowVal, end = " ")
            # print(colVal+i)

        # print(horbeam)

        # print(self.grid)
        # super().printit()

        # printing verticle beams

        it = 0

        while(it < randint(3, 5)):
            it += 1
            rowVal = randint(2, self._rows-10)
            colVal = randint(2, self._columns - 2)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(self.__placed.intersection(temp))
            temp.discard((rowVal, colVal))
            if length > 0:
                continue
            else:
                for i in range(7):
                    temp = set()
                    temp.add((rowVal+i, colVal))
                    length = len(self.__placed.intersection(temp))
                    if(length > 0):
                        break
                    self.__placed.add((rowVal+i, colVal))
                    self.grid[rowVal+i][colVal] = beamobj.vertbeam()
                    temp.discard((rowVal, colVal))
        # printing 45 degree beams

        it = 0

        while (it < randint(8, 12)):
            it += 1
            rowVal = randint(2, self._rows-10)
            colVal = randint(2, self._columns - 10)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(self.__placed.intersection(temp))
            temp.discard((rowVal, colVal))

            if length > 0:
                continue

            else:
                for i in range(4):  # 4 is beam length
                    temp = set()
                    temp.add((rowVal+i, colVal+i))
                    length = len(self.__placed.intersection(temp))
                    if length > 0:
                        break
                    self.__placed.add((rowVal+i, colVal+i))

                    try:
                        self.grid[rowVal+i][colVal+i] = symbol
                    except:
                        break

                    temp.discard((rowVal, colVal))

        # __coins
        coinobj = coin()
        while(it < randint(40, 80)):
            it += 1
            rowVal = randint(2, self._rows-1)
            colVal = randint(2, self._columns-1)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(temp.intersection(self.__placed)) + \
                len(temp.intersection(self.__coins))
            if length > 0:
                continue
            else:
                self.__coins.add((rowVal, colVal))
                self.grid[rowVal][colVal] = coinobj.coinsym()  # "$"
            temp.discard((rowVal, colVal))

    def genBoost(self):
        boostobj = speed()
        it = 0
        while(it < randint(11, 20)):
            it += 1
            rowVal = randint(2, self._rows-15)
            colVal = randint(2, self._columns-1)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(temp.intersection(self.__placed)) + len(
                temp.intersection(self.__coins)) + len(temp.intersection(self.__boosts))
            if length > 0:
                continue
            else:
                self.__boosts.add((rowVal, colVal))
                self.__boosts.add((rowVal, colVal-1))
                self.__boosts.add((rowVal, colVal+1))
                self.__boosts.add((rowVal+1, colVal))
                self.__boosts.add((rowVal-1, colVal))
                self.grid[rowVal][colVal] = boostobj.speedsym()  # "B"

            temp.discard((rowVal, colVal))

    def genMag(self):
        magobj = magnet()
        it = 0
        while(it < randint(10, 15)):
            it += 1
            rowVal = randint(2, 4)
            colVal = randint(5, self._columns-5)
            temp = set()
            temp.add((rowVal, colVal))
            length = len(temp.intersection(self.__placed)) + len(temp.intersection(self.__coins)) + \
                len(temp.intersection(self.__boosts)) + \
                len(temp.intersection(self.__magnets))
            if length > 0:
                continue
            else:
                self.__magnets.add((rowVal, colVal))
                for i in range(rowVal+2, rowVal+14):
                    for j in range(colVal+2, colVal+14):
                        self.__magnets.add((i, j))

                for i in range(rowVal+2, rowVal+14):
                    for j in range(colVal-14, colVal-2):
                        self.__rightmag.add((i, j))
                self.grid[rowVal][colVal] = magobj.magsym()  # "B"

        def genShield():
            shieldobj = shield()
            it = 0
            while(it < randint(5, 10)):
                it += 1
                rowVal = randint(2, self._rows-15)
                colVal = randint(5, self._columns-5)
                temp = set()
                temp.add((rowVal, colVal))
                length = len(self.shields.intersection(temp))
                if(rowVal, colVal) in self.__placed or (rowVal, colVal) in self.__coins or (rowVal, colVal) in self.__boosts or(rowVal, colVal) in self.__magnets or length > 0:
                    continue
                else:
                    self.shields.add((rowVal, colVal))
                    self.grid[rowVal][colVal] = shieldobj.sym()  # "B"
                temp.discard((rowVal, colVal))

    def boostList(self):
        return self.__boosts

    def removeBoostList(self, y):
        self.__boosts.discard(y)

    def collisonLoc(self):
        return self.__placed

    def coinsLoc(self):
        return self.__coins

    def printBoard(self):
        super().printit

    def colisionList(self):
        return self.__placed

    def coinsList(self):
        return self.__coins

    def shieldsList(self):
        return self.shields

    def removeShieldsList(self, y):
        self.__shields.discard(y)

    def removeCoinsList(self, y):
        self.__coins.discard(y)

    def removeCollisionList(self, y):
        self.__placed.discard(y)

    def magList(self):
        return self.__magnets

    def rightmagList(self):
        return self.__rightmag

    def speedUp(self, y):
        self.__speed = 1
        self.__speedTime = time.time()

    def column(self):
        return self._columns


#a = Generate(40,100)
# a.genGround()
# a.genBeams()
# a.printit()
# y=a.grid
