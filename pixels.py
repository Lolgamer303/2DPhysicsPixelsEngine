import numpy as np
import pygame
import enum
import math
import random
import time

class PixelType(enum.Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    def __init__(self, r, g, b, id):
        self.r = r
        self.g = g
        self.b = b
        self.id = id
    
    SAND = (194, 178, 128, 1)
    STONE = (100, 100, 100, 2)

class Pixel:
    
    def __init__(self, x, y, type: PixelType):
        self.x: float = x
        self.y: float = y
        self.type: PixelType = type
        self.velocity: float = 0.01

    def draw(self, screen, size=1):
        pygame.draw.rect(screen, (self.type.r, self.type.g, self.type.b), (self.x, self.y, size, size))

    def update(self, deltaTime, pixels):
        if self.type == PixelType.SAND:
            if self.velocity == 0:
                self.checkForUpdatedSpaces(pixels)
            else: 
                self.velocity = self.velocity + 9.81 * deltaTime
                newY = self.y + self.velocity * deltaTime * 100
                step = newY // 1 - self.y // 1
                if step > 0:
                    for x in range(int(step)):
                        if (self.x, math.floor(self.y) + x + 1) in pixels and pixels.get((self.x, math.floor(self.y) + x + 1)).velocity == 0:
                            self.checkForSpaces(x+1, pixels)
                            return
                self.y = newY
                if self.y > 599:
                    self.velocity = 0
                    self.y = 599
        elif self.type == PixelType.STONE:
            self.velocity = 0

    def checkForSpaces(self, x, pixels):
        pixelLoc = int(self.y // 1 + x)
        downLeft = (self.x - 1, pixelLoc) in pixels and pixels.get((self.x - 1, pixelLoc)).velocity == 0
        downRight = (self.x + 1, pixelLoc) in pixels and pixels.get((self.x + 1, pixelLoc)).velocity == 0
        if not downLeft and not downRight:
            self.x = self.x + random.choice([1, -1])
            self.y = pixelLoc - 1
        elif not downLeft:
            self.x = self.x - 1
            self.y = pixelLoc - 1
        elif not downRight:
            self.x = self.x + 1
            self.y = pixelLoc - 1
        else:
            self.velocity = 0
            self.y = pixelLoc - 1

    def checkForUpdatedSpaces(self, pixels):
        if (self.x, self.y + 1) in pixels and pixels.get((self.x, self.y + 1)).velocity == 0:
            downLeft = (self.x - 1, self.y + 1) in pixels and pixels.get((self.x - 1, self.y + 1)).velocity == 0
            downRight = (self.x + 1, self.y + 1) in pixels and pixels.get((self.x + 1, self.y + 1)).velocity == 0
            if not downLeft and not downRight:
                self.x += random.choice([1,-1])
                self.y += 1
            elif not downLeft:
                self.x -= 1
                self.y += 1
            elif not downRight:
                self.x += 1
                self.y += 1
        else:
            self.velocity = 0.01

            


