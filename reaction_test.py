import dxcam
import win32api, win32con
import ctypes
import keyboard
import numpy as np
import time

ctypes.windll.shcore.SetProcessDpiAwareness(2)

camera = dxcam.create(output_color="BGR")
camera.start(target_fps=60, video_mode=True)

clicked = False
running = False

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def toggle():
    global running, clicked
    running = not running
    clicked = False
    print("started" if running else "paused")

keyboard.add_hotkey('f8', toggle)
print("f8 to start/stop, l to quit")

green_lower = np.array([61, 198, 61])
green_upper = np.array([111, 218, 81])

while True:
    if keyboard.is_pressed('l'):
        print("quitting")
        break

    if not running:
        continue

    frame = camera.get_latest_frame()
    if frame is None:
        continue

    roi = frame[0:600, 0:1920]
    mask_green = np.all((roi >= green_lower) & (roi <= green_upper), axis=2)

    green_pixels = mask_green.sum()

    if green_pixels > 5000 and not clicked:
        print(f"Green detected! ({green_pixels} pixels) clicking")
        click(960, 300)
        clicked = True
        time.sleep(0.5)
    elif green_pixels < 1000:
        clicked = False

camera.stop()