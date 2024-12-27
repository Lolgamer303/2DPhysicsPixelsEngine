import numpy as np
from pygame import *
from time import sleep
import random

class PixelEngine:
    def __init__(self, height, width, pixelScale):
        self.height = height
        self.width = width
        self.pixelScale = pixelScale
        self.grid = np.zeros((height, width), dtype=int)
    def update(self):
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if self.grid[x][y] == 1:
                    self.update_sand(x, y)
                elif self.grid[x][y] == 2:
                    self.update_water(x, y)

    def update_sand(self, x, y):
        if y < self.height - 1:
            if self.grid[x][y+1] == 0:
                self.grid[x][y] = 0
                self.grid[x][y+1] = 1
                return
            downL = self.grid[x-1][y+1] == 0
            downR = self.grid[x+1][y+1] == 0
            if downL and downR:
                self.grid[x][y] = 0
                i = random.choice([1, -1])
                self.grid[x+i][y+1] = 1
            elif downL:
                self.grid[x][y] = 0
                self.grid[x-1][y+1] = 1
            elif downR:
                self.grid[x][y] = 0
                self.grid[x+1][y+1] = 1
            
    def draw(self, screen: Surface):
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if self.grid[x][y] == 1:
                    color = (194, 178, 128)
                    draw.rect(screen, color, (x * self.pixelScale, y * self.pixelScale, self.pixelScale, self.pixelScale))

def handleMouse(engine: PixelEngine):
    if mouse.get_pressed()[0]:
        x, y = mouse.get_pos()
        x = int(x/engine.pixelScale)
        y = int(y/engine.pixelScale)
        if x < engine.width and y < engine.height:
            engine.grid[x][y] = 1

def main():
    init()
    screen = display.set_mode((600, 600))
    display.set_caption("Pixel Physics Engine")
    engine = PixelEngine(200, 200, 3)
    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        screen.fill((0, 0, 0))
        handleMouse(engine)
        engine.update()
        engine.draw(screen)
        display.flip()
    quit()

if __name__ == "__main__":
    main()

        