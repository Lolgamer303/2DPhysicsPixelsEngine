import numpy as np
import pygame
import enum
import random
import colorsys
from typing import Dict, Tuple

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

    def update(self, deltaTime, pixels: Dict[Tuple[int, int], any], w, h, key):
        if self.type == PixelType.SAND:
            if self.velocity == 0:
                self.checkForUpdatedSpaces(pixels, w, h)
            else:
                self.velocity += 9.81 * deltaTime
                newY = self.y + self.velocity * abs(deltaTime) * 100
                step = int(newY) - int(self.y)
                if step > 0:
                    for i in range(step):
                        next_pos = (self.x, int(self.y) + i + 1)
                        if next_pos in pixels and (pixels[next_pos].velocity == 0 or pixels[next_pos].sliding):
                            self.checkForSpaces(i + 1, pixels, w, key, h)
                            return
                self.y = newY
                if self.y >= h:
                    self.velocity = 0
                    self.y = h

    def checkForSpaces(self, step, pixels, w, key, h):
        pixelLoc = int(self.y) + step
        downLeft = (self.x - 1, pixelLoc) in pixels and (pixels[(self.x - 1, pixelLoc)].velocity == 0 or pixels[(self.x - 1, pixelLoc)].sliding)
        downRight = (self.x + 1, pixelLoc) in pixels and (pixels[(self.x + 1, pixelLoc)].velocity == 0 or pixels[(self.x + 1, pixelLoc)].sliding)
        if not downLeft and not downRight and 1 <= self.x < w:
            self.x += random.choice([1, -1])
            self.y = pixelLoc
            self.sliding = True
            if self.checkIfShouldStop(pixels, h):
                self.velocity = 0
        elif not downLeft and self.x >= 1:
            self.x -= 1
            self.y = pixelLoc
            self.sliding = True
            if self.checkIfShouldStop(pixels, h):
                self.velocity = 0
        elif not downRight and self.x < w:
            self.x += 1
            self.y = pixelLoc
            if self.checkIfShouldStop(pixels, h):
                self.velocity = 0
            self.sliding = True
        else:
            self.velocity = 0
            self.y = pixelLoc - 1

    def checkForUpdatedSpaces(self, pixels, w, h):
        below = (self.x, self.y + 1)
        if below in pixels and pixels[below].velocity == 0:
            downLeft = (self.x - 1, self.y + 1) in pixels and (pixels[(self.x - 1, self.y + 1)].velocity == 0 or pixels[(self.x - 1, self.y + 1)].sliding)
            downRight = (self.x + 1, self.y + 1) in pixels and (pixels[(self.x + 1, self.y + 1)].velocity == 0 or pixels[(self.x + 1, self.y + 1)].sliding)
            if not downLeft and not downRight and 1 <= self.x < w:
                self.x += random.choice([1, -1])
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h):
                    self.velocity = 0
            elif not downLeft and self.x >= 1:
                self.x -= 1
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h):
                    self.velocity = 0
            elif not downRight and self.x < w:
                self.x += 1
                self.y += 1
                self.sliding = True
                if self.checkIfShouldStop(pixels, h):
                    self.velocity = 0
        elif self.y < h:
            self.velocity = 0.01

    def checkIfShouldStop(self, pixels, h):
        below = (self.x, int(self.y) + 1)
        downLeft = (self.x - 1, int(self.y) + 1)
        downRight = (self.x + 1, int(self.y) + 1)
        if (below in pixels and pixels[below].velocity == 0 and
            downLeft in pixels and pixels[downLeft].velocity == 0 and
            downRight in pixels and pixels[downRight].velocity == 0):
            return True
        elif self.y >= h:
            return True
        return False