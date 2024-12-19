from pygame import *
from numpy import *
import render
from pixels import PixelType, Pixel
from time import sleep
from sortedcontainers import SortedDict

def main():
    init()
    screen = display.set_mode((800, 600))
    display.set_caption("Pixel Physics Engine")

    FPS = 120
    clock = time.Clock()

    SPAWN_SIZE = 0
    PIXEL_SIZE = 1

    pixels = SortedDict(lambda key: (-key[1], -key[0]))

    def get_mouse_coords():
        x, y = mouse.get_pos()
        return x, y

    def handle_mouse_press():
        if mouse.get_pressed()[0]:
            x, y = get_mouse_coords()
            for i in range(-SPAWN_SIZE, SPAWN_SIZE + 1):
                for j in range(-SPAWN_SIZE, SPAWN_SIZE + 1):
                    pixels[x + i, y + j] = Pixel(x + i , y + j, PixelType.SAND)
        if mouse.get_pressed()[2]:
            x, y = get_mouse_coords()
            for i in range(-SPAWN_SIZE-2, SPAWN_SIZE + 2):
                for j in range(-SPAWN_SIZE-2, SPAWN_SIZE + 2):
                    pixels[(x + i, y + j)] = Pixel(x + i, y + j, PixelType.STONE)

    def draw_slider():
        font_obj = font.Font(None, 36)
        text = font_obj.render(f"Spawn Size: {SPAWN_SIZE}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        draw.rect(screen, (255, 255, 255), (10, 50, 200, 10))
        draw.rect(screen, (0, 0, 255), (10 + SPAWN_SIZE * 20, 45, 10, 20))

    def handle_slider():
        nonlocal SPAWN_SIZE
        if mouse.get_pressed()[0]:
            x, y = get_mouse_coords()
            if 10 <= x <= 210 and 45 <= y <= 65:
                SPAWN_SIZE = (x - 10) // 20

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        frameTime = clock.tick(FPS) / 1000.0
        handle_mouse_press()
        handle_slider()
        screen.fill((0, 0, 0))
        render.render(screen, pixels=pixels, deltaTime=frameTime, pixelsSize=PIXEL_SIZE)
        draw_slider()
        display.flip()
    quit()

if __name__ == "__main__":
    main()
