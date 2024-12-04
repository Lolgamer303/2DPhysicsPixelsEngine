import pygame
import numpy as np
from pixels import Pixel, PixelType
from time import sleep

from typing import Dict, Tuple

def render(screen: pygame.Surface, pixels: Dict[Tuple[int, int], Pixel], deltaTime: float):
    updated_pixels = {}
    for pixel in pixels.values():
        pixel.update(deltaTime, pixels)
        pixel.draw(screen, 10)
        updated_pixels[(int(pixel.x), int(pixel.y))] = pixel
        print(pixel.velocity)
    pixels.clear()
    pixels.update(updated_pixels)