import gradio as gr
import edge_tts
import asyncio
import os
# https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
SUPPORTED_VOICES = {
    'Xiaoxiao-小小-女性': 'zh-CN-XiaoxiaoNeural',
    'Xiaoyi-小艺-女性': 'zh-CN-XiaoyiNeural',
    'Yunjian-云剑-男性': 'zh-CN-YunjianNeural',
    'Yunxi-云西-男性': 'zh-CN-YunxiNeural',
    'Yunxia-云夏-男性': 'zh-CN-YunxiaNeural',
    'Yunyang-云阳-男性': 'zh-CN-YunyangNeural',
    'liaoning-Xiaobei-小北-辽宁-女性': 'zh-CN-liaoning-XiaobeiNeural',
    'shaanxi-Xiaoni-小妮-陕西-女性': 'zh-CN-shaanxi-XiaoniNeural',
    'HK-HiuGaai-慧开-粤语-女性': 'zh-HK-HiuGaaiNeural',
    'HK-HiuMaan-慧漫-粤语-女性': 'zh-HK-HiuMaanNeural',
    'HK-WanLung-王伦-粤语-男性': 'zh-HK-WanLungNeural',
    'TW-HsiaoChen-何小辰-台湾-女性': 'zh-TW-HsiaoChenNeural',
    'TW-YunJhe-云杰-台湾-男性': 'zh-TW-YunJheNeural',
    'TW-HsiaoYu-何小云-台湾-女性': 'zh-TW-HsiaoYuNeural',
    'US-Ava-艾娃-多语种-女性': 'en-US-AvaMultilingualNeural',
    'US-Andrew-安德鲁-多语种-男性': 'en-US-AndrewMultilingualNeural',
    'US-Emma-艾玛-多语种-女性': 'en-US-EmmaMultilingualNeural',
    'US-Brian-布莱恩-多语种-男性': 'en-US-BrianMultilingualNeural',
}

# 发音切换
def changeVoice(voices):
    example = SUPPORTED_VOICES[voices]
    example_file = os.path.join(os.path.dirname(__file__), "example/"+example+".wav")
    return example_file

# 文本转语音
async def textToSpeech(text, voices, rate, volume):
    output_file = "output.mp3"
    voices = SUPPORTED_VOICES[voices]
    if (rate >= 0):
        rates = rate = "+" + str(rate) + "%"
    else:
        rates = str(rate) + "%"
    if (volume >= 0):
        volumes = "+" + str(volume) + "%"
    else:
        volumes = str(volume) + "%"
    communicate = edge_tts.Communicate(text,
                                       voices,
                                       rate=rates,
                                       volume=volumes,
                                       proxy=None)
    await communicate.save(output_file)
    audio_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(audio_file)):
        return audio_file
    else:
        raise gr.Error("生成错误！")
        return FileNotFoundError


# 清除转换结果
def clearSpeech():
    output_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(output_file)):
        os.remove(output_file)
    return None, None


with gr.Blocks(css="style.css", title="文本生成语音") as demo:
    gr.Markdown("""
    # 微软TTS文本生成语音助手
      战略信息部  如需增加语音种类联系 963963 林隽
    """)
    with gr.Row():
        with gr.Column():
            text = gr.TextArea(label="文本", elem_classes="text-area")
            btn = gr.Button("生成", elem_id="submit-btn")
        with gr.Column():
            voices = gr.Dropdown(choices=[
                "Xiaoxiao-小小-女性", "Xiaoyi-小艺-女性", "Yunjian-云剑-男性", "Yunxi-云西-男性",
                "Yunxia-云夏-男性", "Yunyang-云阳-男性", "liaoning-Xiaobei-小北-辽宁-女性",
                "shaanxi-Xiaoni-小妮-陕西-女性","HK-HiuGaai-慧开-粤语-女性","HK-HiuMaan-慧漫-粤语-女性",
                "HK-WanLung-王伦-粤语-男性","TW-HsiaoChen-何小辰-台湾-女性","TW-YunJhe-云杰-台湾-男性",
                "TW-HsiaoYu-何小云-台湾-女性","US-Ava-艾娃-多语种-女性","US-Andrew-安德鲁-多语种-男性",
                "US-Emma-艾玛-多语种-女性","US-Brian-布莱恩-多语种-男性"
            ],
                                 value="Xiaoxiao-小小-女性",
                                 label="音色",
                                 info="请选择发音人",
                                 interactive=True)
            
          #  example = gr.Audio(label="试听",
           #                   value="example/zh-CN-XiaoxiaoNeural.wav",
            #                  interactive=True,
             #                 elem_classes="example")

           # voices.change(fn=changeVoice,inputs=voices,outputs=example)
            voices.change(fn=changeVoice,inputs=voices)
            rate = gr.Slider(-100,
                             100,
                             step=1,
                             value=0,
                             label="语速调整",
                             info="加快或减慢语速",
                             interactive=True)
            
            volume = gr.Slider(-100,
                               100,
                               step=1,
                               value=0,
                               label="音量调整",
                               info="加大或减小音量",
                               interactive=True)
            audio = gr.Audio(label="生成",
                             interactive=False,
                             elem_classes="audio",
)
            clear = gr.Button("清除", elem_id="clear-btn")
            btn.click(fn=textToSpeech,
                      inputs=[text, voices, rate, volume],
                      outputs=[audio])
            clear.click(fn=clearSpeech, outputs=[text, audio])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0",server_port=7870,share=False)
