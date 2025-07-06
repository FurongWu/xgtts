# -- coding:utf-8 --
import os
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

# 获取配置文件路径
def resource_path(relative_path='nls300_config.ini'):
    # """获取打包后的资源绝对路径"""
    if getattr(sys, 'frozen', False):
        # 打包环境
        if sys.platform == 'win32':
            config_dir = os.path.join(os.getenv('APPDATA'), 'AliyunTTS')
        else:
            config_dir = os.path.expanduser('~/.config/AliyunTTS')
    else:
        # 开发环境使用当前目录
        config_dir = os.path.abspath(".")

    # 确保目录存在
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, relative_path)


# 处理中文编码
def auto_transcode(input_bytes, target_encoding='utf-8', source_encoding=None, errors='strict'):
    """
    自动将输入的字节数据转码为目标编码的字节数据

    参数：
    input_bytes: bytes - 输入的字节数据
    target_encoding: str - 目标编码（默认utf-8）
    source_encoding: str - 手动指定源编码（默认自动检测）
    errors: str - 错误处理方式（默认strict，可选ignore/replace等）

    返回：
    bytes - 转码后的字节数据

    示例：
    # >>> gbk_bytes = '你好'.encode('gbk')
    # >>> utf8_bytes = auto_transcode(gbk_bytes)
    # >>> print(utf8_bytes.decode('utf-8'))
    你好
    """
    # 检测第三方库依赖
    try:
        import chardet
    except ImportError:
        raise ImportError('需要chardet库支持，请使用 pip install chardet 安装')

    # 解码逻辑
    if source_encoding:
        # 使用用户指定的源编码
        try:
            text = input_bytes.decode(source_encoding, errors=errors)
        except LookupError:
            raise ValueError(f"不支持的编码格式：{source_encoding}")
    else:
        # 自动检测编码
        detection = chardet.detect(input_bytes)
        source_encoding = detection['encoding']
        confidence = detection['confidence']

        # 处理低置信度情况
        if not source_encoding or confidence < 0.5:
            raise ValueError(
                f'编码检测可信度过低（{confidence:.2f}），检测结果：{source_encoding}')

        try:
            text = input_bytes.decode(source_encoding, errors=errors)
        except UnicodeDecodeError:
            # 尝试常见中文编码回退
            for enc in ['gb18030', 'utf-8', 'big5']:
                try:
                    text = input_bytes.decode(enc, errors=errors)
                    source_encoding = enc
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise

    # 编码到目标格式
    try:
        return text.encode(target_encoding, errors=errors)
    except LookupError:
        raise ValueError(f"不支持的编码格式：{target_encoding}")


# 获取token
# pip install aliyun-python-sdk-core==2.15.1 # 安装阿里云SDK核心库
def get_token(config):
    # 创建AcsClient实例
    client = AcsClient(config.get('DEFAULT', 'ak_id'), config.get('DEFAULT', 'sk_id'), "cn-shanghai");

    # 创建request，并设置参数。
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request)
        ### print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            # expireTime = jss['Token']['ExpireTime']
        ### print("token = " + token)
        ### print("expireTime = " + str(expireTime))
    except Exception as e:
        print(e)

    return token
