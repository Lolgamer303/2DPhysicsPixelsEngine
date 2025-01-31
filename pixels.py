import pygame
import enum
import random
import colorsys
from typing import List


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
        self.velocity: float = 0.001
        self.rainbowHue: float = rainbowHue

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
            # pygame.draw.circle(screen, rgb, (int(self.x * size), int(self.y * size)), size) 
        else:
            pygame.draw.rect(
                screen,
                (self.type.r, self.type.g, self.type.b),
                (self.x * size, self.y * size, size, size),
            )
            pygame.draw.rect(screen, (0, 1, 1), (1, 1, 100, 4))
            # pygame.draw.circle(screen, (self.type.r, self.type.g, self.type.b), (int(self.x * size), int(self.y * size)), size)

    def update(self, deltaTime, pixels: List[List[any]], w, h):
        if self.type == PixelType.SAND:
            if self.velocity == 0:
                if self.y < h:
                    self.checkForUpdatedSpaces(pixels, w, h)
            else:
                newY = (0.5 * 9.81 * deltaTime**2 + self.velocity * deltaTime + self.y / 100) * 100
                self.velocity = 9.81 * deltaTime + self.velocity
                step = int(newY) - int(self.y)
                for i in range(step):
                    if int(self.y) + i + 1 <= h and pixels[int(self.y) + i + 1][self.x] is not None and pixels[int(self.y) + i + 1][self.x].type is not PixelType:
                        self.checkForSpaces(i + 1, pixels, w, h)
                        return
                self.y = newY
                if self.y >= h:
                    self.velocity = 0
                    self.y = h
        elif self.type == PixelType.WATER:
            if self.velocity == 0:
                if self.y < h:
                    self.checkForUpdatedSpaces(pixels, w, h)
            else:
                newY = (0.5 * 9.81 * deltaTime**2 + self.velocity * deltaTime + self.y / 100) * 100
                self.velocity = 9.81 * deltaTime + self.velocity
                step = int(newY) - int(self.y)
                for i in range(step):
                    if int(self.y) + i + 1 <= h and pixels[int(self.y) + i + 1][self.x] is not None:
                        self.waterCheckForSpaces(step=i + 1, w=w, h=h, pixels=pixels)
                        return
                self.y = newY
                if self.y >= h:
                    self.velocity = 0
                    self.y = h

    def checkForSpaces(self, step, pixels, w, h):
        pixelLoc = int(self.y) + step
        downLeft = pixels[pixelLoc][self.x - 1] is not None and pixels[pixelLoc][self.x - 1].type is not PixelType.WATER
        downRight = pixels[pixelLoc][self.x + 1] is not None and pixels[pixelLoc][self.x + 1].type is not PixelType.WATER
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
        if pixels[self.y + 1][self.x] is not None and pixels[self.y + 1][self.x].velocity == 0:
            downLeft = pixels[self.y + 1][self.x - 1]
            downRight = pixels[self.y + 1][self.x + 1]
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
        if self.x <= 0:
            return True if pixels[downRight[0]][downRight[1]] and pixels[below[0]][below[1]] else False
        if self.x >= w:
            return True if pixels[downLeft[0]][downLeft[1]] and pixels[below[0]][below[1]] else False

        if (
            pixels[below[0]][below[1]]
            and pixels[below[0]][below[1]].velocity == 0
            and pixels[downLeft[0]][downLeft[1]]
            and pixels[downLeft[0]][downLeft[1]].velocity == 0
            and pixels[downRight[0]][downRight[1]]
            and pixels[downRight[0]][downRight[1]].velocity == 0
        ):
            return True
        elif self.y >= h:
            return True
        return False

    def waterCheckForSpaces(self, pixels, w, h, step):
        pixelLoc = int(self.y) + step
        if pixelLoc > h:
            self.velocity = 0
            self.y = h
            return
        if pixels[pixelLoc][self.x].type == PixelType.WATER:
            if self.makePlace(pixels, w, pixelLoc):
                self.velocity = 0
                return
            else:
                self.velocity = 0
                self.y = pixelLoc - 1
                return
        print("CHECKED FOR Spaces")
        self.checkForSpaces(step, pixels, w, h)

    def makePlace(self, pixels, w, pixelLoc):
        n = random.choice([1, -1])
        stop = False
        firstDirection = True
        secondDirection = True
        i = 0
        while not stop:
            i += 1
            firstPos = self.x + i * n
            if 0 <= firstPos and firstPos <= w and pixels[pixelLoc][firstPos] is None:
                self.x = firstPos
                self.y = pixelLoc
                return True
            elif 0 <= firstPos and firstPos <= w and pixels[pixelLoc][firstPos].type is not PixelType.WATER:
                firstDirection = False
            elif not (0 <= firstPos and firstPos <= w):
                firstDirection = False
            secondPos = self.x + i * -n
            if 0 <= secondPos and secondPos <= w and pixels[pixelLoc][secondPos] is None:
                self.x = secondPos
                self.y = pixelLoc
                return True
            elif 0 <= secondPos and secondPos <= w and pixels[pixelLoc][secondPos].type is not PixelType.WATER:
                secondDirection = False
            elif not (0 <= secondPos and secondPos <= w):
                secondDirection = False
            if not secondDirection and not firstDirection:
                stop = True
        return False
