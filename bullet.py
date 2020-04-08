import time
class Bullet:
    def __init__(self,x,y,a,Boss):
        self._shape = ['','~','>']
        self.__startTime = 0 
        self.__x  = x
        self.__y = y 
        self._cord = set() #coordinates that the bullet occupies
        self._obj = a
        self._boss = Boss
    def set_position(self,obj,x,y):
        self.__x = x
        self.__y = y
        self._cord = set()
        if(y+3 > obj.column()-2):
            pass
        else:
            obj.removeCollisionList((x,y))
            for i in range (y,y+3):
                try:
                    obj.grid[x][i] = self._shape[i-y]
                    self._cord.add((x,i))
                    temp = set()
                    temp.add((x,i))
                    length = len(temp.intersection(obj.colisionList()))
                    if(length>0):
                        obj.removeCollisionList((x,i))
                    
                    length = len(temp.intersection(self._boss.coordinates()))
                    if(length > 0):
                        self._boss.decreaseLives()
                    temp.discard((x,i))

                except IndexError:
                    self.remove(obj)
    def remove(self,obj):
        for i in range(self.__y,self.__y+3):
            try:
                obj.grid[self.__x][i] = " "
            except:
                pass
    def move(self):
        now = time.time()
        if (int(now-self.__startTime) <= 10):
            self.remove(self._obj)
            self.set_position(self._obj,self.__x,self.__y+2)
        else:
            self.remove(self._obj)
    def shoot(self,obj,x,y):
        self.__startTime = time.time()
        self.set_position(obj,x,y)