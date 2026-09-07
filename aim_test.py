
#gives ~150ms on aim test

import dxcam
import win32api, win32con
import ctypes
import keyboard
import numpy as np
import time
import cv2

ctypes.windll.shcore.SetProcessDpiAwareness(2)

clickCount = 0
maxCount = 31
waitForClear = False

camera = dxcam.create(output_color="BGR")
camera.start(target_fps=60, video_mode=True)

running = False
last_click_time = 0

def stop():
    clickCount == 30

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def toggle():
    global running
    running = not running
    print("started" if running else "paused")

keyboard.add_hotkey('f8', toggle)
print("f8 to start/stop, l to quit")
keyboard.add_hotkey('f9', stop)

target_lower = np.array([212, 175, 129])
target_upper = np.array([252, 215, 169])

while True:
    if keyboard.is_pressed('l'):
        print("quitting")
        break

    if not running:
        continue

    frame = camera.get_latest_frame()
    if frame is None:
        continue

    mask = np.all((frame >= target_lower) & (frame <= target_upper), axis=2)

    if waitForClear:
        if not mask.any():
            waitForClear = False
        else:
            print(f"waiting... mask pixels: {mask.sum()}")
        continue

    if mask.any():
        ys, xs = np.where(mask)
        cx, cy = int(xs.mean()), int(ys.mean())

        now = time.time()
        if now - last_click_time > 0.05:
            click(cx, cy)
            last_click_time = now
            clickCount += 1
            print(f"click {clickCount}")
            if clickCount >= maxCount:
                running = False
                print("30 clicks, finished")
                clickCount = 0
            time.sleep(0.09)

camera.stop()