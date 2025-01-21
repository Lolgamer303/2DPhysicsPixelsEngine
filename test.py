import pixels
import sortedcontainers

test_pixels = sortedcontainers.SortedDict(lambda key: (-key[1], -key[0]))

for i in range(40):
    for j in range(40):
        test_pixels[i + 6, j] = pixels.Pixel(i, j+10, pixels.PixelType.SAND)
        print(j + 6, i)

while True:
    for key, pixel in test_pixels.items():
        print(f'Before : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
        pixel.update(0.1, test_pixels, 499, 499, key)
        print(f'Afterwards : Pixel at {pixel.x}, {pixel.y} has velocity {pixel.velocity}')
        if (int(pixel.x), int(pixel.y)) in test_pixels and test_pixels[int(pixel.x), int(pixel.y)] is not pixel:
            print(f'WARNING : PIXEL ALREADY AT {int(pixel.x), int(pixel.y)}')
        test_pixels[int(pixel.x), int(pixel.y)] = test_pixels.pop(key)
    input()