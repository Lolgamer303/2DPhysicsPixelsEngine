from pixels import Pixel, PixelType

def test_pixel_update():
    width, height = 200, 200  # Define the dimensions of the array
    # Initialize a height by width pixels array with None
    pixels = [[None for _ in range(width + 1)] for _ in range(height + 1)]
    
    # Place a 4x4 grid of pixels 10 units away from the origin
    start_x, start_y = 10, 10
    for i in range(4, 0, -1):
        for j in range(4):
            pixel = Pixel(x=start_x + j, y=start_y + i, type=PixelType.WATER)
            pixels[start_y + i][start_x + j] = pixel
    
    while True:
        for y in range(len(pixels)-1, 0, -1):
            for x in range(len(pixels[y]) - 1):
                pixel = pixels[y][x]
                if pixel is not None:
                    pixel.update(0.1, pixels, width, height)
                    if pixels[int(pixel.y)][int(pixel.x)] is not pixel and pixels[int(pixel.y)][int(pixel.x)] is not None and pixels[int(pixel.y)][int(pixel.x)].type is not PixelType.WATER:
                        print(f"Pixel already exists at that location, {int(pixel.x), int(pixel.y)}")
                    pixels[y][x] = None
                    pixels[int(pixel.y)][int(pixel.x)] = pixel
                    print(f"Pixel at {int(pixel.x), pixel.y, pixel.velocity}")
        input("Press Enter to continue")

if __name__ == "__main__":
    test_pixel_update()