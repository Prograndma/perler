import cv2 as cv
import numpy as np
import imutils
from copy import deepcopy as copy
from random import randint
size = 250
slash_num = 255 / 10


def update_pixel_count(image, row, column, count):
    pix = image[row][column]
    average = np.average([image_not[row][column], image_one[row][column], image_two[row][column]])
    column += 1
    if column == size:
        column = 0
        count += 1
        if count == 3:
            count = 0
            row += 1
            if row == size:
                row = 0
    return pix, row, column, count, average


def update_pixel(image, row, column):
    pix = image[row][column]
    column += 1
    if column == size:
        column -= size
        row += 1
        if row == size:
            row -= size
    return pix, row, column


if __name__ == "__main__":
    path = 'C:\\Users\\Thomas\\Pictures\\Saved Pictures\\thomas_cropped.jpg'
    image = cv.imread(path)                                                 # BGR
    image = imutils.resize(image, width=size, height=size)
    lst = [[[0 for col in range(3)] for col in range(size * 3)] for row in range(size * 3)]
    perler = np.asarray(lst, dtype=np.uint8)
    slash = np.asarray(copy(image), dtype=np.uint8)

    image_not = np.array(copy(image))[:, :, 0]
    image_one = np.array(copy(image))[:, :, 1]
    image_two = np.array(copy(image))[:, :, 2]

    to_use = 'not'
    not_row = 0
    not_column = 0
    one_row = 0
    one_column = 0
    two_row = 0
    two_column = 0
    naught_count = 0
    one_count = 0
    two_count = 0
    average = 0
    for i, row in enumerate(perler):
        for j, pixel in enumerate(row):
            if i % 3 == 0:
                if to_use == 'not':
                    naught, not_row, not_column, naught_count, average = update_pixel_count(image_not, not_row, not_column, naught_count)
                    pixel += np.asarray([naught, 0, 0], dtype=np.uint8)
                    to_use = 'one'
                elif to_use == 'one':
                    one, one_row, one_column, one_count, average = update_pixel_count(image_one, one_row, one_column, one_count)
                    pixel += np.asarray([0, one, 0], dtype=np.uint8)
                    to_use = 'two'
                else:
                    two, two_row, two_column, two_count, average = update_pixel_count(image_two, two_row, two_column, two_count)
                    pixel += np.asarray([0, 0, two], dtype=np.uint8)
                    to_use = 'not'
            elif i % 3 == 1:
                if to_use == 'not':
                    two, two_row, two_column, two_count, average = update_pixel_count(image_two, two_row, two_column, two_count)
                    pixel += np.asarray([0, 0, two], dtype=np.uint8)
                    to_use = 'one'
                elif to_use == 'one':
                    naught, not_row, not_column, naught_count, average = update_pixel_count(image_not, not_row, not_column, naught_count)
                    pixel += np.asarray([naught, 0, 0], dtype=np.uint8)
                    to_use = 'two'
                else:
                    one, one_row, one_column, one_count, average = update_pixel_count(image_one, one_row, one_column, one_count)
                    pixel += np.asarray([0, one, 0], dtype=np.uint8)
                    to_use = 'not'
            else:
                if to_use == 'not':
                    one, one_row, one_column, one_count, average = update_pixel_count(image_one, one_row, one_column, one_count)
                    pixel += np.asarray([0, one, 0], dtype=np.uint8)
                    to_use = 'one'
                elif to_use == 'one':
                    two, two_row, two_column, two_count, average = update_pixel_count(image_two, two_row, two_column, two_count)
                    pixel += np.asarray([0, 0, two], dtype=np.uint8)
                    to_use = 'two'
                else:
                    naught, not_row, not_column, naught_count, average = update_pixel_count(image_not, not_row, not_column, naught_count)
                    pixel += np.asarray([naught, 0, 0], dtype=np.uint8)
                    to_use = 'not'

    blue_scale = np.asarray([[[0 for col in range(3)] for col in range(size)] for row in range(size)], dtype=np.uint8)
    green_scale = np.asarray([[[0 for col in range(3)] for col in range(size)] for row in range(size)], dtype=np.uint8)
    red_scale = np.asarray([[[0 for col in range(3)] for col in range(size)] for row in range(size)], dtype=np.uint8)

    not_row = 0
    not_column = 0
    one_row = 0
    one_column = 0
    two_row = 0
    two_column = 0

    for blue_row, green_row, red_row in zip(blue_scale, green_scale, red_scale):
        for b_pix, g_pix, r_pix in zip(blue_row, green_row, red_row):
            naught, not_row, not_column = update_pixel(image_not, not_row, not_column)
            one, one_row, one_column = update_pixel(image_one, one_row, one_column)
            two, two_row, two_column = update_pixel(image_two, two_row, two_column)

            b_pix += np.asarray([naught, 0, 0], dtype=np.uint8)
            g_pix += np.asarray([0, one, 0], dtype=np.uint8)
            r_pix += np.asarray([0, 0, two], dtype=np.uint8)

    slash = np.uint8(slash / slash_num)
    slash = np.uint8(slash * slash_num)

    # perler = imutils.resize(perler, width=size, height=size)

    cv.imshow('blue_scale', blue_scale)
    cv.imshow('green_scale', green_scale)
    cv.imshow('red_scale', red_scale)

    cv.imshow('not', image_not)
    cv.imshow('one', image_one)
    cv.imshow('two', image_two)

    cv.imshow('pixels', perler)
    cv.imshow('original', image)
    cv.imshow('slash', slash)

    cv.imshow('blow_up', imutils.resize(perler, width=size * 12))
    # if not cv.imwrite(path + 'blue.png', imutils.resize(perler, width=size * 12)):
    #     print("couldn't save")

    weird_blue = cv.imread(path + 'blue.png')
    weird_green = cv.imread(path + 'green.png')
    weird_red = cv.imread(path + 'red.png')

    ave_weird = np.average([weird_blue, weird_red, weird_green], axis=0)

    cv.imshow('ave_weird', ave_weird)
    # if not cv.imwrite(path + 'ave.png', ave_weird):
    #     print("couldn't save")
    cv.waitKey(0)
