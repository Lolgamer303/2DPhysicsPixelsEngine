import numpy as np
import pygame
import enum

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
    AIR = (0, 0, 0, 2)

class Pixel:
    def __init__(self, x, y, type: PixelType):
        self.x: float = x
        self.y: float = y
        self.type: PixelType = type
        self.velocity: float = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (self.type.r, self.type.g, self.type.b), (self.x, self.y, 1, 1))
    def draw(self, screen, size):
        pygame.draw.rect(screen, (self.type.r, self.type.g, self.type.b), (self.x, self.y, size, size))

    def update(self, deltaTime, pixels):
        if self.type == PixelType.SAND:
            self.velocity += deltaTime * 9.81 * 10
            self.y += + self.velocity * deltaTime