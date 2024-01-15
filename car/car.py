class car:
    def __init__(self, pPos, pSpeed, pMass=1) -> None:
        self.__pos = pPos
        self.__speed = pSpeed
        self.__mass = pMass

    def SetPos(self, newPos) -> None:
        self.__pos = newPos

    def GetPos(self):
        return self.__pos

    def SetSpeed(self, newSpeed) -> None:
        self.__speed = newSpeed

    def GetSpeed(self):
        return self.__speed