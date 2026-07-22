import asyncio, os, subprocess, tempfile
import edge_tts, imageio_ffmpeg

VOICE="zh-CN-XiaoxiaoNeural"
RATE="+25%"
segments=[
    (0.35,"Nexa Module，让设备理解自然语言。"),
    (5.05,"工业、楼宇、农业和移动终端，都能用自然语言发起任务。"),
    (11.05,"本地文字、串口、语音和远程控制，统一进入设备 Agent。"),
    (17.05,"设备携带自然语言、状态和 Skills，通过加密连接请求 AI 意图服务器。"),
    (24.05,"AI 返回 Skill 计划。设备校验执行，并向应用服务器回传结果。"),
    (30.05,"提供全连接版和纯四 G 版，适配不同网络环境。"),
    (34.85,"固定 IPv6、心跳重连和失联告警，让设备持续在线。"),
    (39.35,"Nexa Module，自然语言驱动设备。"),
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
    cmd=[ff,"-y",*inputs,"-filter_complex",";".join(filters),"-map","0:v:0","-map","[outa]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-t","42","-movflags","+faststart",temp]
    subprocess.check_call(cmd)
    os.replace(temp,"nexa-module-intro.mp4")
print("Chinese voice-over added to nexa-module-intro.mp4")
