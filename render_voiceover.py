import asyncio, os, subprocess, tempfile
import edge_tts, imageio_ffmpeg

VOICE="zh-CN-XiaoxiaoNeural"
RATE="+25%"
segments=[
    (0.40,"Nexa Module。让设备理解意图，让能力直接发生。"),
    (6.10,"工业、楼宇、农业和移动终端，都能用自然语言发起任务。"),
    (13.10,"本地文字、串口、语音和远程控制，在设备端统一为自然语言。"),
    (19.10,"设备携带自然语言、状态和 Skills，通过 TCP 加 TLS 请求 AI 意图服务器。"),
    (26.10,"AI 完成意图识别与 Skill 匹配。设备校验计划，并在本地可信执行。"),
    (33.10,"执行结果通过固定 IPv6 直达应用服务器，不经过传统 IoT 业务中转节点。"),
    (39.10,"全连接版与纯四 G 版，共享心跳重连、离线缓存和失联告警。"),
    (44.10,"Nexa Module。自然语言进入，设备能力发生。"),
]
async def generate(folder):
    files=[]
    for i,(_,line) in enumerate(segments):
        path=os.path.join(folder,f"voice-{i}.mp3")
        await edge_tts.Communicate(line,VOICE,rate=RATE,volume="+5%").save(path)
        files.append(path)
    return files

with tempfile.TemporaryDirectory(prefix="nexa-voice-") as folder:
    files=asyncio.run(generate(folder))
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    inputs=["-i","nexa-module-intro.mp4"]
    for path in files: inputs += ["-i",path]
    filters=[]
    mix=[]
    for i,(start,_) in enumerate(segments,1):
        delay=int(start*1000)
        filters.append(f"[{i}:a]aresample=48000,highpass=f=100,lowpass=f=6500,volume=0.88,adelay={delay}|{delay}[a{i}]")
        mix.append(f"[a{i}]")
    filters.append("".join(mix)+f"amix=inputs={len(files)}:duration=longest:dropout_transition=0:normalize=0,alimiter=limit=0.78:attack=8:release=80[outa]")
    temp="nexa-module-voiced.mp4"
    cmd=[ff,"-y",*inputs,"-filter_complex",";".join(filters),"-map","0:v:0","-map","[outa]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-t","48","-movflags","+faststart",temp]
    subprocess.check_call(cmd)
    os.replace(temp,"nexa-module-intro.mp4")
print("Chinese voice-over added to nexa-module-intro.mp4")
