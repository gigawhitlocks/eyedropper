#!/usr/bin/python2.7

import PIL.Image # python-imaging
import PIL.ImageStat # python-imaging
import Xlib.display # python-xlib
import sys
from contextlib import contextmanager

# hide_stdout() is a hack to suppress output from an Xlib bug.
@contextmanager
def hide_stdout_core():
    save_stdout = sys.stdout
    with open("/dev/null", 'w') as sys.stdout:
        yield
    sys.stdout = save_stdout

def hide_stdout(f, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with hide_stdout_core():
            return f(*args, **kwargs)
    return wrapper

@hide_stdout
def get_pixel_color(i_x, i_y):
    o_x_root = Xlib.display.Display().screen().root
    o_x_image = o_x_root.get_image(i_x, i_y, 1, 1, Xlib.X.ZPixmap, 0xffffffff)
    o_pil_image_rgb = PIL.Image.fromstring("RGB", 
            (1, 1), o_x_image.data, "raw", "BGRX")

    lf_color = PIL.ImageStat.Stat(o_pil_image_rgb).mean
    return tuple(map(int, lf_color))


@hide_stdout
def mousepos():
    save_stdout = sys.stdout # we have to redirect stdout to silence
    sys.stdout = open('/dev/null', 'w') # a bug in the next line
    data  = Xlib.display.Display().screen().root.query_pointer()._data
    sys.stdout = save_stdout # which prints shit >(
    return data["root_x"], data["root_y"]

while(1):
    sys.stdout.write((str(get_pixel_color(*mousepos())))+"\r")


