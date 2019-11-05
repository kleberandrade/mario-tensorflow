from pynput.keyboard import Key, Controller
import pynput
import time
import random
import cv2
import pyscreenshot as ImageGrab
import numpy
import pyautogui
from mss import mss

keyboard = Controller()

keys = [
    Key.up,                                 # UP
    Key.down,                               # DOWN
    Key.left,                               # LEFT
    Key.right,                              # RIGHT
    pynput.keyboard.KeyCode.from_char('x'),  # A
    pynput.keyboard.KeyCode.from_char('z'),  # B
    pynput.keyboard.KeyCode.from_char('s'),  # X
    pynput.keyboard.KeyCode.from_char('a'),  # Y
    pynput.keyboard.KeyCode.from_char('d'),  # L
    pynput.keyboard.KeyCode.from_char('c'),  # R
    Key.enter,                              # START
    Key.shift_r,                            # SELECT
]

windows_name = 'Super Mario World - Snes9x 1.60'

def get_screen_dimension(select_screen=True):
    wins_named = dict(zip(pyautogui.getAllTitles(), pyautogui.getAllWindows()))
    x = wins_named[windows_name].left
    y = wins_named[windows_name].top
    w = wins_named[windows_name].width
    h = wins_named[windows_name].height

    if select_screen:
        pyautogui.mouseDown(x + w / 2, y + h / 2)
        time.sleep(0.2)
        pyautogui.mouseUp()

    #return (x + 8, y + 52, x+w - 8, y+h - 10)
    return {"top": x + 8, "left": y + 52, "width": w - 8, "height": h - 10}

def capture_screen(dimension):
    with mss() as sct:
        screen = numpy.array(sct.grab(dimension))
        image = process_image(screen)
        return image

def process_image(image):
    image = cv2.resize(image, (0,0), fx = 0.4, fy = 0.4)
    image = cv2.Canny(image, threshold1 = 100, threshold2 = 200)
    return image

def action():
    index = random.randint(0, len(keys) - 3)
    print('Press ', keys[index])
    keyboard.press(keys[index])
    time.sleep(0.002)
    keyboard.release(keys[index])

def main():
    dimension = get_screen_dimension()
    print('Screen ', dimension)

    while True:
        last_time = time.time()
        image = capture_screen(dimension)
        action()
        print("fps: {}".format(1 / (time.time() - last_time)))

if __name__ == '__main__':
    main()