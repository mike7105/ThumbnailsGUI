# -*- coding: utf-8 -*-
"""модуль с классом для картинок Thumb"""
import os
import glob
import tkinter.messagebox as msgbox


class Thumb:
    """Класс содержит информацию по формированию уменьшенных картинок
        size -- разрешение выходной картинки
        ftype -- тип картинок на вход: jpg, png, bmp
        otype -- тип картинок на выход: jpg, png, bmp
        initdir -- папка с исходными изображениями
        outdir -- папка с выходными кратинками
        suffix -- суффикс, который прибавится к имени исходного файла,
        чтобы получить выходной файл
       """

    def __init__(self):
        self.__size = (0, 0)
        self.__ftype = ""
        self.__otype = ""
        self.__initdir = ""
        self.__outdir = ""
        self.__suffix = "t"

    @property
    def suffix(self):
        """Получить суффикс файла выходных картинок"""
        return self.__suffix

    @suffix.setter
    def suffix(self, value):
        value = value.strip()
        self.__suffix = value

    @property
    def initdir(self):
        """Получить директорию с изначальными картинками"""
        return self.__initdir

    @initdir.setter
    def initdir(self, value):
        value = os.path.normpath(value.strip())
        if not os.path.exists(value):
            # print("Такой директории не существует!")
            msgbox.showerror("Ошибка!", "Такой директории не существует!")
            self.__initdir = ""
        elif value == ".":
            # print("Путь не введён!")
            msgbox.showerror("Ошибка!", "Путь не введён!")
            self.__initdir = ""
        else:
            self.__initdir = value

    @property
    def outdir(self):
        """Получить директорию с выходными картинками"""
        return self.__outdir

    @outdir.setter
    def outdir(self, value):
        value = os.path.normpath(value.strip())
        if value == ".":
            # print("Путь не введён!")
            msgbox.showerror("Ошибка!", "Путь не введён!")
            self.__outdir = ""
        elif not os.path.isabs(value):
            # print("Путь должен быть абсолютным!")
            msgbox.showerror("Ошибка!", "Путь должен быть абсолютным!")
            self.__outdir = ""
        else:
            if not os.path.exists(value):
                os.mkdir(value)
                # print("Created! " + value)
                msgbox.showinfo("Ошибка!", "Created! " + value)
            self.__outdir = value

    @property
    def ftype(self):
        """получить расширение входного файла"""
        return self.__ftype

    @ftype.setter
    def ftype(self, value):
        value = value.strip().lower()
        if value in ["jpg", "png", "bmp"]:
            self.__ftype = value
        else:
            # print("Поддерживаемые расширения: jpg, png, bmp!")
            msgbox.showerror(
                "Ошибка!", "Поддерживаемые расширения: jpg, png, bmp!")
            self.__ftype = ""

    @property
    def otype(self):
        """получить расширение выходного файла"""
        return self.__otype

    @otype.setter
    def otype(self, value):
        value = value.strip().lower()
        if value in ["jpg", "png", "bmp"]:
            self.__otype = value
        else:
            # print("Поддерживаемые расширения: jpg, png, bmp!")
            msgbox.showerror(
                "Ошибка!", "Поддерживаемые расширения: jpg, png, bmp!")
            self.__otype = ""

    @property
    def size(self):
        """получить размеры выходной картинки"""
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    def get_outfile(self, infile: str) -> str:
        """Из имени входного файла делает
        имя выходного файла, прибавляя суффикс"""
        file = os.path.splitext(os.path.basename(infile))[0]
        return os.path.join(self.__outdir, file + self.__suffix + "." + self.__otype)

    def clear_outdir(self) -> None:
        """Очищает от файлов выбранного типа outdir"""
        if self.__outdir != "":
            for infile in glob.glob(self.__outdir + "\\*." + self.__otype):
                os.remove(infile)
            # print("Cleared! " + self.__outdir)
            msgbox.showinfo("Ошибка!", "Cleared! " + self.__outdir)


if __name__ == "__main__":
    pass
