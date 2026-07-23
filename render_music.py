import os
import subprocess
import wave

import imageio_ffmpeg
import numpy as np

SAMPLE_RATE, DURATION = 48000, 42
SAMPLE_COUNT = SAMPLE_RATE * DURATION
VIDEO, WAV, OUTPUT = "nexa-module-intro.mp4", "nexa-bg-music.wav", "nexa-module-final.mp4"
music = np.zeros((SAMPLE_COUNT, 2), dtype=np.float64)
tempo = 92
beat = 60 / tempo
chords = [
    [130.81, 164.81, 196.00, 246.94],
    [110.00, 130.81, 164.81, 220.00],
    [87.31, 130.81, 174.61, 220.00],
    [98.00, 146.83, 196.00, 220.00],
]

for chord_index, start in enumerate(np.arange(0, DURATION, beat * 4)):
    duration = beat * 4.7
    start_sample = int(start * SAMPLE_RATE)
    end_sample = min(SAMPLE_COUNT, int((start + duration) * SAMPLE_RATE))
    timeline = np.arange(end_sample - start_sample) / SAMPLE_RATE
    envelope = np.minimum(1, timeline / 0.7) * np.minimum(1, (duration - timeline) / 1.1)
    for note_index, frequency in enumerate(chords[chord_index % len(chords)]):
        tone = np.sin(2 * np.pi * frequency * timeline)
        tone += 0.12 * np.sin(2 * np.pi * frequency * 2 * timeline)
        pan = 0.3 + 0.4 * note_index / 3
        music[start_sample:end_sample, 0] += tone * envelope * (1 - pan) * 0.055
        music[start_sample:end_sample, 1] += tone * envelope * pan * 0.055

scale = [261.63, 329.63, 392.00, 493.88, 440.00, 392.00, 329.63, 293.66]
for note_index, start in enumerate(np.arange(0, DURATION, beat)):
    if note_index % 4 == 3:
        continue
    duration = 0.48
    start_sample = int(start * SAMPLE_RATE)
    end_sample = min(SAMPLE_COUNT, start_sample + int(duration * SAMPLE_RATE))
    timeline = np.arange(end_sample - start_sample) / SAMPLE_RATE
    envelope = np.exp(-timeline * 7) * (1 - np.exp(-timeline * 60))
    frequency = scale[note_index % len(scale)]
    tone = np.sin(2 * np.pi * frequency * timeline)
    tone += 0.16 * np.sin(2 * np.pi * frequency * 2 * timeline)
    pan = 0.38 + 0.24 * (note_index % 8) / 7
    music[start_sample:end_sample, 0] += tone * envelope * (1 - pan) * 0.10
    music[start_sample:end_sample, 1] += tone * envelope * pan * 0.10

delay = int(0.22 * SAMPLE_RATE)
music[delay:, 0] += music[:-delay, 1] * 0.08
music[delay:, 1] += music[:-delay, 0] * 0.08
fade = int(1.5 * SAMPLE_RATE)
music[:fade] *= np.linspace(0, 1, fade)[:, None]
music[-fade:] *= np.linspace(1, 0, fade)[:, None]
music /= max(1, np.max(np.abs(music)) / 0.68)

pcm = (music * 32767).astype(np.int16)
with wave.open(WAV, "wb") as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(pcm.tobytes())

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
filter_graph = (
    "[0:a]asplit=2[voice][sidechain];"
    "[1:a]volume=0.17,lowpass=f=6000[music];"
    "[music][sidechain]sidechaincompress=threshold=0.025:ratio=8:attack=25:release=420[ducked];"
    "[voice][ducked]amix=inputs=2:duration=first:dropout_transition=0,"
    "loudnorm=I=-17:TP=-1.5:LRA=9,alimiter=limit=0.95:attack=5:release=100[audio]"
)
command = [
    ffmpeg, "-y", "-i", VIDEO, "-i", WAV, "-filter_complex", filter_graph,
    "-map", "0:v:0", "-map", "[audio]", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", "42",
    "-movflags", "+faststart", OUTPUT,
]
subprocess.check_call(command)
os.replace(OUTPUT, VIDEO)
os.remove(WAV)
print("Light background music mixed under narration")
