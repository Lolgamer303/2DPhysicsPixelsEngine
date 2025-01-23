# /// script
# dependencies = [
#  "pytmx",
#  "i18n",
# ]
# ///

from typing import List
from pygame import *
import pygame_gui.ui_manager
from render import render
import pygame
from pixels import PixelType, Pixel
from configparser import ConfigParser
import pygame_gui
import time
import asyncio

def modifySpawnSize(value, config_obj: ConfigParser):
    config_obj["SPAWN_SIZE"] = {
        'value': str(value),
    }
    with open('config.ini', 'w') as conf:
        config_obj.write(conf)
def pixelModeToggle(config_obj: ConfigParser):
    config_obj.read("config.ini")
    config_obj["PIXEL_MODE"] = {
        'value': 'True' if str(config_obj["PIXEL_MODE"]['value']) == 'False' else 'False',
    }
    with open('config.ini', 'w') as conf:
        config_obj.write(conf)

def modifyPixelSize(value, config_obj: ConfigParser, pixels: List[List[Pixel]]):
    config_obj["PIXEL_SIZE"] = {
        'value': str(value),
    }    
    w = int(800 / value) - 1
    h = w
    pixels = None
    pixels = [[None for _ in range(h+1)] for _ in range(w+1)]
    config_obj['SIZE'] = {
        'width': str(w),
        'height': str(h),
    }
    with open('config.ini', 'w') as conf:
        config_obj.write(conf)
    return pixels
def modifyRainbowMode(config_obj: ConfigParser):
    config_obj.read("config.ini")
    config_obj["RAINBOW_MODE"] = {
        'value': 'True' if str(config_obj["RAINBOW_MODE"]['value']) == 'False' else 'False',
    }
    with open('config.ini', 'w') as conf:
        config_obj.write(conf)

def get_mouse_coords():
    x, y = mouse.get_pos()
    return x, y

async def main():
    init()
    screen = display.set_mode((1000, 800))
    config_obj = ConfigParser()
    modifySpawnSize(5, config_obj)
    modifyPixelSize(4, config_obj, pixels=None)
    config_obj["RAINBOW_MODE"] = {
        'value': 'False',
    }
    config_obj["PIXEL_MODE"] = {
        'value': 'False',
    }
    with open('config.ini', 'w') as conf:
        config_obj.write(conf)
    manager = pygame_gui.UIManager((1000, 800), theme_path='theme.json')
    display.set_caption("Pixel Physics Engine")
    clock = pygame.time.Clock()

    settings_text = pygame_gui.elements.UITextBox(
        relative_rect=Rect((857, 20), (85, 30)),
        html_text="<b>SETTINGS</b>",
        manager=manager,
    )
    spawn_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=Rect(810, 200, 180, 50),
        start_value=5,
        value_range=(0, 10),
        manager=manager
    )
    spawn_slider_text = pygame_gui.elements.UITextBox(
        html_text="<b>Pixels Spawn Size<b/>",
        relative_rect=Rect((828.5, 160), (143, 30)),
        manager=manager,
    )
    pixel_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=Rect((810, 300), (180, 50)),
        start_value=4,
        value_range=(1, 10),
        manager=manager
    )
    pixel_slider_text = pygame_gui.elements.UITextBox(
        html_text="<b>Pixels Size<b/>",
        relative_rect=Rect((855, 260), (90, 30)),
        manager=manager,
    )
    pause_button = pygame_gui.elements.UIButton(
        relative_rect=Rect((850, 400), (100, 40)),
        text="PAUSE"
    )
    next_frame_button = pygame_gui.elements.UIButton(
        relative_rect=Rect((950, 400), (40, 40)),
        text=">"
    )
    fps_text = pygame_gui.elements.UITextBox(
        relative_rect=Rect((850, 70), (100, 30)),
        html_text="<b>0 FPS</b>",
        manager=manager,
    )
    rainbowmode_toggle = pygame_gui.elements.UIButton(
        relative_rect=Rect((840, 500), (120, 40)),
        text="Rainbow Mode",
        manager=manager,
    )
    pixel_mode_toogle = pygame_gui.elements.UIButton(
        relative_rect=Rect((840, 550), (120, 40)),
        text="Pixel Mode",
        manager=manager,
    )
    
    pixels = [[None for _ in range(200)] for _ in range(200)]

    COOLDOWN = 0.05
    def handle_mouse_press(deltaTime: float):
        nonlocal currentTimeCoolDown
        nonlocal runningTime
        runningTime += deltaTime
        nonlocal confirmation_dialog
        if confirmation_dialog is not None:
            return
        currentTimeCoolDown += deltaTime
        obj = ConfigParser()
        obj.read("config.ini")
        spawn_size = int((obj['SPAWN_SIZE'])['value'])
        pixel_size = int((obj['PIXEL_SIZE'])['value'])
        w = int((obj['SIZE'])['WIDTH'])
        h = int((obj['SIZE'])['HEIGHT'])
        pixel_mode = True if ((obj['PIXEL_MODE'])['value']) == 'True' else False
        if currentTimeCoolDown > COOLDOWN + COOLDOWN / 2 * spawn_size and (mouse.get_pressed()[0]):
            currentTimeCoolDown = 0
            x, y = get_mouse_coords()
            if x < 0 or x > 800:
                return
            x = int(x/pixel_size)
            y = int(y/pixel_size)
            for i in range(-spawn_size, spawn_size + 1):
                for j in range(-spawn_size, spawn_size + 1):
                    if (x+j) >= 0 and (x+j) < w and (y+i) >= 0 and (y+i) < h:
                        pixels[y + i][x + j] = Pixel(x + j , y + i, PixelType.WATER if pixel_mode else PixelType.SAND, rainbowHue=(runningTime/12)%1)
        elif mouse.get_pressed()[2]:
            x, y = get_mouse_coords()
            if x < 0 or x > 800:
                return
            x = int(x/pixel_size)
            y = int(y/pixel_size)
            for i in range(-spawn_size-2, spawn_size + 2):
                for j in range(-spawn_size-2, spawn_size + 2):
                    if (x+j) >= 0 and (x+j) < w and (y+i) >= 0 and (y+i) < h:
                        pixels[y+i][x+j] = Pixel(x + j, y + i, PixelType.STONE)
                        pixels[y+i][x+j].velocity = 0
    def show_confirmation_dialog():
        return pygame_gui.windows.UIConfirmationDialog(
            rect=Rect((400, 300), (200, 200)),
            manager=manager,
            window_title='Confirm',
            action_long_desc='Changing the pixel size will <b>erase all existing pixels</b>. Do you want to proceed?',
            action_short_name='OK',
            blocking=False
        )

    running = True
    confirmation_dialog = None
    previous_pixel_size = pixel_slider.get_current_value()
    currentTimeCoolDown = 0
    paused = False
    next_frame = False  
    runningTime = 0
    while running:
            start_time = time.perf_counter()
            time_delta = clock.tick(120)/1000.0
            for e in event.get():
                if e.type == QUIT:
                    running = False
                manager.process_events(e)
                if e.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if e.ui_element == spawn_slider:
                        modifySpawnSize(e.value, config_obj)
                    elif e.ui_element == pixel_slider:
                        if not previous_pixel_size == pixel_slider.get_current_value():
                            if confirmation_dialog is None:
                                confirmation_dialog = show_confirmation_dialog()
                elif e.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if confirmation_dialog is not None:
                        pixels = modifyPixelSize(int(pixel_slider.get_current_value()), config_obj, pixels=pixels)
                        confirmation_dialog = None
                        previous_pixel_size = pixel_slider.get_current_value()
                elif e.type == pygame_gui.UI_WINDOW_CLOSE and e.ui_element == confirmation_dialog:
                    pixel_slider.set_current_value(previous_pixel_size)
                    confirmation_dialog = None
                elif e.type == pygame_gui.UI_BUTTON_PRESSED:
                    if e.ui_element == pause_button:
                        paused = not paused
                    elif e.ui_element == next_frame_button:
                        if paused:
                            next_frame = True
                    elif e.ui_element == rainbowmode_toggle:
                        modifyRainbowMode(config_obj)  
                    elif e.ui_element == pixel_mode_toogle:
                        pixelModeToggle(config_obj)                      
            manager.update(time_delta)
            handle_mouse_press(time_delta)
            screen.fill((20, 20, 20))
            if paused:
                time_delta = 0
            if next_frame and paused:
                time_delta = clock.tick(120)/1000.0
                next_frame = False
            render(screen, pixels=pixels, deltaTime=time_delta, runningTime=runningTime)
            screen.fill((40, 40, 40), Rect(800, 0, 200, 800))
            manager.draw_ui(screen)
            display.flip()

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            frame_rate = 1.0 / elapsed_time
            fps_text.html_text = f"<b>{int(frame_rate)} FPS</b>"
            fps_text.rebuild()
            await asyncio.sleep(0)
    quit()

if __name__ == "__main__":
    asyncio.run(main())