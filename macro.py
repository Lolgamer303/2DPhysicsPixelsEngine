import time
import pyautogui
import win32gui

def focus_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
    else:
        print(f"Window with title '{window_title}' not found.")

def type_and_remove_letter():
    pyautogui.click(500, 500)
    pyautogui.typewrite('a')
    pyautogui.press('backspace')

def main():
    initial_window = win32gui.GetForegroundWindow()
    initial_window_title = win32gui.GetWindowText(initial_window)
    time.sleep(5)
    current_window = win32gui.GetForegroundWindow()
    current_window_title = win32gui.GetWindowText(current_window)
    target_window_title = "pig.py - 2DPhysicsPixelsEngine - Visual Studio Code"
    print(current_window_title)
    while True:
        focus_window(initial_window_title)
        time.sleep(0.5)  # Give some time to focus
        type_and_remove_letter()
        time.sleep(0.5)  # Give some time to type and remove
        focus_window(current_window_title)
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    main()