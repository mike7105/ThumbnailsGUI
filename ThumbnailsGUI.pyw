# -*- coding: utf-8 -*-
"""Приложение конвертирует изображения между форматами png jpg bmp в папке целиком,
а так же может уменьшать и менять размеры изображений"""
__version__ = '1.9'
import sys
import tkinter as tk
import os
from modules.application import Application, resource_path

if __name__ == '__main__':
    try:

        root = tk.Tk()
        app = Application(master=root, version=__version__)
        root.iconbitmap(resource_path(r"modules\ico\app.ico"))
        root.mainloop()
    except Exception as e:
        print('Unexpected error:', e)  # sys.exc_info()[0]
