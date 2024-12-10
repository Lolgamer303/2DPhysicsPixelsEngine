from pygame import *
from numpy import *
import render
from pixels import PixelType, Pixel
import random

init()
screen = display.set_mode((800, 600))
display.set_caption("Pixel Physics Engine")

FPS = 120
clock = time.Clock()

SPAWN_SIZE = 3

pixels = {}

def get_mouse_coords():
    x, y = mouse.get_pos()
    return x, y

def handle_mouse_press():
    if mouse.get_pressed()[0]:
        x, y = get_mouse_coords()
        pixels[(x, y)] = Pixel(x, y, PixelType.SAND)

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