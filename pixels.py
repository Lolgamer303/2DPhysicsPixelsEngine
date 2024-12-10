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
            self.velocity += deltaTime * 9.81 * 10
            self.y += self.velocity * deltaTime
            y = math.floor(self.y)
            self.handleSpace(pixels, y)

    def handleSpace(self, pixels, y):
        if self.velocity > 0: 
            if y < 0 or y >= 599:
                self.velocity = 0
                self.y = 599
                return
        hasAPixelDown = (self.x, y + 1) in pixels and (pixels.get((self.x, y + 1)).velocity == 0 or pixels.get((self.x, y + 1)).type == PixelType.STONE)
        if hasAPixelDown: 
            hasAPixelDownLeft = (self.x - 1, y + 1) in pixels and pixels.get((self.x - 1, y + 1)).velocity == 0
            hasAPixelDownRight = (self.x + 1, y + 1) in pixels and pixels.get((self.x + 1, y + 1)).velocity == 0
            if hasAPixelDown:
                if not hasAPixelDownLeft and not hasAPixelDownRight:
                    self.velocity / 2
                    l = random.choice([-1, 1])
                    self.x += l
                    return
                if not hasAPixelDownRight:
                    self.velocity /= 2
                    self.x += 1
                    return
                elif not hasAPixelDownLeft:
                    self.velocity /= 2
                    self.x -= 1
                    return
                else:
                    self.velocity = 0
                    self.y = y
                    return