import asyncio, os, subprocess, tempfile
import edge_tts, imageio_ffmpeg

VOICE="zh-CN-XiaoxiaoNeural"
RATE="+18%"
segments=[
    (0.45,"Nexa Module，让每台设备，成为能理解自然语言的 Agent Module。"),
    (6.20,"一句自然语言，结合设备能力上下文，由云端 AI 匹配成可执行的 Skill 计划。"),
    (13.15,"云端负责理解，设备负责校验权限、风险与参数，并在本地安全执行。"),
    (20.10,"设备通过固定 IPv6 与 TCP 加密连接，直连应用服务器，业务不再经过平台中转。"),
    (27.05,"工业设备、楼宇园区和智慧农业，都能获得自然语言控制能力。"),
    (32.10,"Nexa Module。自然语言进入，设备能力发生。"),
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
    cmd=[ff,"-y",*inputs,"-filter_complex",";".join(filters),"-map","0:v:0","-map","[outa]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-t","36","-movflags","+faststart",temp]
    subprocess.check_call(cmd)
    os.replace(temp,"nexa-module-intro.mp4")
print("Chinese voice-over added to nexa-module-intro.mp4")
