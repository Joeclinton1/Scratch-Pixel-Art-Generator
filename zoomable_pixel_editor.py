from tkinter import *
from PIL import Image, ImageTk
from math import floor, sqrt
import numpy as np

size = 64
imgName = 'image.jpg'
lookup = "0123456789abcdef"
colour2pos = open('colour2pos.txt', 'r').readlines()
palette = []
for i, hex_colour in enumerate(colour2pos):
    if i % 4 == 0:
        palette.append([lookup.find(l) for l in list(hex_colour[:-1])])


def resize(img_path, size):
    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(img_path)
    ratio = img.size[0] / float(img.size[1])

    if ratio > 1:  # horizontal > vertical
        img = img.resize((size, size * img.size[1] // img.size[0]),
                         Image.ANTIALIAS)
    elif ratio < 1:  # vertical > horizontal
        img = img.resize((size * img.size[1] // img.size[0], size),
                         Image.ANTIALIAS)
    else:
        img = img.resize((size, size), Image.ANTIALIAS)
    return img


def get_closest_colour(c):
    def dist2colour(p):
        return sqrt((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 + (p[2] - c[2]) ** 2)
    min_c = min(palette, key=dist2colour)
    print(c, min_c)
    return min_c


def get_save_code(img):
    pixels = np.array(img)
    dim = img.size
    shift = [floor(x / 2) for x in dim]
    code = '1'
    padding = []

    # add the markup data
    for i in range(2):
        code += str(len(str(shift[i])))
        code += str(shift[i])
        padding.append(len(hex(dim[i])) - 2)
        code += str(padding[-1])

    # add the pixel data
    for y in range(dim[1]):
        for x in range(dim[0]):
            hex_colour = ''.join([lookup[l // 16] for l in pixels[-y + dim[1] - 1, x]])

            # change colour if hex_colour is not in pallette
            rgb = [l // 16 for l in pixels[-y + dim[1] - 1, x]]
            if rgb not in palette:
                hex_colour = ''.join([lookup[l] for l in get_closest_colour(rgb)])

            if hex_colour != 'fff':
                for i, z in enumerate((x, y)):
                    hex_val = str(hex(z)[2:])
                    code += (padding[i] - len(hex_val)) * '0' + hex_val
                code += hex_colour
    return code


def display_image(img):
    pixels_img = [tuple([y // 16 * 16 for y in x]) for x in list(img.getdata())]
    img.putdata(pixels_img)
    img_tk = ImageTk.PhotoImage(img)
    root.img_tk = img_tk
    canvas.itemconfig(thumbnail, image=img_tk)


def read_image():
    img = resize(imgName, size).convert("RGB")

    display_image(img)
    print(get_save_code(img))


root = Tk()
root.title("OpenCV and Tkinter")

canvas = Canvas(root, width=200, height=200)
canvas.pack()
img_placeholder = ImageTk.PhotoImage(file=imgName)
thumbnail = canvas.create_image((0, 0), image=img_placeholder, anchor=NW)

read_image()

root.mainloop()
