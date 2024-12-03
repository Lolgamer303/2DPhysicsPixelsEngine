import pygame
import numpy as np
from pixels import Pixel, PixelType
from time import sleep

def render(screen: pygame.Surface, pixels: list[Pixel], deltaTime: float):
    for pixel in pixels:
        pixel.update(deltaTime, pixels)
        pixel.draw(screen, 1)

        
        