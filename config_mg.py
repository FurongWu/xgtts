# -- coding:utf-8 --
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser
import os
from tools import resource_path




class ConfigWindow:
    def __init__(self, parent):
        self.parent = parent  # parent现在为MainApp实例
        self.window = tk.Toplevel(parent.window)
        self.window.title("初始化配置")
        self.window.geometry("490x380+%d+%d" % (
            (self.window.winfo_screenwidth() - 490) // 2,
            (self.window.winfo_screenheight() - 380) // 2
        ))
        self.window.resizable(False, False)  # 禁用窗口缩放
        # 模态对话框设置
        self.window.grab_set()
        self.window.transient(parent.window)

        # # 关闭事件处理
        # self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.load_config()
        # 添加窗口关闭协议
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """窗口关闭时的清理操作"""
        self.parent.config_window = None  # 关键修复点
        self.window.destroy()

    def create_widgets(self):
        # 配置项
        labels = [
            ('ak_id:', 0), ('sk_id:', 1), ('appkey:', 2), ('音色:', 3),
            ('音频编码格式:', 4), ('音频采样率:', 5), ('音量:', 6),
            ('语速:', 7), ('语调:', 8), ('合成音频保存路径:', 9), ('服务器网关:', 10),
        ]

        # 创建标签
        for text, row in labels:
            ttk.Label(self.window, text=text).grid(
                row=row, column=0, padx=10, pady=5, sticky='w')

        # 输入控件
        self.ak_id = ttk.Entry(self.window, width=35)
        self.sk_id = ttk.Entry(self.window, show='*')
        self.appkey = ttk.Entry(self.window)
        self.voice = ttk.Entry(self.window)

        self.format = ttk.Combobox(self.window, values=['pcm', 'wav', 'mp3'], state='readonly')
        self.sample_rate = ttk.Combobox(self.window,
                                        values=['16000', '8000', '24000'],
                                        state='readonly')

        # 修改点1：将Scale改为Spinbox
        self.volume = ttk.Spinbox(self.window, from_=0, to=100)
        self.speed = ttk.Spinbox(self.window, from_=-500, to=500)
        self.pitch = ttk.Spinbox(self.window, from_=-500, to=500)
        self.path = ttk.Entry(self.window)
        self.path_btn = ttk.Button(self.window, text="浏览", command=self.select_path)
        # 上海：nls-gateway-cn-shanghai.aliyuncs.com
        # 北京：nls-gateway-cn-beijing.aliyuncs.com
        # 深圳：nls-gateway-cn-shenzhen.aliyuncs.com
        self.server = ttk.Combobox(self.window, values=['nls-gateway-cn-shanghai.aliyuncs.com',
                                                        'nls-gateway-cn-beijing.aliyuncs.com',
                                                        'nls-gateway-cn-shenzhen.aliyuncs.com'], state='readonly')

        # 布局
        entries = [
            self.ak_id, self.sk_id, self.appkey, self.voice,
            self.format, self.sample_rate, self.volume,
            self.speed, self.pitch, self.path, self.server
        ]

        for row, widget in enumerate(entries):
            widget.grid(row=row, column=1, padx=10, pady=5, sticky='ew')

        self.path_btn.grid(row=9, column=2, padx=5)

        # 保存按钮
        ttk.Button(self.window, text="保存配置", command=self.save_config).grid(
            row=10, column=2, padx=5, sticky='e')

    def load_config(self):
        """修改点2：每次打开都重新读取配置文件"""
        self.config = configparser.ConfigParser()
        # resource_path()
        if os.path.exists(resource_path()):
            self.config.read(resource_path(), encoding='utf-8')
        else:
            self.config['DEFAULT'] = {}

        defaults = self.config['DEFAULT']

        # 清空原有内容
        for entry in [self.ak_id, self.sk_id, self.appkey, self.voice, self.path]:
            entry.delete(0, tk.END)

        # 设置新值
        self.ak_id.insert(0, defaults.get('ak_id', ''))
        self.sk_id.insert(0, defaults.get('sk_id', ''))
        self.appkey.insert(0, defaults.get('appkey', ''))
        self.voice.insert(0, defaults.get('voice', 'xiaoyun'))
        self.format.set(defaults.get('format', 'mp3'))
        self.sample_rate.set(defaults.get('sample_rate', '16000'))
        self.server.set(defaults.get('server', 'nls-gateway-cn-shenzhen.aliyuncs.com'))
        # 修改点3：设置Spinbox的值
        self.volume.delete(0, 'end')
        self.volume.insert(0, defaults.get('volume', '50'))
        self.speed.delete(0, 'end')
        self.speed.insert(0, defaults.get('speed', '0'))
        self.pitch.delete(0, 'end')
        self.pitch.insert(0, defaults.get('pitch', '0'))
        self.path.insert(0, defaults.get('path', os.path.join(os.getcwd(), 'out')))

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path.delete(0, tk.END)
            self.path.insert(0, path)

    def save_config(self):
        # 修改点4：获取Spinbox的值
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'ak_id': self.ak_id.get(),
            'sk_id': self.sk_id.get(),
            'appkey': self.appkey.get(),
            'voice': self.voice.get(),
            'format': self.format.get(),
            'sample_rate': self.sample_rate.get(),
            'volume': self.volume.get(),  # 直接获取Spinbox的值
            'speed': self.speed.get(),
            'pitch': self.pitch.get(),
            'path': self.path.get(),
            'server': self.server.get()
        }
        # resource_path()
        with open(resource_path(), 'w', encoding='utf-8') as f:
            config.write(f)

        messagebox.showinfo("提示", "配置保存成功！")
        self.window.destroy()