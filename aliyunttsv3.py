# -- coding:utf-8 --
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser
import os
import sys
import webbrowser
import datetime
import http.client
import json
import queue
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from tools import auto_transcode, get_token,resource_path
from tts_sdk import AliyunTts
from config_mg import ConfigWindow
import nls

# pip install chardet
# pip install aliyun-python-sdk-core==2.15.1 # 安装阿里云SDK核心库

# 示例（需替换为你的实际路径）
# pyinstaller --noconsole \
# --paths "D:\python\pythonProject\nls300v3\venv\Lib\site-packages" \
# --hidden-import nls \
# -F aliyunttsv3.py

#pyinstaller --noconsole --paths "D:\python\pythonProject\nls300v3\venv\Lib\site-packages" --hidden-import nls -F aliyunttsv3.py

# 以下MainApp类保持不变
class MainApp:

    def __init__(self):
        # self.window = tk.Tk()
        self.str_text_count = 600
        self.window = tk.Tk()
        self.config_window = None  # 配置窗口引用
        self.window.title("XG-TTS for ali-python-sdk版-V0.3 by 西瓜 微信：aliyuntts")
        self.window.geometry("500x350+%d+%d" % (
            (self.window.winfo_screenwidth() - 500) // 2,
            (self.window.winfo_screenheight() - 350) // 2
        ))
        self.window.resizable(False, False)  # 禁用窗口缩放
        self.check_config()
        self.create_widgets()

    def check_config(self):
        # resource_path()
        if not os.path.exists(resource_path()):
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'path': os.path.join(os.getcwd(), 'out'),
                'volume': '50',
                'speed': '0',
                'pitch': '0',
                'voice': 'xiaoyun',
                'format': 'pcm',
                'sample_rate': '16000',
                'server': 'nls-gateway-cn-shenzhen.aliyuncs.com',
            }
            # resource_path()
            with open(resource_path(), 'w', encoding='utf-8') as f:
                config.write(f)

    def create_widgets(self):

        # 操作按钮区域
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(padx=10, pady=5, fill='x')

        ttk.Button(btn_frame, text="填写配置参数", command=self.open_config).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="加载文本文件", command=self.load_file).pack(side='left', padx=5)
        self.btn1 = ttk.Button(btn_frame, text="开始合成语音", command=self.synthesize)
        self.btn1.pack(side='left', padx=5)
        # 绑定不同事件类型
        self.btn1.bind("<Button-1>",self.clear_text2)  # 左键单击
        ttk.Button(btn_frame, text="打开音频目录", command=self.open_dir).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空文本内容", command=self.clear_text).pack(side='left', padx=5)

        # 输入区域
        input_frame = ttk.LabelFrame(self.window,
                                     text=f"输入文本或加载TXT文本文件后点击开始合成（只会生成前300字符的语音）")
        input_frame.pack(padx=10, pady=5, fill='both', expand=True)

        # 文本输入框
        self.text_input = tk.Text(input_frame, height=15, width=70)
        self.text_input.pack(padx=5, pady=5, fill='both')

        # 添加字符计数器标签（新增部分）
        counter_frame = ttk.Frame(input_frame)
        counter_frame.pack(fill='x', padx=5, pady=0)
        # 字数1
        self.char_count_label = ttk.Label(counter_frame, text=f"0/{self.str_text_count}", foreground="gray")
        self.char_count_label.pack(side='right')

        # 绑定事件（修改原有事件绑定）
        self.text_input.bind('<KeyRelease>', self.limit_text_length)

        status_frame = ttk.Frame(self.window)
        status_frame.pack(padx=10, pady=0, fill='x')
        # 添加状态显示文本框（修改部分）
        self.status_text = tk.Text(status_frame, height=2, width=70, )
        self.status_text.pack(padx=5, pady=0, fill='x', expand=True)
        # self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, f"生成的音频文件路径会显示在这里......")

        # 使用指导链接
        link_frame = ttk.Frame(self.window)
        link_frame.pack(padx=5, pady=0, fill='x')
        # 创建超链接标签
        self.link_label = tk.Label(link_frame, text="使用前需填写好相关配置参数并保存配置，点击这里可以查看配置参数填写介绍！", fg="blue", cursor="hand2", )
        # 事件绑定
        self.link_label.bind("<Button-1>", lambda e: self.open_url("https://blog.rongtech.top/archives/1745936143532"))
        self.link_label.bind("<Enter>", lambda e: self.link_label.config(fg="red"))
        self.link_label.bind("<Leave>", lambda e: self.link_label.config(fg="blue"))
        self.link_label.pack(side='left', padx=5, pady=0, fill='both')

    import webbrowser
    def open_url(self, url):
        self.webbrowser.open(url)

    def clear_text(self):
        self.text_input.delete(1.0, tk.END)
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, f"生成的音频文件路径会显示在这里......")

    def clear_text2(self,event=None):
        # self.text_input.delete(1.0, tk.END)
        # 获取当前文本内容
        content = self.text_input.get("1.0", "end-1c")
        current_count = len(content.strip())
        if current_count != 0:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"音频文件正在合成......")

    def open_dir(self):
        config = configparser.ConfigParser()
        # resource_path()
        config.read(resource_path(), encoding='utf-8')
        out_dir = config.get('DEFAULT', 'path', fallback='out')
        os.startfile(out_dir)

    def open_config(self):
        """安全打开配置窗口"""
        # 检查窗口是否存在
        if not hasattr(self, 'config_window') or \
                not self.config_window or \
                not self.config_window.window.winfo_exists():
            self.config_window = ConfigWindow(self)
        else:
            # 如果窗口已存在，提到最前并获取焦点
            self.config_window.window.lift()
            self.config_window.window.focus_set()

    # 字数限制
    def limit_text_length(self, event):
        """修改后的事件处理函数"""
        # 获取当前文本内容
        content = self.text_input.get("1.0", "end-1c")
        current_count = len(content)

        # 更新计数器显示（新增）
        self.char_count_label.config(text=f"{current_count}/{self.str_text_count}")
        self.char_count_label.config(foreground="red" if current_count > self.str_text_count else "gray")
        # 如果文本长度== 0,将音频文件路径清空
        if current_count == 0:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"生成的音频文件路径会显示在这里......")
        # 处理超限内容（修改后逻辑）
        if current_count > self.str_text_count:
            # 解除事件绑定防止递归
            self.text_input.unbind('<KeyRelease>')

            # 截断文本并设置光标
            self.text_input.delete(f"1.0+{self.str_text_count}c", "end")
            self.text_input.mark_set("insert", "end")

            # 重新绑定事件
            self.text_input.bind('<KeyRelease>', self.limit_text_length)

            # 显示警告信息（修改为{self.str_text_count}字符）
            messagebox.showwarning("提示", f"文本长度不能超过{self.str_text_count}字符,已经自动截取前{self.str_text_count}字符并显示！")

    def load_file(self):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, f"生成的音频文件路径会显示在这里......")
        filepath = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                content = auto_transcode(content)
                str_data = content.decode('utf-8')

                # 插入文本后自动触发计数更新（新增）
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, str_data)
                self.limit_text_length(None)  # 手动触发计数更新

            except Exception as e:
                messagebox.showerror("错误", f"文件读取失败：{str(e)}")

    def synthesize(self):
        text_content = self.text_input.get(1.0, "end-1c").strip()
        print('input_text：',text_content)
        if not text_content:
            messagebox.showwarning("警告", "请输入要合成的文本内容！")
            return
        try:

            config = configparser.ConfigParser()
            config.read(resource_path(), encoding='utf-8')
            output_dir = config.get('DEFAULT', 'path', fallback='out')
            os.makedirs(output_dir, exist_ok=True)

            filename = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S") + '.' + config.get('DEFAULT', 'format')
            output_path = os.path.join(output_dir, filename)

            serverhost = config.get('DEFAULT', 'server')
            appkey = config.get('DEFAULT', 'appkey')
            token = get_token(config)
            format = config.get('DEFAULT', 'format')
            sampleRate = config.get('DEFAULT', 'sample_rate')
            voice = config.get('DEFAULT', 'voice')
            volume = config.get('DEFAULT', 'volume')
            speech_rate = config.get('DEFAULT', 'speed')
            pitch_rate = config.get('DEFAULT', 'pitch')

            ats = AliyunTts(appkey, serverhost,token,output_path,voice,format,int(sampleRate),int(volume),int(speech_rate),int(pitch_rate))
            ats.start(text_content)
            self.status_text.delete(1.0, tk.END)
            # self.status_text.insert(tk.END, f"已合成文件：{output_path}")
            self.status_text.insert(tk.END, output_path)

            # 如果有异常，显示错误信息

        except Exception as e:
            messagebox.showerror("合成失败", f"错误信息：{str(e)}")


if __name__ == "__main__":
    app = MainApp()
    app.window.mainloop()