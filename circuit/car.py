from maths_utils import *

class car:

    def __init__(self, pPos, pSpeed) -> None:
        self.__pos = pPos
        self.__speed = pSpeed

    def SetPos(self, newPos):
        self.__pos = newPos

    def GetPos(self) -> vec2:
        return self.__pos

    def SetSpeed(self, newSpeed):
        self.__speed = newSpeed

    def GetSpeed(self) -> vec2:
        return self.__speed