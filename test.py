from pixels import Pixel, PixelType

def test_pixel_update():
    width, height = 200, 200  # Define the dimensions of the array
    # Initialize a height by width pixels array with None
    pixels = [[None for _ in range(width + 1)] for _ in range(height + 1)]
    
    # Place a 4x4 grid of pixels 10 units away from the origin
    start_x, start_y = 10, 10
    for i in range(2, 0, -1):
        for j in range(2):
            pixel = Pixel(x=start_x + j, y=start_y + i, type=PixelType.WATER)
            pixels[start_y + i][start_x + j] = pixel
    
    while True:
        # Print initial state
        for i in range(2, 0, -1):
            for j in range(2):
                pixel = pixels[start_y + i][start_x + j]
                if pixel:
                    print(f"Before update: Location: ({pixel.x}, {pixel.y}), Velocity: {pixel.velocity}")
        
        # Wait for user input (Enter key)
        input("Press Enter to update pixels...")
        
        # Update pixel locations
        for i in range(2, 0, -1):
            for j in range(2):
                pixel = pixels[start_y + i][start_x + j]
                if pixel:
                    pixel.update(deltaTime=0.1, pixels=pixels, w=width, h=height)
        
        # Print updated state
        for i in range(2, 0, -1):
            for j in range(2):
                pixel = pixels[start_y + i][start_x + j]
                if pixel:
                    print(f"After update: Location: ({pixel.x}, {pixel.y}), Velocity: {pixel.velocity}")

if __name__ == "__main__":
    test_pixel_update()