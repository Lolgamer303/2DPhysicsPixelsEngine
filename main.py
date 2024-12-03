from pygame import *
from numpy import *
import render
import pixels

init()
screen = display.set_mode((800, 600))
display.set_caption("Pixel Physics Engine")

FPS = 60
clock = time.Clock()

pixels = [pixels.Pixel(400, 300, pixels.PixelType.SAND)] 

running = True
while running:

    for e in event.get():
        if e.type == QUIT:
            running = False
    frameTime = clock.tick(FPS) / 1000.0

    screen.fill((0, 0, 0))
    render.render(screen, pixels=pixels, deltaTime=frameTime)

    display.flip()
quit()