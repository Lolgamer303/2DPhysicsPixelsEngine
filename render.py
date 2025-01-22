import pygame
import numpy as np
from pixels import Pixel, PixelType
from time import sleep
from configparser import ConfigParser
from typing import List

def render(screen: pygame.Surface, pixels: List[List[Pixel]], deltaTime: float, runningTime: float):
    obj = ConfigParser()
    obj.read('config.ini')
    pixelsSize = int((obj['PIXEL_SIZE'])['value'])
    w = int((obj['SIZE'])['width'])
    h = int((obj['SIZE'])['height'])
    rainbowMode = True if (obj['RAINBOW_MODE'])['value'] == 'True' else False
    for y in range(len(pixels)-1, 0, -1):
        for x in range(len(pixels[y]) - 1):
            pixel = pixels[y][x]
            if pixel is not None:
                pixel.update(deltaTime, pixels, w, h)
                pixel.draw(screen, pixelsSize, rainbowMode, runningTime)
                if pixels[int(pixel.y)][int(pixel.x)] is not pixel and pixels[int(pixel.y)][int(pixel.x)] is not None and pixels[int(pixel.y)][int(pixel.x)].type is not PixelType.WATER:
                    raise Exception(f"Pixel already exists at that location, {int(pixel.x), int(pixel.y)}")
                pixels[y][x] = None
                pixels[int(pixel.y)][int(pixel.x)] = pixel
    return pixels