# -- coding:utf-8 --

import nls

# 以下代码会根据上述TEXT文本反复进行语音合成
class AliyunTts:
    def __init__(self,appkey,url,token, test_file, voice="ailun", format="mp3",
                 sample_rate=16000, volume=50, speech_rate=0, pitch_rate=0):
        # 移除线程相关初始化
        self.appkey = appkey
        self.url = 'wss://'+url+'/ws/v1'
        self.token = token
        self.__test_file = test_file
        self.voice = voice
        self.format = format
        self.sample_rate = sample_rate
        self.volume = volume
        self.speech_rate = speech_rate
        self.pitch_rate = pitch_rate

    def start(self, text):
        """同步执行语音合成"""
        self.__text = text
        self.__f = open(self.__test_file, "wb")

        # 直接调用执行方法
        self.__run_tts()

    # 保留原有回调方法（日志输出部分未修改）
    def test_on_metainfo(self, message, *args):
        print("on_metainfo message=>{}".format(message))

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))

    def __run_tts(self):  # 原__test_run重命名
        print("tts task start..")
        tts = nls.NlsSpeechSynthesizer(
            url=self.url,
            token=self.token,
            appkey=self.appkey,
            on_metainfo=self.test_on_metainfo,
            on_data=self.test_on_data,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
            callback_args=[None]
        )
        print("session start")
        r = tts.start(self.__text, self.voice, self.format,
                      self.sample_rate, self.volume,
                      self.speech_rate, self.pitch_rate)
        print("tts done with result:{}".format(r))

