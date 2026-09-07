
#gives avrage of ~100ms on reaction test
#depeding on fps it gives ~90-120ms for me
import dxcam
import win32api, win32con
import ctypes
import keyboard
import numpy as np
import time
import cv2

ctypes.windll.shcore.SetProcessDpiAwareness(2)

camera = dxcam.create(output_color="BGR", region=(0, 0, 1920, 600))
camera.start(target_fps=120, video_mode=True)

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

green_lower = np.array([61, 198, 61], dtype=np.uint8)
green_upper = np.array([111, 218, 81], dtype=np.uint8)

while True:
    if keyboard.is_pressed('l'):
        print("quitting")
        break

    if not running:
        continue

    frame = camera.get_latest_frame()
    if frame is None:
        continue

    green_pixels = cv2.countNonZero(cv2.inRange(frame, green_lower, green_upper))

    if green_pixels > 5000 and not clicked:
        print(f"Green detected! ({green_pixels} pixels) clicking")
        click(960, 300)
        clicked = True
    elif green_pixels < 1000:
        clicked = False

camera.stop()