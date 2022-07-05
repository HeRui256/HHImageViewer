# -*- coding = utf-8 -*-
"""
由个人开发者开发的图片查看器 《HH查图器》 （英文名HHImageViewer）
使用Python编写，调用tkinter库实现图形化界面，调用PIL以加载图像
调用库：base64，os，PIL，tkinter，zlib
单文件脚本，不需要额外的文件
>>使用说明
将图片和此文件放在同一个文件夹，运行本文件以查看图片
如果同时存在多个图片，按↑或←以切换上一张图片，按↓或→切换下一张图片（文件顺序按文件名排序文件）
调整图片大小时，需要调整窗口的横向宽度，调整宽度后，再点击图片一下就可以调整图片，（也可以按快捷键Shift或Ctrl或Alt或Backapace或Enter或空格）
>>稳定支持的格式（经测试，能正常打开）
png，jpg，gif，bmp，jpeg，tga
>>理论上支持的格式（没测试过，本人没见过这些格式，不知道行不行，但下列格式PIL库都支持，那理论上都可以）
blp，bufr，cur，dcx，dds，grib，ico，im，jfif，jpe，jpx，jpf，apng，psd，rgb，tif，tiff，webp，xpm，xbm
>>编写完成于2022年7月4日，中国江西
>>制作人员名单
程序：何睿
图标：张肥肥（网名）
美术设计：张肥肥（网名）
"""
import base64
import os
import tkinter as tk
import zlib

from PIL import Image as PIL_Image, ImageTk

def ico_unzip():
    """将字符解压成一个ico图标并返回，用给ImageTk.PhotoImage的data形参调用"""
    ico = zlib.decompress(zlib.decompress(b'x\x9c\xab\x98\xf3\xf6\xa46_K\x80\x88\xcbA\xd5\x8dL.\x9fy-\xde\xe40\x182y'
                                          b'\xde\xb0\xb5\xd9p\xc2pr\x88\xea\xf7-;<g-9\x9f\x1e\x13T\xe6\xb5;7\xdb(f'
                                          b'\xfa\xb6%?\xe3N\x06\x16\xfd\x97?\xbd\xe7yl8#\x03\xc9\xe0\xc0~.\x86\x03\xfeW'
                                          b'\xber\x06\xab\x94\xeb\x03\x00\x98\x1e$j'))  # 经过两次解压，为一个未解码的ico文件
    icon = base64.b64decode(ico)    # 解码后为一个纯白色ico图标作为窗口左上角图标
    return icon


def hh_image_viewer():
    """窗口和当前展示图片的图片的参数"""
    image_list = []      # 所有图片文件名列表
    image_number = 0     # 正在播放的图像的编号（从0开始）
    image_size = tuple()      # 正在播放的图像的大小（像素）
    image_data = None    # 正在播放的图像的数据（二进制）
    screen_size = []     # 屏幕大小
    window_size = []     # 窗口大小（原先的窗口大小）

    window = tk.Tk()
    window.attributes("-alpha", 1)
    window.title("")
    window.geometry("1080x720+420+180")
    window["background"] = "#FFFFFF"
    window = window
    icon_image = ImageTk.PhotoImage(data=ico_unzip())    # GUI左上角的图标
    window.tk.call("wm", "iconphoto", window, icon_image)
    window.wm_attributes('-topmost',1)

    screen_size.append(window.winfo_screenwidth())   # 屏幕宽度
    screen_size.append(window.winfo_screenheight())  # 屏幕长度          （屏幕分辨率）

    def set_image_list():
        """（初始化文件名列表）将当前工作目录下的图像的文件名添加到self.file_name_list（带后缀）"""
        suffix_list = ["png", "jpg", "gif", "bmp", "jpeg", "tga", "blp", "bufr", "cur", "dcx", "dds", "grib", "ico",
                       "im", "jfif", "jpe", "jpx", "jpf", "apng", "psd", "rgb", "tif", "tiff", "webp", "xpm", "xbm"]
        # 此程序引用的PIL库支持的图片后缀名
        path = os.getcwd()
        file_folder_list = os.listdir(path)  # 同目录下的所有文件和文件夹名
        file_list = [i for i in file_folder_list if os.path.isfile(f"{path}\\{i}")]  # 只有文件名，排除了文件夹
        image_list.clear()
        for i in file_list:
            if i.split(".")[-1] in suffix_list:
                image_list.append(i)
        image_list.sort()  # 设置图像名列表
        return image_list

    def turn_window():
        """调节窗口，使用image_size和screen_size变量使窗口居中放置，不需要传参"""
        left_x = int((screen_size[0] - window_size[0]) / 2)
        top_y = int((screen_size[1] - window_size[1]) / 2)
        window.geometry(f"{window_size[0]}x{window_size[1]}+{left_x}+{top_y }")

    def turn_image(add=0):
        """切换图片，可传入切换上一张还是下一张，+1为切换下一张，-1为切换上一张，默认为0不切换"""
        nonlocal image_number, image_data, image_size, window_size
        image_number += add
        file_name = image_list[int((image_number + len(image_list)) % len(image_list))]
        if os.path.isfile(file_name) is False:                       # 检查文件是否存在，防止不存在文件报错崩溃
            set_image_list()
            file_name = image_list[int((image_number + len(image_list)) % len(image_list))]
        print(file_name)
        image_data = image = PIL_Image.open(file_name)
        image_size = image.size
        result_size = ()

        def turn_size(_width, _height):    # 递归，找到使图片不超过屏幕的边缘的合适大小
            nonlocal result_size
            if _width <= screen_size[0] and _height <= screen_size[1]:
                result_size = (int(_width), int(_height))
            else:
                turn_size(_width/2, _height/2)

        turn_size(*image_size)
        window_size = list(result_size)
        image_data_small = ImageTk.PhotoImage(image.resize(result_size))
        turn_window()
        return image_data_small

    def set_image():
        """根据窗口宽度调节图片大小（同宽），给resize()使用"""
        nonlocal image_data, image_label
        width = window.winfo_width()    # 图片与窗口同宽
        height = int(width * image_size[1] / image_size[0])    # 根据原图按比例求出高度
        image = ImageTk.PhotoImage(image_data.resize((width, height)))
        image_label.configure(image=image)
        window.mainloop()

    def resize(event=None):
        """根据窗口拖动调节窗口长宽比和图片大小"""
        if image_list:
            if window.winfo_width() / window.winfo_height() != image_size[0] / image_size[1]:
                window.geometry(f"{window.winfo_width()}x{int(window.winfo_width() * image_size[1] / image_size[0])}"
                                f"+{window.winfo_x()}+{window.winfo_y()}")
            set_image()

    def turn(add):
        """为下面turn_last和turn_next所调用"""
        nonlocal image_number
        try:
            image = turn_image(add)
            image_label.configure(image=image)
            window.mainloop()
        except:
            image_number += add

    def turn_last(event):
        """切换到上一张照片"""
        if image_list:        # 从之前的列表检查是否有文件，如果不存在就不执行，怕报错崩溃（只使用内存）
            turn(-1)
        else:
            if set_image_list():  # 从外存再次检查是否有文件
                turn(-1)

    def turn_next(event):
        """切换到下一张照片"""
        if image_list:        # 从之前的列表检查是否有文件，如果不存在就不执行，怕报错崩溃（只使用内存）
            turn(1)
        else:
            if set_image_list():  # 从外存再次检查是否有文件
                turn(1)

    def window_quit(event):
        """结束程序"""
        window.destroy()

    if set_image_list():  # 如果有当前目录有图片
        image_label_data = turn_image()
        image_label = tk.Label(window, image=image_label_data, bg="#FFFFFF", bd=0)
        image_label.place(x=0, y=0)

    window.bind("<ButtonPress-1>", resize)    # 调节窗口比例
    window.bind("<Shift_L>", resize)
    window.bind("<Shift_R>", resize)
    window.bind("<Return> ", resize)
    window.bind("<Alt_L>", resize)
    window.bind("<Alt_R>", resize)
    window.bind("<Control_L>", resize)
    window.bind("<Control_R>", resize)
    window.bind("<space>", resize)
    window.bind("<BackSpace>", resize)

    window.bind("<Escape>", window_quit)      # 退出

    window.bind("<Left>", turn_last)        # 切换到上一张
    window.bind("<Up> ", turn_last)
    window.bind("<Right>", turn_next)       # 切换到下一张
    window.bind("<Down>", turn_next)

    window.mainloop()


hh_image_viewer()
