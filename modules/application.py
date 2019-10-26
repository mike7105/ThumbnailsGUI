# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as tkFD
from modules.Images import Thumb
import modules.htmblocks as htm
from PIL import Image, ImageTk
import glob
import shelve
import os
import re
import time
import threading
import queue
import webbrowser


class Application(ttk.Notebook):
    def __init__(self, master=None, version=""):
        super().__init__(master)
        self.version = version
        self.grid(row=0, column=0, columnspan=2, sticky="wnse")

        # LabelStatus
        self.lblStatus = ttk.Label(text="Статус: [0/0]")
        self.lblStatus.grid(row=1, column=0, sticky="wes", padx=4, pady=4)

        # Button
        self.btnExit = ttk.Button(text="Выход", command=self.master.destroy)
        self.btnExit.grid(row=1, column=1, sticky="es", padx=4, pady=4)

        # ProgressBar
        self.varPB = tk.IntVar()
        self.pgb = ttk.Progressbar(
            maximum=100, variable=self.varPB, length=300)
        # self.varPB.set(0)
        self.pgb.grid(row=2, column=0, sticky="we")

        # Sizegrip
        self.sgp = ttk.Sizegrip()
        self.sgp.grid(row=2, column=1, sticky="es")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.master.title("Работа с картинками")
        left = str(int((self.winfo_screenwidth()-600)/2))
        top = str(int((self.winfo_screenheight()-400)/2))
        self.master.geometry("=600x400+" + left + "+" + top)
        self.master.minsize(width=300, height=300)

        self.th = Thumb()
        self.th.suffix = ""

        self.th2 = Thumb()

        self.create_menu()
        self.create_widgets()

        # #####STYLE#######
        self.s = ttk.Style()
        # self.s.configure(".", background="red")
        # self.s.map('TCombobox', fieldbackground=[('readonly','white')])
        # self.s.configure("btnRed", background="red")

    def create_menu(self):
        # pimage = Image.open(
        # os.path.join(os.getcwd(),r"modules/ico/open.png"))
        # pimage = Image.open(os.path.abspath(r"modules/ico/open.png"))
        self.open_image = None  # ImageTk.PhotoImage(pimage)
        # pimage = Image.open(os.path.abspath(r"modules/ico/save.png"))
        self.save_image = None  # ImageTk.PhotoImage(pimage)
        # pimage = Image.open(os.path.abspath(r"modules/ico/about.png"))
        self.about_image = None  # ImageTk.PhotoImage(pimage)

        # Создаем само главное меню и назначаем его окну приложения
        window = self.master
        self.mainmenu = tk.Menu(window, tearoff=False)
        window["menu"] = self.mainmenu

        # Создаем подменю Файл
        self.filemenu = tk.Menu(self.mainmenu, tearoff=False)

        self.filemenu.add_command(
            label="Открыть", accelerator="Ctrl+O", image=self.open_image,
            compound=tk.LEFT, command=self.open_file)
        self.bind_all("<Control-KeyPress-o>", self.open_file)

        self.filemenu.add_command(
            label="Сохранить", accelerator="Ctrl+S", image=self.save_image,
            compound=tk.LEFT, command=self.save_file)
        self.bind_all("<Control-KeyPress-s>", self.save_file)

        self.filemenu.add_command(
            label="Создать htm Dim",
            accelerator="Ctrl+D", command=self.createHTMDim)
        self.bind_all("<Control-KeyPress-d>", self.createHTMDim)

        self.filemenu.add_separator()

        self.filemenu.add_command(
            label="Выход", accelerator="Ctrl+Q", command=self.master.destroy)
        self.bind_all(
            "<Control-KeyPress-q>", lambda evt: self.btnExit.invoke())

        self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)

        # Добавляем меню Настройки в главное меню
        self.thememenu = tk.Menu(self.mainmenu, tearoff=False)
        self.them = tk.StringVar()
        self.them.set("vista")
        self.tharr = ["default", "winnative", "clam", "alt", "classic", "vista", "xpnative"]

        for s in self.tharr:
            self.thememenu.add_radiobutton(
                label=s, variable=self.them, value=s,
                command=self.change_theme)
        self.mainmenu.add_cascade(label="Темы", menu=self.thememenu)

        # Создаем подменю Справка
        self.helpmenu = tk.Menu(self.mainmenu, tearoff=False)
        self.helpmenu.add_command(
            label="О программе...", image=self.about_image,
            compound=tk.LEFT, command=self.show_info)
        self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)

        # Контекстное меню
        self.contextmenu = tk.Menu(self, tearoff=False)
        self.contextmenu.add_command(label="Скопировать", command=self.copy)

    def create_widgets(self):
        grid_params = {"padx": 4, "pady": 4}

        # ###############Notebook converter_png_jpg############################
        self.frame1 = ttk.Frame(self)

        # LabelConv
        self.lblConv = ttk.Label(self.frame1, text="Выберите тип конвертера:")
        self.lblConv.grid(row=0, column=0, sticky="we", **grid_params)

        # Combobox
        self.convs = {"1. png -> jpg": "1", "2. jpg -> png": "2"}
        self.cboConv = ttk.Combobox(
            self.frame1, values=list(self.convs.keys()), exportselection=0)
        self.cboConv.state(['readonly'])
        self.cboConv.bind("<<ComboboxSelected>>", self.set_types)
        self.cboConv.grid(row=1, column=0, sticky="we", **grid_params)

        # LabelErr
        self.lblErr = ttk.Label(self.frame1, text="")
        self.lblErr.grid(row=1, column=1, sticky="w", **grid_params)

        # LabelInitDir
        self.lblInitDir = ttk.Label(
            self.frame1, text="Путь к {0} картинкам:".format(self.th.ftype))
        self.lblInitDir.grid(row=2, column=0, sticky="we", **grid_params)

        # EntryInitDir
        self.varInitDir = tk.StringVar()
        self.varInitDir.set("")
        self.entInitDir = ttk.Entry(self.frame1, textvariable=self.varInitDir)
        self.entInitDir.state(["disabled"])
        self.entInitDir.grid(row=3, column=0, sticky="we", **grid_params)
        self.entInitDir.bind(
            "<Button-3>",
            lambda evt, obj=self.varInitDir: self.show_menu(evt, obj))

        # ButtonInitDir
        self.btnInitDir = ttk.Button(
            self.frame1, text="Выбрать...", command=self.open_InitDir)
        self.btnInitDir.grid(row=3, column=1, sticky="we", **grid_params)

        # LabelOutDir
        self.lblOutDir = ttk.Label(
            self.frame1, text="Путь к {0} картинкам:".format(self.th.otype))
        self.lblOutDir.grid(row=4, column=0, sticky="we", **grid_params)

        # EntryOutDir
        self.varOutDir = tk.StringVar()
        self.varOutDir.set("")
        self.entOutDir = ttk.Entry(self.frame1, textvariable=self.varOutDir)
        self.entOutDir.state(["disabled"])
        self.entOutDir.grid(row=5, column=0, sticky="we", **grid_params)
        self.entOutDir.bind(
            "<Button-3>",
            lambda evt, obj=self.varOutDir: self.show_menu(evt, obj))

        # ButtonOutDir
        self.btnOutDir = ttk.Button(
            self.frame1, text="Выбрать...", command=self.open_OutDir)
        self.btnOutDir.grid(row=5, column=1, sticky="we", **grid_params)

        # ButtonConvert
        self.btnConvert = ttk.Button(
            self.frame1, text="Конвертировать", command=self.convert)
        self.btnConvert.grid(row=6, column=0, columnspan=2, **grid_params)

        self.add(self.frame1, text="Конвертер", padding=2)
        self.frame1.grid_columnconfigure(0, weight=2, pad=4)
        self.frame1.grid_columnconfigure(1, weight=1, pad=4)

        # ################Notebook thumbnails##################################
        self.frame2 = ttk.Frame(self)

        # LabelSize
        self.lblSize = ttk.Label(self.frame2, text="Введите размеры:")

        # LabelFrame
        self.lbFrame = ttk.LabelFrame(self.frame2, labelwidget=self.lblSize)
        self.lbFrame.grid(
            row=0, column=0, columnspan=3, sticky="we", **grid_params)

        # Radiobutton
        self.varDim = tk.IntVar()
        # self.varDim.set()
        self.rdb1 = ttk.Radiobutton(
            self.lbFrame, text="Ширина", value=1, variable=self.varDim,
            command=self.changeDim)
        self.rdb1.grid(row=0, column=0, sticky="w", **grid_params)
        self.rdb2 = ttk.Radiobutton(
            self.lbFrame, text="Высота", value=2, variable=self.varDim,
            command=self.changeDim)
        self.rdb2.grid(row=0, column=1, sticky="w", **grid_params)
        self.rdb3 = ttk.Radiobutton(
            self.lbFrame, text="Квадрат", value=3, variable=self.varDim,
            command=self.changeDim)
        self.rdb3.grid(row=0, column=2, sticky="w", **grid_params)

        # EntrySize
        self.pre = re.compile(r"^\d+$")
        v = self.register(self.is_num)
        self.varSize = tk.IntVar()
        self.varSize.set(0)
        self.entSize = ttk.Entry(
            self.lbFrame, textvariable=self.varSize, validatecommand=(v, "%P"),
            validate="focusout", invalidcommand=self.invalid_nums)
        self.entSize.state(["disabled"])
        self.entSize.grid(row=1, column=0, sticky="we", **grid_params)

        # LabelErr2
        self.lblErr2 = ttk.Label(self.lbFrame, text="")
        self.lblErr2.grid(row=1, column=1, sticky="we", **grid_params)

        self.lbFrame.grid_columnconfigure(0, weight=1, pad=4)
        self.lbFrame.grid_columnconfigure(1, weight=1, pad=4)
        self.lbFrame.grid_columnconfigure(2, weight=1, pad=4)

        # LabelType
        self.lblType = ttk.Label(
            self.frame2, text="Введите расширение картинок:")
        self.lblType.grid(row=1, column=0, sticky="we", **grid_params)

        # ComboboxType
        self.types = ["png", "jpg", "bmp"]
        self.cboType = ttk.Combobox(
            self.frame2, values=self.types, exportselection=0)
        self.cboType.state(['readonly'])
        self.cboType.bind("<<ComboboxSelected>>", self.set_types)
        self.cboType.grid(row=1, column=1, sticky="we", **grid_params)

        # LabelSuf
        self.lblSuf = ttk.Label(
            self.frame2, text="Приписка (суффикс) к новым картинкам:")
        self.lblSuf.grid(row=2, column=0, sticky="we", **grid_params)

        # EntrySuf
        self.varSuf = tk.StringVar()
        self.varSuf.set("")
        self.entSuf = ttk.Entry(self.frame2, textvariable=self.varSuf)
        self.entSuf.bind("<FocusOut>", self.set_suf)
        self.entSuf.grid(row=2, column=1, sticky="we", **grid_params)

        # LabelInitDir2
        self.lblInitDir2 = ttk.Label(
            self.frame2, text="Путь к оригинальным картинкам:")
        self.lblInitDir2.grid(
            row=3, column=0, columnspan=2, sticky="we", **grid_params)

        # EntryInitDir2
        self.varInitDir2 = tk.StringVar()
        self.varInitDir2.set("")
        self.entInitDir2 = ttk.Entry(
            self.frame2, textvariable=self.varInitDir2)
        self.entInitDir2.state(["disabled"])
        self.entInitDir2.grid(
            row=4, column=0, columnspan=2, sticky="we", **grid_params)
        self.entInitDir2.bind(
            "<Button-3>",
            lambda evt, obj=self.varInitDir2: self.show_menu(evt, obj))

        # ButtonInitDir2
        self.btnInitDir2 = ttk.Button(
            self.frame2, text="Выбрать...", command=self.open_InitDir)
        self.btnInitDir2.grid(row=4, column=2, sticky="we", **grid_params)

        # LabelOutDir2
        self.lblOutDir2 = ttk.Label(
            self.frame2, text="Путь к новым картинкам:")
        self.lblOutDir2.grid(
            row=5, column=0, columnspan=2, sticky="we", **grid_params)

        # EntryOutDir2
        self.varOutDir2 = tk.StringVar()
        self.varOutDir2.set("")
        self.entOutDir2 = ttk.Entry(self.frame2, textvariable=self.varOutDir2)
        self.entOutDir2.state(["disabled"])
        self.entOutDir2.grid(
            row=6, column=0, columnspan=2, sticky="we", **grid_params)
        self.entOutDir2.bind(
            "<Button-3>",
            lambda evt, obj=self.varOutDir2: self.show_menu(evt, obj))

        # ButtonOutDir2
        self.btnOutDir2 = ttk.Button(
            self.frame2, text="Выбрать...", command=self.open_OutDir)
        self.btnOutDir2.grid(row=6, column=2, sticky="we", **grid_params)

        # ButtonResize
        self.btnResize = ttk.Button(
            self.frame2, text="Уменьшить", command=self.resize)
        self.btnResize.grid(row=7, column=0, **grid_params)

        # ButtonEnlarge
        self.btnEnlarge = ttk.Button(
            self.frame2, text="Оквадратить", command=self.enlarge)
        self.btnEnlarge.grid(row=7, column=1, **grid_params)

        self.add(self.frame2, text="Размеры", padding=2)
        self.frame2.grid_columnconfigure(0, weight=2, pad=4)
        self.frame2.grid_columnconfigure(1, weight=2, pad=4)
        self.frame2.grid_columnconfigure(2, weight=1, pad=4)

    def open_file(self, evt=None):
        """Считывание сохраненных ранее параметров"""
        ind = self.index("current")
        filename = tkFD.askopenfilename(
            title="Выберите файл настроек",
            filetypes=(("Файл настроек", "DAT"),))
        if filename:
            filename = os.path.splitext(filename)[0]
            db = shelve.open(filename)
            if ind == self.index(self.frame1):
                self.th = db.get("conv")
            elif ind == self.index(self.frame2):
                self.th2 = db.get("resize")
            db.close()

            if self.th is not None:
                self.varInitDir.set(self.th.initdir)
                self.varOutDir.set(self.th.outdir)
                if self.th.ftype == "png":
                    self.cboConv.current(0)
                else:
                    self.cboConv.current(1)
                self.lblErr["text"] = ""
                self.lblErr["background"] = ""

            if self.th2 is not None:
                self.varInitDir2.set(self.th2.initdir)
                self.varOutDir2.set(self.th2.outdir)
                if self.th2.ftype == "png":
                    self.cboType.current(0)
                elif self.th2.ftype == "jpg":
                    self.cboType.current(1)
                elif self.th2.ftype == "bmp":
                    self.cboType.current(2)

                if self.th2.size[0] > 0 and self.th2.size[1] > 0:
                    self.varSize.set(self.th2.size[0])
                    self.varDim.set(3)
                    self.btnResize.state(["disabled"])
                    self.btnEnlarge.state(["!disabled"])
                elif self.th2.size[0] > 0:
                    self.varSize.set(self.th2.size[0])
                    self.varDim.set(1)
                    self.btnResize.state(["!disabled"])
                    self.btnEnlarge.state(["disabled"])
                elif self.th2.size[1] > 0:
                    self.varSize.set(self.th2.size[1])
                    self.varDim.set(2)
                    self.btnResize.state(["!disabled"])
                    self.btnEnlarge.state(["disabled"])

                self.entSize.state(["!disabled"])
                self.lblType["background"] = ""
                self.lblErr2["text"] = ""
                self.lblErr2["background"] = ""
                self.varSuf.set(self.th2.suffix)
        else:
            msgbox.showerror(
                title="Открытие файла настроек", message="Файл не выбран!")

    def save_file(self, evt=None):
        """Сохранение введенных параметров"""
        ind = self.index("current")
        filename = tkFD.asksaveasfilename(
            title="Сохранение настроек", filetypes=(("Файл настроек", "DAT"),))
        if filename:
            filename = os.path.splitext(filename)[0]
            db = shelve.open(filename)
            if ind == self.index(self.frame1):
                db["conv"] = self.th
            elif ind == self.index(self.frame2):
                db["resize"] = self.th2
            db.close()
        else:
            msgbox.showerror("Сохранение файла настроек", "Файл не выбран!")

    def show_info(self):
        """Показ информации"""
        msgbox.showinfo("О программе...", """Version: {0}
© Михаил Чесноков, 2019 г.
mailto: Mihail.Chesnokov@ipsos.com""".format(self.version), parent=self)

    def set_suf(self, evt):
        """Установка суффикса"""
        self.th2.suffix = self.varSuf.get()

    def set_types(self, evt):
        """Проставляет расширения входных/выходных
        файлов согласно выбранным параметрам"""
        ind = self.index("current")
        if ind == self.index(self.frame1):
            if self.convs[self.cboConv.get()] == "1":
                self.th.ftype = "png"
                self.th.otype = "jpg"
            else:
                self.th.ftype = "jpg"
                self.th.otype = "png"
            self.lblInitDir["text"] = "Путь к {0} картинкам:".format(
                self.th.ftype)
            self.lblOutDir["text"] = "Путь к {0} картинкам:".format(
                self.th.otype)
            self.lblErr["text"] = ""
            self.lblErr["background"] = ""
        elif ind == self.index(self.frame2):
            self.th2.ftype = self.cboType.get()
            self.th2.otype = self.cboType.get()
            self.lblType["background"] = ""

    def open_InitDir(self):
        """Выбор директории для изначальных файлов"""
        filename = tkFD.askdirectory(title="Выберите директорию")
        ind = self.index("current")
        if ind == self.index(self.frame1):
            self.varInitDir.set(filename)
            self.th.initdir = filename
        elif ind == self.index(self.frame2):
            self.varInitDir2.set(filename)
            self.th2.initdir = filename

    def open_OutDir(self):
        """Выбор директории для выходных файлов"""
        filename = tkFD.askdirectory(title="Выберите директорию")
        ind = self.index("current")
        if ind == self.index(self.frame1):
            self.varOutDir.set(filename)
            self.th.outdir = filename
        elif ind == self.index(self.frame2):
            self.varOutDir2.set(filename)
            self.th2.outdir = filename

    def convert(self):
        """Конвертирование картинок в другой формат"""
        # self.varPB.set()
        if not self.check():
            msgbox.showerror("Ошибка!", "Заполните все поля!!")
        else:
            self.images = glob.glob(self.th.initdir + "\\*." + self.th.ftype)
            self.pgb["maximum"] = len(self.images)

            self.t1 = time.time()

            self.lock = threading.Lock()
            self.q = queue.Queue()
            for infile in self.images:
                self.q.put(infile)

            threads = []
            self.barrier = threading.Barrier(6)
            for i in range(0, 5):
                t = threading.Thread(target=self.convertTH2)
                threads.append(t)
                t.start()
            t = threading.Thread(target=self.tm)
            threads.append(t)
            t.start()

    def tm(self):
        """Функция для завершающего потока"""
        self.barrier.wait()
        self.t2 = time.time()
        self.tr = self.t2 - self.t1
        # print(self.tr)
        self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
            self.pgb["maximum"], self.pgb["maximum"])

    def convertTH2(self):
        """Многопоточное конвертирование"""
        local = threading.local()
        while not self.q.empty():
            local.infile = self.q.get()
            local.im = Image.open(local.infile)
            if self.th.otype == "png":
                local.im2 = local.im.convert("RGBA")
            else:
                local.im2 = local.im.convert("RGB")
            local.outfile = self.th.get_outfile(local.infile)
            local.im2.save(local.outfile)  # , quality=100)
            with self.lock:
                self.pgb.step()
                self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                    self.varPB.get(), self.pgb["maximum"])
            self.q.task_done()
        self.barrier.wait()

    def convertNoTH(self):
        """Последовательное конвертирование"""
        for infile in self.images:
            im = Image.open(infile)
            if self.th.otype == "png":
                im2 = im.convert("RGBA")
            else:
                im2 = im.convert("RGB")
            outfile = self.th.get_outfile(infile)
            im2.save(outfile)  # , quality=100)

            self.after(0, self.pgb.step())
            self.pgb.update()
            self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                self.varPB.get(), self.pgb["maximum"])

    def resize(self):
        """Изменение размеров картинок"""
        # self.varPB.set(0)
        self.th2.suffix = self.varSuf.get()
        if not self.check():
            msgbox.showerror("Ошибка!", "Заполните все поля!!")
        else:
            images = glob.glob(self.th2.initdir + "\\*." + self.th2.ftype)
            self.pgb["maximum"] = len(images)
            for infile in images:
                im = Image.open(infile)
                im.thumbnail(self.th2.size)
                outfile = self.th2.get_outfile(infile)
                im.save(outfile)  # , quality=100)
                self.after(0, self.pgb.step())
                self.pgb.update()
                self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                    self.varPB.get(), self.pgb["maximum"])
            # self.varPB.set(self.pgb["maximum"])
            self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                self.pgb["maximum"], self.pgb["maximum"])

    def enlarge(self):
        """Вписывание кратинки в заданные размеры,
        добавляя белые или прозрачные поля"""
        # self.varPB.set(0)
        self.th2.suffix = self.varSuf.get()
        if not self.check():
            msgbox.showerror("Ошибка!", "Заполните все поля!!")
        else:
            images = glob.glob(self.th2.initdir + "\\*." + self.th2.ftype)
            self.pgb["maximum"] = len(images)
            for infile in images:
                im = Image.open(infile)
                if im.size[0] > self.th2.size[0] or \
                im.size[1] > self.th2.size[1]:
                    im.thumbnail(self.th2.size)
                if self.th2.ftype == "png":
                    im2 = Image.new("RGBA", self.th2.size, (255, 255, 255, 0))
                else:
                    im2 = Image.new("RGB", self.th2.size, (255, 255, 255))

                im2.paste(im, (
                    int((self.th2.size[0]-im.size[0])/2),
                    int((self.th2.size[1]-im.size[1])/2)))

                outfile = self.th2.get_outfile(infile)
                im2.save(outfile)  # , quality=100)
                self.after(0, self.pgb.step())
                self.pgb.update()
                self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                    self.varPB.get(), self.pgb["maximum"])
            # self.varPB.set(self.pgb["maximum"])
            self.lblStatus["text"] = "Статус: [{0}/{1}]".format(
                self.pgb["maximum"], self.pgb["maximum"])

    def createHTMDim(self, evt=None):
        """Создает htm файл MultiCol из картинок в выходнйо директории"""
        ind = self.index("current")
        if ind == self.index(self.frame1):
            outdir = self.th.outdir
            images = glob.glob(
                self.th.outdir + "\\*" + self.th.suffix +
                "." + self.th.otype)
        elif ind == self.index(self.frame2):
            outdir = self.th2.outdir
            images = glob.glob(
                self.th2.outdir + "\\*" + self.th2.suffix +
                "." + self.th2.otype)

        if len(images) > 0:
            with open(outdir + "\\MA2.htm", "w", encoding="utf-8") as f:
                f.write(htm.startHTM)
                i = 0
                for im in images:
                    f.write(htm.blockHTM.format(
                        i, i+1, i, i+1, i, "Марка", os.path.basename(im)))
                    i += 1
                f.write(htm.endHTM)
            webbrowser.open_new_tab(outdir + "\\MA2.htm")
        else:
            if ind == self.index(self.frame1):
                msgbox.showerror(
                    "Ошибка!", "Картинок не найдено: " + self.th.outdir +
                    "\\*" + self.th.suffix + "." + self.th.otype)
            elif ind == self.index(self.frame2):
                msgbox.showerror(
                    "Ошибка!", "Картинок не найдено: " + self.th2.outdir +
                    "\\*" + self.th2.suffix + "." + self.th2.otype)

    def changeDim(self):
        """Действия при переключения опций"""
        if self.varDim.get() == 1 or self.varDim.get() == 2:
            self.btnResize.state(["!disabled"])
            self.btnEnlarge.state(["disabled"])
        else:
            self.btnResize.state(["disabled"])
            self.btnEnlarge.state(["!disabled"])

        if self.varDim.get() == 1:
            self.th2.size = (self.varSize.get(), 9999)
        elif self.varDim.get() == 2:
            self.th2.size = (9999, self.varSize.get())
        elif self.varDim.get() == 3:
            self.th2.size = (self.varSize.get(), self.varSize.get())
        self.entSize.state(["!disabled"])

    def show_menu(self, evt, obj):
        """Показывает контекстное меню"""
        self.compToCopy = obj.get()
        self.contextmenu.post(evt.x_root, evt.y_root)

    def copy(self):
        """Копирует содержимое путей"""
        # print(self.compToCopy)
        self.clipboard_clear()
        self.clipboard_append(self.compToCopy)

    def change_theme(self):
        """меняет внешний вид при выборе встроенных тем"""
        self.s.theme_use(self.them.get())

    # валидация
    def is_num(self, value):
        """Проверка, что введенное значение - число"""
        if self.pre.match(value):
            if self.varDim.get() == 1:
                self.th2.size = (self.varSize.get(), 9999)
            elif self.varDim.get() == 2:
                self.th2.size = (9999, self.varSize.get())
            elif self.varDim.get() == 3:
                self.th2.size = (self.varSize.get(), self.varSize.get())
            if self.varSize.get() > 0:
                self.lblErr2["text"] = ""
                self.lblErr2["background"] = ""
            return True
        else:
            return False

    def invalid_nums(self):
        """Ошибка при вводе размера"""
        self.varSize.set(0)
        self.entSize.focus_set()

    def check(self):
        """Проверка на заполненность всех полей"""
        ind = self.index("current")
        if ind == self.index(self.frame2):
            if self.th2.ftype == "" or self.th2.otype == "" or \
            self.th2.initdir == "" or self.th2.outdir == "" or \
            self.th2.size[0] == 0 or self.th2.size[1] == 0:
                if self.th2.ftype == "" or self.th2.otype == "":
                    self.cboType.focus_set()
                    self.lblType["background"] = "red"
                if self.th2.initdir == "":
                    self.varInitDir2.set("!!!")
                if self.th2.outdir == "":
                    self.varOutDir2.set("!!!")
                if self.th2.size[0] == 0 or self.th2.size[1] == 0:
                    self.entSize.focus_set()
                    self.lblErr2["text"] = "!!!"
                    self.lblErr2["background"] = "red"
                return False
            else:
                return True
        elif ind == self.index(self.frame1):
            if self.th.ftype == "" or self.th.otype == "" or \
            self.th.initdir == "" or self.th.outdir == "":
                if self.th.ftype == "" or self.th.otype == "":
                    self.cboConv.focus_set()
                    self.lblErr["text"] = "!!!"
                    self.lblErr["background"] = "red"
                if self.th.initdir == "":
                    self.varInitDir.set("!!!")
                if self.th.outdir == "":
                    self.varOutDir.set("!!!")
                return False
            else:
                return True

if __name__ == "__main__":
    pass
