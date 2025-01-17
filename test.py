import pixels
import sortedcontainers

test_pixels = sortedcontainers.SortedDict(lambda key: (-key[1], -key[0]))

for i in range(3):
    for j in range(3):
        test_pixels[i, j] = pixels.Pixel(i, j+10, pixels.PixelType.SAND)
        print(j, i)

while True:
    for key, pixel in test_pixels.items():
        print(f'Before : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
        pixel.update(0.1, test_pixels, 100, 100, key)
        print(f'Afterwards : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
    input()