import os
import cv2
import numpy as np

img_dir = "./imgs/"


def calc_green_pixels(folder):
    lix = []
    liy = []
    for image in os.listdir(folder):
        img = cv2.imread(folder+image)

        scale_percent = 50  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

        imask = mask > 0
        green = np.zeros_like(resized, np.uint8)
        green[imask] = resized[imask]
        count = cv2.countNonZero(mask)

        lix.append(int(image.split('.')[0][1:]))
        liy.append(count)
    return (lix, liy)