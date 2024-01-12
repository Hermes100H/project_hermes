class car:
    def __init__(self, pPos, pSpeed) -> None:
        self.__pos = pPos
        self.__speed = pSpeed

    def SetPos(self, newPos) -> None:
        self.__pos = newPos

    def GetPos(self):
        return self.__pos

    def SetSpeed(self, newSpeed) -> None:
        self.__speed = newSpeed

    def GetSpeed(self):
        return self.__speed