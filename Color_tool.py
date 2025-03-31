import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk,ImageGrab
import pyautogui
from tkinter import Menu
import webbrowser



class Color_tool:
    def __init__(self):
        try:
            #创建全局变量存储图像引用
            self.global_label = None  # 用于存储当前显示的标签
            self.global_photo = None  # 用于保持对PhotoImage的引用
            self.rgb_color = None
            self.id=None
            self.flog_id=0
            self.color_list = [0, 0, 0]
            self.on_exe = None
            self.x=self.y=0
            y = x = 0
            self.flog = 0
            self.root = tk.Tk()
            self.root.title('Color_tool')
            self.root.geometry('530x400')
            self.rgb_label = tk.Label(self.root,
                                      text=f'R:{self.color_list[0]}   G:{self.color_list[1]}   B:{self.color_list[2]}',
                                      font=('微软雅黑', 16))
            self.rgb_label.place(relx=0, rely=0.76)
            self.rgb_label_sixth = tk.Label(self.root, text=f'{self.change_rgb(self.color_list)}', font=('微软雅黑', 16))
            self.rgb_label_sixth.place(relx=0, rely=0.87)
            self.mouse_label = tk.Label(self.root, width=10, text=f'({x},{y})', font=('Helvetica', 16))
            self.mouse_label.place(relx=0.64, rely=0.76)
            self.mouse_place()

            self.global_label = ttk.Label(self.root, image=self.global_photo)
            self.global_label.pack()

            about_button = tk.Button(self.root, width=8, text='关于', command=self.about_this, bd=4,
                                     font=('微软雅黑', 10, 'bold'))
            about_button.place(relx=0.71, rely=0.87)
            self.mouse_event(about_button)

            self.root.bind('<Control-a>', self.get_color)
            self.root.bind('<Control-c>', self.copy_all)
            self.root.bind('<Control-x>', self.copy_rgb)
            self.root.bind('<Control-z>', self.copy_sixth)
            self.root.bind('<Control-b>',self.updating_label)

            top = Menu(self.root)  # 父容器（top）为根窗体的实例
            menuFile = Menu(top)  # 建立一个下拉菜单menuFile
            top.add_cascade(label="帮助", menu=menuFile)
            menuFile.add_command(label="复制", accelerator='Ctrl+C', command=lambda: self.copy_all(event=None))
            menuFile.add_command(label="复制RGB", accelerator='Ctrl+X', command=lambda: self.copy_rgb(event=None))
            menuFile.add_command(label="复制十六进制值", accelerator='Ctrl+Z', command=lambda: self.copy_sixth(event=None))
            menuFile.add_command(label='选择鼠标当前颜色', accelerator='Ctrl+A', command=lambda: self.get_color(event=None))
            menuFile.add_command(label='实时刷新',accelerator='Ctrl+B',command=lambda : self.updating_label(event=None))
            menuFile.add_separator()  # 分割线
            menuFile.add_command(label="退出", command=self.root.destroy)

            self.root.config(menu=top)  # 如果缺失此句，则不会显示菜单分组
            self.root.attributes('-topmost', True)

            self.root.resizable(False, False)
            self.root.mainloop()
        except:
            pass

    def updating(self,event):
        if self.flog_id == 1:
            self.global_label.after_cancel(self.id)
            self.id=None
            self.flog_id=0
            pass
        else:
            x, y = pyautogui.position()
            img = ImageGrab.grab()
            r, g, b = map(int, img.getpixel((x, y)))  # 抓取屏幕截图,rgb更准确
            self.color_list = [r, g, b]
            rgb_color = (r, g, b)
            # 创建新图像
            color_image = Image.new('RGB', (520, 300), rgb_color)
            # 转换图像格式
            self.global_photo = ImageTk.PhotoImage(color_image)

            self.global_label.config(image=self.global_photo)

            self.rgb_label.config(text=f'R:{self.color_list[0]}   G:{self.color_list[1]}   B:{self.color_list[2]}')
            self.rgb_label_sixth.config(text=f'{self.change_rgb(self.color_list).upper()}')
            self.id=self.global_label.after(2,self.updating,event)
            self.root.update()
    def updating_label(self,event):
        if self.id:
            self.flog_id=1
        else:
            self.updating(event)
    #清空粘贴板，写入复制内容
    def copy_all(self,event):
        self.root.clipboard_clear()
        self.root.clipboard_append(f'{self.color_list}  {self.change_rgb(self.color_list).upper()}')
        pass
    def copy_rgb(self,event):
        self.root.clipboard_clear()
        self.root.clipboard_append(f'{self.color_list}')
        pass
    def copy_sixth(self,event):
        self.root.clipboard_clear()
        self.root.clipboard_append(f'{self.change_rgb(self.color_list).upper()}')
        pass
    #显示鼠标坐标，随时刷新
    def mouse_place(self):
        x, y = pyautogui.position()
        self.mouse_label.config(text=f'({x},{y})')
        self.mouse_label.after(1, self.mouse_place)

    #将RGB值转换为十六进制值
    def change_rgb(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    #获取鼠标当前位置的颜色
    def get_color(self, event):
        if self.id:
            self.global_label.after_cancel(self.id)
            self.id=0
        # 获取鼠标位置和颜色
        x, y = pyautogui.position()
        img = ImageGrab.grab()
        r, g, b = map(int, img.getpixel((x, y)))  #抓取屏幕截图,rgb更准确
        self.color_list = [r, g, b]
        rgb_color = (r, g, b)
        #以下为最初的方法一
        #img = pyautogui.screenshot()    #获取屏幕截图，是pillow的image对象，未知原因rgb色值抓取不准确
        #pixel_color = img.getpixel((x, y))    #获取当前RGB值

        # 创建新图像
        color_image = Image.new('RGB', (520, 300), rgb_color)

        # 转换图像格式
        self.global_photo = ImageTk.PhotoImage(color_image)  # 保持全局引用，否则图片显示不出来


        self.global_label.config(image=self.global_photo)

        self.rgb_label.config(text=f'R:{self.color_list[0]}   G:{self.color_list[1]}   B:{self.color_list[2]}')
        self.rgb_label_sixth.config(text=f'{self.change_rgb(self.color_list).upper()}')
        self.root.update()

    #关于窗口
    def about_this(self):
        win = tk.Toplevel()
        win.attributes('-topmost', 1)

        win.title('关于')
        win.geometry('360x360')
        writer = tk.Label(win, text='作者\n子轩大魔王', font=('微软雅黑', 16, 'bold'))
        writer.pack()
        web_button = tk.Button(win, text='打开他的哔哩哔哩空间', font=('微软雅黑', 10, 'bold'), bd=6,
                               command=lambda: webbrowser.open('https://space.bilibili.com/413055811'))
        web_button.pack()
        self.mouse_event(web_button)
        lb1 = tk.Label(win, text='遇见喜欢的颜色', font=('方正舒体', 22, 'bold'))
        lb1.place(relx=0.06, rely=0.52)
        lb2 = tk.Label(win, text='一键           它！', font=('方正舒体', 22, 'bold'))
        lb2.place(relx=0.12, rely=0.8)
        lb3 = tk.Label(win, text='Get', font=('方正舒体', 36, 'bold'), fg='red')
        lb3.place(relx=0.39, rely=0.732)

        win.resizable(False, False)
        win.mainloop()

    #按钮动画
    class mouse_event:
        def __init__(self, button):
            self.button = button
            self.button.bind('<Enter>', self.enter)
            self.button.bind('<Leave>', self.leave)
            pass

        def enter(self, event):
            self.button.config(bg='lightgray', font=('微软雅黑', 10, 'bold'))

        def leave(self, event):
            self.button.config(bg='SystemButtonFace', font=('微软雅黑', 10, 'bold'))

Color_tool()














