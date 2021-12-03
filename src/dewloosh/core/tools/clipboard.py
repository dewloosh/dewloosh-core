# -*- coding: utf-8 -*-
from PIL import ImageGrab


def save_image_on_clipboard(path, ext='PNG'):
    im = ImageGrab.grabclipboard()
    im.save(path, ext)
