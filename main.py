import random
import time
import tkinter
import copy

import cv2 as cv
from enum import Enum

SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1600

SIMULATOR_WIDTH = 3840
SIMULATOR_HEIGHT = 1080

w_resize_ratio = SCREEN_WIDTH/SIMULATOR_WIDTH
h_resize_ratio = SCREEN_HEIGHT/SIMULATOR_HEIGHT


class Position(Enum):
    left_mirror = 1
    right_mirror = 2
    center_mirror = 3
    front = 4
    tachometer = 5
    infotainment = 6


def draw_crosshair(pos, img):
    tmpImg = copy.deepcopy(img)
    cv.drawMarker(tmpImg, pos_to_xy(pos), (0, 255, 0), cv.MARKER_CROSS, 100, 15)
    cv.circle(tmpImg, pos_to_xy(pos), 30, (0, 255, 0), 15)
    return tmpImg


def get_position(last_pos):
    return random.randint(1, 6)


def pos_to_xy(pos):
    if pos == 1:  # left mirror
        return round(550 * w_resize_ratio), round(850 * h_resize_ratio)
    if pos == 2:  # right mirror
        return round(3400 * w_resize_ratio), round(750 * h_resize_ratio)
    if pos == 3:  # center mirror
        return round(2420 * w_resize_ratio), round(425 * h_resize_ratio)
    if pos == 4:  # front
        return round(1730 * w_resize_ratio), round(560 * h_resize_ratio)
    if pos == 5:  # tachometer
        return round(1730 * w_resize_ratio), round(1000 * h_resize_ratio)
    if pos == 6:  # infotainment
        return round(2330 * w_resize_ratio), round(1000 * h_resize_ratio)


def save_frames(frame_count, videocapture, pos):
    if pos == 1:
        cat = 'left_mirror'
    elif pos == 2:
        cat = 'right_mirror'
    elif pos == 3:
        cat = 'center_mirror'
    elif pos == 4:
        cat = 'front'
    elif pos == 5:
        cat = 'tachometer'
    elif pos == 6:
        cat = 'infotainment'
    else:
        pass

    img_path = 'dataset/' + cat + '/'\
               + str(random.randint(1000000, 9999999))

    for i in range(1, frame_count):
        try:
            ret, frame = videocapture.read()
        except:
            print("exception videocapture failed")

        crop = frame[100:620, 330:950]
        # cv.imshow('crop', crop)
        cv.imwrite(img_path + str(i) + '.jpg', crop)
        # time.sleep(0.1)


def close():
    root.destroy()


lastpos = Position.front
cap = cv.VideoCapture(0)

root = tkinter.Tk()
root.title('Dataset Creator')

tkinter.Button(root, text="Start Calibration", command=close).pack()
root.mainloop()

simulator_screenshot = cv.imread('screenshot_simulator.png')

resized = cv.resize(simulator_screenshot, (SCREEN_WIDTH, SCREEN_HEIGHT))

timeout = 20
timeout_start = time.time()

while time.time() < timeout_start + timeout:
    position = get_position(lastpos)
    cv.imshow('Driver Dataset Creator', draw_crosshair(position, copy.deepcopy(resized)))

    if time.time() < timeout_start + 1:
        cv.waitKey()
    else:
        time.sleep(0.5)

    save_frames(10, cap, position)

    lastpos = position

    if cv.waitKey(10) == ' ':
        break

cap.release()
cv.destroyAllWindows()
