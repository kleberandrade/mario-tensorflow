from pynput.keyboard import Key, Controller
import pynput
import time
import random
import cv2
import pyscreenshot as ImageGrab
import numpy
import pyautogui

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

def log(text):
    print('[%s] %s' % (time.strftime('%H:%M:%S'), text))

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

    return (x + 8, y + 52, x+w - 8, y+h - 10)


def capture_screen(screen_dimension):
    screen = numpy.array(ImageGrab.grab(screen_dimension))
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
    time.sleep(0.2)
    keyboard.release(keys[index])

def process_image_debug():
    size = get_screen_dimension()
    image = ImageGrab.grab(size)
    image = numpy.array(image)
    image = cv2.resize(image, (0,0), fx = 0.25, fy = 0.25, interpolation=cv2.INTER_CUBIC)
    image = cv2.Canny(image, threshold1 = 100, threshold2 = 200)

def main():
    screen_dimension = get_screen_dimension()
    print('Screen ', screen_dimension)

    while True:
        t1 = time.time()
        image = capture_screen(screen_dimension)
        action()
        t2 = time.time()
        print('Elapsed: ' + str(t2 - t1))


if __name__ == '__main__':
    #main()
    process_image_debug()
