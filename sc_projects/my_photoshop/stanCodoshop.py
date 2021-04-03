"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
-----------------------------------------------
This program will use all photos from the same angle to remove people or foreign objects from the pictures.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    dist = ((pixel.red-red)**2 + (pixel.green-green)**2 + (pixel.blue-blue)**2) ** 0.5
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    rgb = []
    p_red = 0
    p_green = 0
    p_blue = 0
    for i in range(len(pixels)):
        p_red += pixels[i].red
        p_green += pixels[i].green
        p_blue += pixels[i].blue
    rgb.append(int(p_red / len(pixels)))
    rgb.append(int(p_green / len(pixels)))
    rgb.append(int(p_blue / len(pixels)))
    return rgb


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    dist_p = {}
    dist_lst = []
    rgb = get_average(pixels)
    for i in range(len(pixels)):
        dist = get_pixel_dist(pixels[i], rgb[0], rgb[1], rgb[2])
        # save distance-pixel pair in the dictionary
        dist_p[dist] = pixels[i]
        dist_lst.append(dist)
    min_dist = min(dist_lst)
    best = dist_p[min_dist]
    return best


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    for i in range(width):
        for j in range(height):
            pixels = []
            for k in range(len(images)):
                img_p = images[k].get_pixel(i, j)
                pixels.append(img_p)
            best = get_best_pixel(pixels)
            result.get_pixel(i, j).red = best.red
            result.get_pixel(i, j).green = best.green
            result.get_pixel(i, j).blue = best.blue
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
