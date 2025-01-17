import pygame
import numpy as np
from pixels import Pixel, PixelType
from time import sleep
from configparser import ConfigParser
from typing import Dict, Tuple

def render(screen: pygame.Surface, pixels: Dict[Tuple[int, int], Pixel], deltaTime: float, runningTime: float):
    updated_pixels = {}
    obj = ConfigParser()
    obj.read('config.ini')
    pixelsSize = int((obj['PIXEL_SIZE'])['value'])
    w = int((obj['SIZE'])['width'])
    h = int((obj['SIZE'])['height'])
    rainbowMode = True if (obj['RAINBOW_MODE'])['value'] == 'True' else False
    for key, pixel in pixels.items():
        pixel.update(deltaTime, pixels, w, h, key)
        pixel.draw(screen, pixelsSize, rainbowMode, runningTime)
        if ((int(pixel.x), int(pixel.y))) in pixels and pixels.get((int(pixel.x), int(pixel.y))) is not pixel:
            raise Exception("Pixel already exists at that location" + str((int(pixel.x), int(pixel.y))))
        pixels[(int(pixel.x), int(pixel.y))] = pixels.pop(key)
#            updated_pixels[(int(pixel.x), int(pixel.y))] = pixel
#    pixels.clear()
#    pixels.update(updated_pixels)
    return pixels