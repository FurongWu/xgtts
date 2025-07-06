# XG-TTS 阿里云语音合成工具

一个基于阿里云语音合成服务的桌面应用程序，提供简单易用的文本转语音功能。

## 📋 项目简介

XG-TTS 是一个使用 Python 和 Tkinter 开发的桌面应用程序，集成了阿里云语音合成服务。用户可以通过图形界面轻松地将文本转换为语音文件，支持多种音色、格式和参数调节。

## ✨ 主要功能

- 🎤 **文本转语音**: 支持中文文本转语音合成
- 📁 **文件导入**: 支持加载 TXT 文本文件进行批量处理
- 🎛️ **参数调节**: 可调节音量、语速、语调等参数
- 🎨 **多种音色**: 支持多种阿里云音色选择
- 📊 **格式支持**: 支持 PCM、WAV、MP3 等多种音频格式
- 🔧 **配置管理**: 图形化配置界面，支持保存和加载配置
- 📏 **字符限制**: 自动限制文本长度（默认600字符）
- 🌐 **多服务器**: 支持上海、北京、深圳等多个服务器节点

## 🛠️ 技术栈

- **Python 3.x**: 主要开发语言
- **Tkinter**: GUI 界面框架
- **阿里云 SDK**: 语音合成服务
- **WebSocket**: 实时通信协议
- **chardet**: 字符编码检测

## 📦 安装说明

### 环境要求

- Python 3.7 或更高版本
- Windows 操作系统（主要支持）

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone <repository-url>
   cd nls300v3
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **安装阿里云 SDK**
   ```bash
   pip install aliyun-python-sdk-core==2.15.1
   pip install chardet
   ```

## 🚀 使用方法

### 1. 配置参数

首次使用需要配置阿里云服务参数：

1. 点击"填写配置参数"按钮
2. 填写以下必要信息：
   - **ak_id**: 阿里云 AccessKey ID
   - **sk_id**: 阿里云 AccessKey Secret
   - **appkey**: 语音服务应用密钥
   - **音色**: 选择语音音色（如 xiaoyun）
   - **音频格式**: 选择输出格式（pcm/wav/mp3）
   - **采样率**: 选择音频采样率
   - **音量/语速/语调**: 调节语音参数
   - **保存路径**: 设置音频文件保存目录
   - **服务器**: 选择就近的服务器节点

### 2. 文本转语音

1. **直接输入文本**：在文本框中输入要转换的文本
2. **加载文件**：点击"加载文本文件"选择 TXT 文件
3. **开始合成**：点击"开始合成语音"按钮
4. **查看结果**：合成完成后会在状态栏显示文件路径

### 3. 其他功能

- **打开音频目录**：快速打开音频文件保存目录
- **清空文本内容**：清空当前输入的文本
- **字符计数**：实时显示文本字符数量

## 📁 项目结构

```
nls300v3/
├── aliyunttsv3.py      # 主程序文件
├── config_mg.py        # 配置管理模块
├── tts_sdk.py          # 语音合成SDK封装
├── tools.py            # 工具函数
├── nls300_config.ini   # 配置文件
├── requirements.txt    # 依赖包列表
├── setup.py           # 安装脚本
├── nls/               # 阿里云NLS SDK
├── tests/             # 测试文件
├── docs/              # 文档
└── out/               # 输出目录
```

## ⚙️ 配置说明

### 配置文件位置

- **开发环境**: 项目根目录下的 `nls300_config.ini`
- **打包环境**: `%APPDATA%/AliyunTTS/nls300_config.ini`

### 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ak_id | 阿里云 AccessKey ID | - |
| sk_id | 阿里云 AccessKey Secret | - |
| appkey | 语音服务应用密钥 | - |
| voice | 音色选择 | xiaoyun |
| format | 音频格式 | mp3 |
| sample_rate | 采样率 | 16000 |
| volume | 音量 (0-100) | 50 |
| speed | 语速 (-500到500) | 0 |
| pitch | 语调 (-500到500) | 0 |
| path | 保存路径 | ./out |
| server | 服务器地址 | nls-gateway-cn-shenzhen.aliyuncs.com |

## 🔧 打包部署

### 使用 PyInstaller 打包

```bash
# 基本打包命令
pyinstaller --noconsole --paths "venv\Lib\site-packages" --hidden-import nls -F aliyunttsv3.py

# 包含图标的打包
pyinstaller --noconsole --paths "venv\Lib\site-packages" --hidden-import nls --icon=MPIS-TTS.ico -F aliyunttsv3.py
```

### 打包注意事项

1. 确保虚拟环境中已安装所有依赖
2. 使用 `--hidden-import nls` 确保 NLS SDK 被正确包含
3. 打包后的程序会自动在用户目录创建配置文件

## 🐛 常见问题

### Q: 如何获取阿里云语音服务参数？
A: 需要在阿里云控制台开通语音服务，获取 AccessKey、Secret 和 AppKey。

### Q: 支持哪些音频格式？
A: 支持 PCM、WAV、MP3 格式，推荐使用 MP3 格式。

### Q: 文本长度有限制吗？
A: 默认限制为 600 字符，超过会自动截取。

### Q: 如何更换音色？
A: 在配置界面中选择不同的音色参数，如 xiaoyun、ailun 等。

## 📄 许可证

本项目基于 Apache License 2.0 开源协议。

## 👨‍💻 开发者

- **作者**: 西瓜
- **联系方式**: 微信：aliyuntts
- **项目地址**: [GitHub Repository]

## 🙏 致谢

- 阿里云语音合成服务
- Python Tkinter 社区
- 所有贡献者和用户

---

**注意**: 使用前请确保已正确配置阿里云语音服务参数，详细配置说明请参考：[配置参数填写介绍](https://blog.rongtech.top/archives/1745936143532)
