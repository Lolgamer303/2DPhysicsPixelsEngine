from pygame import *
from numpy import *
import render
from pixels import PixelType, Pixel
from time import sleep

def main():
    init()
    screen = display.set_mode((800, 600))
    display.set_caption("Pixel Physics Engine")

    FPS = 120
    clock = time.Clock()

    SPAWN_SIZE = 0

    pixels: dict = {}

    def get_mouse_coords():
        x, y = mouse.get_pos()
        return x, y

    def handle_mouse_press():
        if mouse.get_pressed()[0]:
            x, y = get_mouse_coords()
            for i in range(-SPAWN_SIZE, SPAWN_SIZE + 1):
                for j in range(-SPAWN_SIZE, SPAWN_SIZE + 1):
                    pixels[(x + i, y + j)] = Pixel(x + i, y + j, PixelType.SAND)
        if mouse.get_pressed()[2]:
            x, y = get_mouse_coords()
            for i in range(-SPAWN_SIZE-2, SPAWN_SIZE + 2):
                for j in range(-SPAWN_SIZE-2, SPAWN_SIZE + 2):
                    pixels[(x + i, y + j)] = Pixel(x + i, y + j, PixelType.STONE)

    running = True
    while running:

        for e in event.get():
            if e.type == QUIT:
                running = False
        frameTime = clock.tick(FPS) / 1000.0
        handle_mouse_press()
        screen.fill((0, 0, 0))
        render.render(screen, pixels=pixels, deltaTime=frameTime)

        display.flip()
    quit()

if __name__ == "__main__":
    main()
