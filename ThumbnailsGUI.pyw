# -*- coding: utf-8 -*-
import tkinter as tk
import os
from modules.application import Application

root = tk.Tk()
app = Application(master=root, version="1.8")
# root.iconbitmap(os.path.abspath("app.ico"))
root.mainloop()
