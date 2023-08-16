import cv2
import numpy as np
import pyautogui
import os
import subprocess
import time
from io import BytesIO
import win32clipboard
from PIL import Image


web_load = 5
image_load = 20

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


urls = []
images = []
with open("urls.txt") as lines:
    urls.append(lines.read())

with open("images.txt") as lines:
    images.append(lines.read())

for url in urls:
    # os.system(f"chrome {url}")
    subprocess.run(["chrome",f"{url}"])
    time.sleep(web_load)

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.png")

    img_rgb = cv2.imread('screenshot.png')
    template = cv2.imread('comment_white.png')
    w, h = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    #! comment location
    X, Y = pt

    #! click comment box
    pyautogui.click(x=X+10, y=Y+10)
    for filepath in images:
        image = Image.open(filepath)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        send_to_clipboard(win32clipboard.CF_DIB, data)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(image_load)
        pyautogui.press("enter")
        time.sleep(10)
        pyautogui.press("enter")
