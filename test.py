from pixels import Pixel, PixelType
from render import render

def test_pixel_update():
    pixels = {
        (1, 1): Pixel(1, 1, PixelType.SAND),
        (6, 6): Pixel(6, 6, PixelType.STONE),
        (1, 2): Pixel(1, 2, PixelType.SAND)
    }
    for key in pixels:
        print(f"Before update: {key} -> {pixels[key].type}")
        pixels[key].update(4, pixels)
        print(f"After update: {(pixels[key].x, pixels[key].y)} -> {pixels[key].type}")

if __name__ == "__main__":
    test_pixel_update()