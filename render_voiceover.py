import asyncio
import os
import subprocess
import tempfile

import edge_tts
import imageio_ffmpeg

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+15%"
VIDEO = "nexa-module-intro.mp4"
OUTPUT = "nexa-module-with-voice.mp4"

SEGMENTS = [
    (0.65, "Nexa Module，让自然语言进入，让设备能力发生。"),
    (6.35, "串口、远程、语音或本地界面，都能用自然语言表达任务。"),
    (13.35, "意图理解内置于模组。设备听懂需求，自主判断、调度能力，并完成执行。"),
    (20.35, "状态、事件和业务数据，不再经过传统物联网平台，而是由设备直达应用服务器。"),
    (28.35, "更少的中间节点，更短的交付链路，让设备自主工作，也让数据回到客户手中。"),
    (36.45, "Nexa Module。让设备听懂人话，并直接连接你的业务。"),
]


async def synthesize(folder):
    audio_files = []
    for index, (_, line) in enumerate(SEGMENTS):
        audio_path = os.path.join(folder, f"voice-{index}.mp3")
        await edge_tts.Communicate(line, VOICE, rate=RATE).save(audio_path)
        audio_files.append(audio_path)
    return audio_files


with tempfile.TemporaryDirectory(prefix="nexa-voice-") as temp_dir:
    files = asyncio.run(synthesize(temp_dir))
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    inputs = ["-i", VIDEO]
    for audio_file in files:
        inputs.extend(["-i", audio_file])

    filters = []
    delayed_tracks = []
    for input_index, (start, _) in enumerate(SEGMENTS, 1):
        delay = int(start * 1000)
        filters.append(
            f"[{input_index}:a]aresample=48000,highpass=f=90,lowpass=f=9000,"
            f"acompressor=threshold=-18dB:ratio=2.5:attack=8:release=100,"
            f"volume=1.08,adelay={delay}|{delay}[voice{input_index}]"
        )
        delayed_tracks.append(f"[voice{input_index}]")

    filters.append(
        "".join(delayed_tracks)
        + f"amix=inputs={len(files)}:duration=longest:dropout_transition=0:normalize=0,"
        "alimiter=limit=0.92:attack=5:release=80[voice]"
    )
    command = [
        ffmpeg, "-y", *inputs, "-filter_complex", ";".join(filters),
        "-map", "0:v:0", "-map", "[voice]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", "42", "-movflags", "+faststart", OUTPUT,
    ]
    subprocess.check_call(command)

os.replace(OUTPUT, VIDEO)
print("Chinese narration added")
