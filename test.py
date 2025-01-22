import pixels
import sortedcontainers

test_pixels = [[None for _ in range(200)] for _ in range(200)]


for i in range(2):
    for j in range(2):
        print(f'Creating pixel at {j + 6}, {i+1}')
        test_pixels[i+1][j + 6] = pixels.Pixel(j+6, i+1, pixels.PixelType.WATER)

while True:
    for y in range(len(test_pixels)-1, 0, -1):
        for x in range(len(test_pixels[y]) - 1):
            pixel = test_pixels[y][x]
            if pixel is None:
                continue
            print(f'Before : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
            pixel.update(0.1, test_pixels, 100, 100)
            print(f'Afterwards : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
            if (int(pixel.x), int(pixel.y)) in test_pixels and test_pixels[int(pixel.x), int(pixel.y)] is not pixel:
                print(f'WARNING : PIXEL ALREADY AT {int(pixel.x), int(pixel.y)}')
            test_pixels[y][x] = None
            test_pixels[int(pixel.y)][int(pixel.x)] = pixel
    input()