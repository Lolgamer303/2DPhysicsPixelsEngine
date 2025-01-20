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
        if ((int(pixel.x), int(pixel.y))) in pixels and pixels[(int(pixel.x), int(pixel.y))] is not pixel:
            print("Pixel already exists at that location" + str((int(pixel.x), int(pixel.y))))
        pixels[(int(pixel.x), int(pixel.y))] = pixels.pop(key)
        pixel.draw(screen, pixelsSize, rainbowMode, runningTime)
#            updated_pixels[(int(pixel.x), int(pixel.y))] = pixel
#    pixels.clear()
#    pixels.update(updated_pixels)
    return pixels