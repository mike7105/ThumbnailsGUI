# -*- coding: utf-8 -*-
"""Приложение конвертирует изображения между форматами png jpg в папке целиком,
а так же может уменьшать и менять размеры изображений"""
__version__ = '2.0'
import tkinter as tk
import traceback
import tkinter.messagebox as msgbox
import sys
from modules.application import Application, resource_path

if __name__ == '__main__':
    root = tk.Tk()
    try:
        app = Application(master=root, version=__version__)
        root.iconbitmap(resource_path(r"modules\ico\app.ico"))
        root.mainloop()
    except Exception as e:
        trace_inf = traceback.format_exc()
        print(e)
        print("Unexpected error:", trace_inf)
        msgbox.showinfo("Unexpected error:", trace_inf)
        root.destroy()
    finally:
        sys.exit()
