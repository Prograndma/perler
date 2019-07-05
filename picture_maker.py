import cv2 as cv
import numpy as np
import imutils
import hitherdither
from PIL import Image
import os
from hitherdither.palette import Palette
import time


size = 250


def create_color_sample(blue_val, green_val, red_val):
    return np.asarray([[[blue_val, green_val, red_val] for pixel in range(size)] for column in range(size)],
                      dtype=np.uint8)


def create_palette_from_pictures(base_path):
    image_paths = []
    for (rootDir, dirNames, filenames) in os.walk(base_path):
        # loop over the filenames in the current directory
        for filename in filenames:
            image_paths.append(os.path.join(rootDir, filename))

    colors = []

    for i, image_name in enumerate(image_paths):
        image = cv.imread(image_name)
        if image is not None:
            # cv.imshow('orig', image)
            blue, green, red = split_image_into_bgr_grayscale(image)
            blue = np.average(blue)
            green = np.average(green)
            red = np.average(red)
            # colors.append((blue, green, red))
            colors.append((np.uint8(red), np.uint8(green), np.uint8(blue)))                           # RGB
            # cv.imshow('sample', create_color_sample(blue, green, red))
        else:
            print("problem with: ")
            print(image_name)
            print("sorry")

    return Palette(colors)


def from_cv_to_pil(image):
    img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return Image.fromarray(img)


def split_image_into_bgr_grayscale(image):
    image_b = np.array(image)[:, :, 0]
    image_g = np.array(image)[:, :, 1]
    image_r = np.array(image)[:, :, 2]
    return image_b, image_g, image_r


def split_image_into_bgr_color(image):
    b_scale = np.asarray([[[0 for pixel in range(3)] for row in range(size)] for column in range(size)], dtype=np.uint8)
    g_scale = np.asarray([[[0 for pixel in range(3)] for row in range(size)] for column in range(size)], dtype=np.uint8)
    r_scale = np.asarray([[[0 for pixel in range(3)] for row in range(size)] for column in range(size)], dtype=np.uint8)

    b_row_counter = 0
    b_column = 0
    g_row_counter = 0
    g_column = 0
    r_row_counter = 0
    r_column = 0

    blue_i, green_i, red_i = split_image_into_bgr_grayscale(image)

    for b_row, g_row, r_row in zip(b_scale, g_scale, r_scale):
        for b_pix, g_pix, r_pix in zip(b_row, g_row, r_row):
            blue, b_row, b_column = update_pixel(blue_i, b_row_counter, b_column)
            green, g_row_counter, g_column = update_pixel(green_i, g_row_counter, g_column)
            red, r_row_counter, r_column = update_pixel(red_i, r_row_counter, r_column)

            b_pix += np.asarray([blue, 0, 0], dtype=np.uint8)
            g_pix += np.asarray([0, green, 0], dtype=np.uint8)
            r_pix += np.asarray([0, 0, red], dtype=np.uint8)


def update_pixel(image, row, column):
    pix = image[row][column]
    column += 1
    if column == size:
        column = 0
        row += 1
        if row == size:
            row = 0
    return pix, row, column


def update_pixel_count(image, row, column, count):
    pix = image[row][column]
    column += 1
    if column == size:
        column = 0
        count += 1
        if count == 3:
            count = 0
            row += 1
            if row == size:
                row = 0
    return pix, row, column, count


def slash(num_shades, image):
    if num_shades > 1:
        divisor = 255 / num_shades - 1
        result = np.uint8(image / divisor)
        result = np.uint8(result * divisor)
    else:
        print("can't make so few colors")
        return None
    return result


def pixel_scatter(image, destination=None):
    if destination is None:
        temp = [[[0 for pixel in range(3)] for row in range(size * 3)] for col in range(size * 3)]
        destination = np.asarray(temp, dtype=np.uint8)

    image_blue, image_green, image_red = split_image_into_bgr_grayscale(image)

    blue_row = 0
    blue_column = 0
    blue_count = 0

    green_row = 0
    green_column = 0
    green_count = 0

    red_row = 0
    red_column = 0
    red_count = 0

    for i, row in enumerate(destination):
        for j, pixel in enumerate(row):
            if i % 3 == 0:
                if j % 3 == 0:
                    blue_pixel, blue_row, blue_column, blue_count = update_pixel_count(image_blue, blue_row,
                                                                                       blue_column, blue_count)
                    pixel += np.asarray([blue_pixel, 0, 0], dtype=np.uint8)
                elif j % 3 == 1:
                    green_pixel, green_row, green_column, green_count = update_pixel_count(image_green, green_row,
                                                                                           green_column, green_count)
                    pixel += np.asarray([0, green_pixel, 0], dtype=np.uint8)
                else:
                    red_pixel, red_row, red_column, red_count = update_pixel_count(image_red, red_row, red_column,
                                                                                   red_count)
                    pixel += np.asarray([0, 0, red_pixel], dtype=np.uint8)
            elif i % 3 == 1:
                if j % 3 == 0:
                    red_pixel, red_row, red_column, red_count = update_pixel_count(image_red, red_row, red_column,
                                                                                   red_count)
                    pixel += np.asarray([0, 0, red_pixel], dtype=np.uint8)
                elif j % 3 == 1:
                    blue_pixel, blue_row, blue_column, blue_count = update_pixel_count(image_blue, blue_row,
                                                                                       blue_column, blue_count)
                    pixel += np.asarray([blue_pixel, 0, 0], dtype=np.uint8)
                else:
                    green_pixel, green_row, green_column, green_count = update_pixel_count(image_green, green_row,
                                                                                           green_column, green_count)
                    pixel += np.asarray([0, green_pixel, 0], dtype=np.uint8)
            else:
                if j % 3 == 0:
                    green_pixel, green_row, green_column, green_count = update_pixel_count(image_green, green_row,
                                                                                           green_column, green_count)
                    pixel += np.asarray([0, green_pixel, 0], dtype=np.uint8)
                elif j % 3 == 1:
                    red_pixel, red_row, red_column, red_count = update_pixel_count(image_red, red_row, red_column,
                                                                                   red_count)
                    pixel += np.asarray([0, 0, red_pixel], dtype=np.uint8)
                else:
                    blue_pixel, blue_row, blue_column, blue_count = update_pixel_count(image_blue, blue_row,
                                                                                       blue_column, blue_count)
                    pixel += np.asarray([blue_pixel, 0, 0], dtype=np.uint8)

    return destination


def dither_image(image, palette):       # This... works? It takes about ten minutes on a 250X250 image. wow.
    print("creating a pil from cv")
    pil_image = from_cv_to_pil(image)
    print("image created")
    start = time.time()
    print("Trying to dither the image. This might fail?")
    dither = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(pil_image, palette, order=8)
    print("time elapsed dithering image: " + str(time.time() - start))
    print("dither created")
    print("attempting to show for reals now.")

    return dither


def bayer_dither(image, palette):               # quicker, can't choose palette, as far as I can tell .
    print("creating a pil from cv")
    pil_image = from_cv_to_pil(image)
    print("image created")
    start = time.time()
    print("Trying to dither the image. This might fail?")

    dithered = hitherdither.ordered.bayer.bayer_dithering(pil_image, palette, [256 / 4, 256 / 4, 256 / 4], order=8)
    print("time elapsed dithering image: " + str(time.time() - start))
    print("dither created")
    print("attempting to show for reals now.")
    return dithered


if __name__ == "__main__":
    path = 'C:\\Users\\Thomas\\Pictures\\Saved Pictures\\thomas_cropped.jpg'
    palette_path = 'C:\\Users\\Thomas\\Pictures\\perler_bead_samples'
    save_path = 'C:\\Users\\Thomas\\Pictures\\Saved Pictures\\'
    image_original = cv.imread(path)
    palette_main = create_palette_from_pictures(palette_path)

    if image_original is None:
        print("Could not load image from path:")
        print(path)
        exit()

    image_original = imutils.resize(image_original, width=size, height=size)
    perler = pixel_scatter(image_original)
    cv.imshow('pixels', perler)
    cv.imshow('original', image_original)

    cv.waitKey(0)

    print("calling dither function, expect it to take up to ten minutes. ")
    dither_image(image_original, palette_main)
    print("hopefully just showed image")
    cv.waitKey()


# ave_weird = np.average([weird_blue, weird_red, weird_green], axis=0)
