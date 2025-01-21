import numpy as np
import pygame
import enum
import random
import colorsys
from typing import Dict, List, Tuple

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
    WATER = (0, 0, 255, 3)

class Pixel:
    def __init__(self, x, y, type: PixelType, rainbowHue=None):
        self.x: float = x
        self.y: float = y
        self.type: PixelType = type
        self.velocity: float = 0.01
        self.rainbowHue: float = rainbowHue
        self.sliding: bool = False

    def draw(self, screen, size=1, rainbowMode=False, runningTime=0):
        if rainbowMode:
            if self.rainbowHue is not None:
                rgb = colorsys.hls_to_rgb(self.rainbowHue, 0.5, 1.0)
                rgb = tuple(int(c * 255) for c in rgb)
                pygame.draw.rect(screen, rgb, (self.x * size, self.y * size, size, size))
            elif self.type == PixelType.STONE:
                rgb = colorsys.hls_to_rgb((runningTime / 10) % 1, 0.5, 1.0)
                rgb = tuple(int(c * 255) for c in rgb)
            pygame.draw.rect(screen, rgb, (self.x * size, self.y * size, size, size))
        else:
            pygame.draw.rect(screen, (self.type.r, self.type.g, self.type.b), (self.x * size, self.y * size, size, size))

    def update(self, deltaTime, pixels: List[List[any]], w, h):
        if self.type == PixelType.SAND:
            if self.velocity == 0:
                if self.y < h:
                    self.checkForUpdatedSpaces(pixels, w, h)
            else:
                self.velocity += 9.81 * deltaTime
                newY = self.y + self.velocity * deltaTime * 100
                step = int(newY) - int(self.y)
                if step > 0:
                    for i in range(step):
                        if int(self.y) + i + 1 <= h and pixels[int(self.y) + i + 1][self.x] is not None:
                            self.checkForSpaces(i + 1, pixels, w, h)
                            return
                self.y = newY
                if self.y >= h:
                    self.velocity = 0
                    self.y = h

    def checkForSpaces(self, step, pixels, w, h):
        pixelLoc = int(self.y) + step
        downLeft = pixels[pixelLoc][self.x-1] is not None # and (pixels[(self.x - 1, pixelLoc)].velocity == 0 or pixels[(self.x - 1, pixelLoc)].sliding)
        downRight = pixels[pixelLoc][self.x+1] is not None # and (pixels[(self.x + 1, pixelLoc)].velocity == 0 or pixels[(self.x + 1, pixelLoc)].sliding)
        if not downLeft and not downRight and 1 <= self.x < w:
            self.x += random.choice([1, -1])
            self.y = pixelLoc
            self.sliding = True
            if self.checkIfShouldStop(pixels, h, w):
                self.velocity = 0
        elif not downLeft and self.x >= 1:
            self.x -= 1
            self.y = pixelLoc
            self.sliding = True
            if self.checkIfShouldStop(pixels, h, w):
                self.velocity = 0
        elif not downRight and self.x < w:
            self.x += 1
            self.y = pixelLoc
            if self.checkIfShouldStop(pixels, h, w):
                self.velocity = 0
            self.sliding = True
            
        else:
            self.velocity = 0
            self.y = pixelLoc - 1

    def checkForUpdatedSpaces(self, pixels, w, h):
        if  pixels[self.y + 1][self.x] is not None and pixels[self.y + 1][self.x].velocity == 0:
            downLeft = pixels[self.y + 1][self.x - 1] # and (pixels[(self.x - 1, self.y + 1)].velocity == 0 or pixels[(self.x - 1, self.y + 1)].sliding)
            downRight = pixels[self.y + 1][self.x + 1] # and (pixels[(self.x + 1, self.y + 1)].velocity == 0 or pixels[(self.x + 1, self.y + 1)].sliding)
            if not downLeft and not downRight and 1 <= self.x < w:
                self.x += random.choice([1, -1])
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h, w):
                    self.velocity = 0
            elif not downLeft and self.x >= 1:
                self.x -= 1
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h, w):
                    self.velocity = 0
            elif not downRight and self.x < w:
                self.x += 1
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h, w):
                    self.velocity = 0
        elif self.y < h:
            self.velocity = 0.01

    def checkIfShouldStop(self, pixels, h, w):
        if self.y + 1 > h:
            return True
        below = (int(self.y) + 1, self.x)
        downLeft = (int(self.y) + 1, self.x - 1)
        downRight = (int(self.y) + 1, self.x + 1)
        if self.x <= 0: return True if pixels[downRight[0]][downRight[1]] and pixels[below[0]][below[1]] else False
        if self.x >= w: return True if pixels[downLeft[0]][downLeft[1]] and pixels[below[0]][below[1]] else False

        if (pixels[below[0]][below[1]] and pixels[below[0]][below[1]].velocity == 0 and
            pixels[downLeft[0]][downLeft[1]] and pixels[downLeft[0]][downLeft[1]].velocity == 0 and
            pixels[downRight[0]][downRight[1]] and pixels[downRight[0]][downRight[1]].velocity == 0):
            return True
        elif self.y >= h:
            return True
        return False