import cv2 as cv
import numpy as np
import imutils


size = 250


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


if __name__ == "__main__":
    path = 'C:\\Users\\Thomas\\Pictures\\Saved Pictures\\thomas_cropped.jpg'
    save_path = 'C:\\Users\\Thomas\\Pictures\\Saved Pictures\\'
    image_original = cv.imread(path)                                                 # BGR
    if image_original is None:
        print("Could not load image from path:")
        print(path)
        exit()

    image_original = imutils.resize(image_original, width=size, height=size)
    perler = pixel_scatter(image_original)
    perler = slash(6, perler)
    cv.imshow('pixels', perler)
    cv.imshow('original', image_original)

    cv.waitKey(0)


# ave_weird = np.average([weird_blue, weird_red, weird_green], axis=0)
