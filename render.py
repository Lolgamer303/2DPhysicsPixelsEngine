import pygame
import numpy as np
from pixels import Pixel, PixelType
from time import sleep
from configparser import ConfigParser
from typing import Dict, Tuple

def render(screen: pygame.Surface, pixels: Dict[Tuple[int, int], Pixel], deltaTime: float):
    updated_pixels = {}
    obj = ConfigParser()
    obj.read('config.ini')
    pixelsSize = int((obj['PIXEL_SIZE'])['value'])
    w = int((obj['SIZE'])['width'])
    h = int((obj['SIZE'])['height'])
    for pixel in pixels.values():
        pixel.update(deltaTime, pixels, w, h)
        pixel.draw(screen, pixelsSize)
        updated_pixels[(int(pixel.x), int(pixel.y))] = pixel
    pixels.clear()
    pixels.update(updated_pixels)
    return pixels