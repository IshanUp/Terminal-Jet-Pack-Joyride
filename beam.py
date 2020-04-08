class beam:
    def __init__(self):
        self.__horb = '\33[36m\33[1m' + '-' + '\033[39m'
        self.__vertb = '\33[36m\33[1m' + '|' + '\033[39m'
        self.__slantb = '\33[36m\33[1m' + '\\' + '\033[39m'
    def horbeam(self):
        return self.__horb
    def vertbeam(self):
        return self.__vertb