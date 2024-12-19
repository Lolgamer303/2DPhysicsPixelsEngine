import numpy as np
import pygame
import enum
import math
import random

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
                self.velocity += 9.81 * deltaTime
                newY = self.y + self.velocity * deltaTime * 100
                step = int(newY) - int(self.y)
                if step > 0:
                    for i in range(step):
                        if (self.x, int(self.y) + i + 1) in pixels and pixels[(self.x, int(self.y) + i + 1)].velocity == 0:
                            self.checkForSpaces(i + 1, pixels)
                            return
                self.y = newY
                if self.y >= 598:
                    self.velocity = 0
                    self.y = 598
        elif self.type == PixelType.STONE:
            self.velocity = 0

    def checkForSpaces(self, step, pixels):
        pixelLoc = int(self.y) + step
        downLeft = (self.x - 1, pixelLoc) in pixels and pixels[(self.x - 1, pixelLoc)].velocity == 0
        downRight = (self.x + 1, pixelLoc) in pixels and pixels[(self.x + 1, pixelLoc)].velocity == 0
        if not downLeft and not downRight and 1 <= self.x <= 798:
            self.x += random.choice([1, -1])
            self.y = pixelLoc
        elif not downLeft and self.x >= 1:
            self.x -= 1
            self.y = pixelLoc
        elif not downRight and self.x <= 798:
            self.x += 1
            self.y = pixelLoc
        else:
            self.velocity = 0
            self.y = pixelLoc - 1

    def checkForUpdatedSpaces(self, pixels):
        if (self.x, self.y + 1) in pixels and pixels[(self.x, self.y + 1)].velocity == 0:
            downLeft = (self.x - 1, self.y + 1) in pixels and pixels[(self.x - 1, self.y + 1)].velocity == 0
            downRight = (self.x + 1, self.y + 1) in pixels and pixels[(self.x + 1, self.y + 1)].velocity == 0
            if not downLeft and not downRight and 1 <= self.x <= 798:
                self.x += random.choice([1, -1])
                self.y += 1
            elif not downLeft and self.x >= 1:
                self.x -= 1
                self.y += 1
            elif not downRight and self.x <= 798:
                self.x += 1
                self.y += 1
        elif self.y < 598:
            self.velocity = 0.01