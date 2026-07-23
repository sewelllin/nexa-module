from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, subprocess, imageio_ffmpeg

W, H, FPS, DURATION = 1280, 720, 30, 42
FB, FR = "C:/Windows/Fonts/msyhbd.ttc", "C:/Windows/Fonts/msyh.ttc"
OUT, POSTER = "nexa-module-intro.mp4", "nexa-video-poster.jpg"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def txt(d, xy, s, n, c, bold=False, a=None):
    d.text(xy, s, font=font(n, bold), fill=c, anchor=a)


def box(d, b, r, fill, outline=None, w=1):
    d.rounded_rectangle(b, radius=r, fill=fill, outline=outline, width=w)


def ease(x):
    x = max(0, min(1, x))
    return x * x * (3 - 2 * x)


def canvas(dark=True):
    im = Image.new("RGB", (W, H), (5, 12, 9) if dark else (245, 248, 244))
    d = ImageDraw.Draw(im, "RGBA")
    grid = (112, 246, 178, 15) if dark else (22, 90, 58, 12)
    for x in range(0, W, 64):
        d.line((x, 0, x, H), fill=grid)
    for y in range(0, H, 64):
        d.line((0, y, W, y), fill=grid)
    return im, d


def glow(im, x, y, r, col=(91, 235, 160), a=95):
    lay = Image.new("RGBA", (W, H))
    q = ImageDraw.Draw(lay)
    q.ellipse((x - r, y - r, x + r, y + r), fill=(*col, a))
    lay = lay.filter(ImageFilter.GaussianBlur(r // 2))
    im.paste(lay, (0, 0), lay)


def chip(d, x, y, s=1):
    box(d, (x - 118*s, y - 148*s, x + 118*s, y + 148*s), 34*s, (9, 31, 22, 255), (79, 130, 100, 255), 3)
    box(d, (x - 96*s, y - 126*s, x + 96*s, y + 126*s), 24*s, (15, 52, 37, 255), (61, 109, 82, 255), 2)
    box(d, (x - 66*s, y - 66*s, x + 66*s, y + 66*s), 26*s, (202, 255, 99, 255))
    txt(d, (x, y - 10*s), "NEXA", int(31*s), (8, 36, 23), True, "mm")
    txt(d, (x, y + 31*s), "AGENT MODULE", int(8*s), (8, 36, 23), True, "mm")
    for i in range(6):
        px = x - 48*s + i * 19*s
        box(d, (px, y + 108*s, px + 8*s, y + 126*s), 4*s, (82, 111, 95, 255))


def pill(d, x, y, label, active=False):
    fill = (202, 255, 99, 255) if active else (255, 255, 255, 235)
    box(d, (x, y, x + 210, y + 56), 16, fill)
    txt(d, (x + 105, y + 29), label, 16, (12, 31, 20), True, "mm")


def card(d, x, y, w, h, title, body, dark=False, accent=False):
    fill = (14, 45, 33, 245) if dark else (255, 255, 255, 245)
    line = (82, 142, 106, 255) if dark else (204, 218, 208, 255)
    if accent:
        fill = line = (202, 255, 99, 255)
    box(d, (x, y, x + w, y + h), 22, fill, line, 2)
    txt(d, (x + 26, y + 42), title, 22, (10, 33, 20) if accent or not dark else (240, 255, 247), True)
    txt(d, (x + 26, y + 84), body, 15, (72, 84, 75) if accent or not dark else (158, 184, 169))


def packets(d, a, b, t, n=6, col=(98, 240, 171)):
    for i in range(n):
        u = (t * .55 + i / n) % 1
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(*col, 245))


def fade(d, t, a, b):
    alpha = int(255 * max(1 - ease((t - a) / .45), 1 - ease((b - t) / .45)))
    if alpha:
        d.rectangle((0, 0, W, H), fill=(5, 12, 9, alpha))


def intro(t):
    im, d = canvas(True)
    glow(im, 910, 355, 280)
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(3):
        r = 155 + i * 62 + 8 * math.sin(t * 1.5 + i)
        d.ellipse((910-r, 355-r, 910+r, 355+r), outline=(112, 246, 178, 36), width=2)
    chip(d, 910, 355, .92)
    txt(d, (96, 116), "NEXA MODULE", 14, (110, 244, 174), True)
    txt(d, (96, 188), "自然语言进入", 56, (255, 255, 255), True)
    txt(d, (96, 258), "设备能力发生", 56, (91, 235, 160), True)
    txt(d, (100, 356), "不是设备接入平台，而是设备直接理解、执行并回到业务。", 19, (153, 177, 164))
    pill(d, 100, 438, "任何入口都能说人话", True)
    pill(d, 330, 438, "去中间节点")
    pill(d, 560, 438, "直达应用服务器")
    return im, d


def inputs(t):
    im, d = canvas(False)
    txt(d, (640, 62), "所有入口，都变成自然语言入口", 38, (12, 24, 17), True, "ma")
    chip(d, 640, 380, .62)
    data = [("串口文本", 110, 165), ("远程控制", 110, 500), ("语音转写", 970, 165), ("本地界面", 970, 500)]
    for i, (lab, x, y) in enumerate(data):
        active = int(t * 2.2) % 4 == i
        pill(d, x, y, lab, active)
        sx, sy = (x + 210 if x < 640 else x), y + 28
        ex, ey = (548 if x < 640 else 732), 380
        d.line((sx, sy, ex, ey), fill=(45, 157, 104, 110), width=2)
        packets(d, (sx, sy), (ex, ey), t + i * .13, 3)
    txt(d, (640, 640), "Nexa Module 统一接收、理解任务边界", 18, (46, 119, 78), True, "ma")
    return im, d


def module(t):
    im, d = canvas(True)
    glow(im, 640, 360, 230)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (640, 58), "AI 意图理解，是 Module 的内置能力", 38, (255, 255, 255), True, "ma")
    chip(d, 640, 360, .72)
    nodes = [("理解输入", -260, -90), ("判断任务", 240, -90), ("调度能力", -250, 130), ("本地执行", 250, 130)]
    for i, (lab, dx, dy) in enumerate(nodes):
        x, y = 640 + dx + 6*math.sin(t*2+i), 360 + dy + 6*math.cos(t*2+i)
        card(d, x-88, y-36, 176, 72, lab, "", accent=(i == int(t*1.6) % 4))
        d.line((x, y, 640 + (85 if dx < 0 else -85), 360 + (40 if dy < 0 else -40)), fill=(102, 235, 168, 80), width=2)
    txt(d, (640, 638), "用户看到的是：设备会听懂、会判断、会行动", 18, (153, 177, 164), True, "ma")
    return im, d


def direct(t):
    im, d = canvas(False)
    txt(d, (640, 58), "设备直接连接业务终点", 38, (12, 24, 17), True, "ma")
    card(d, 80, 230, 310, 260, "Nexa Module", "理解自然语言\n执行设备能力\n主动上报数据", accent=True)
    chip(d, 235, 372, .38)
    card(d, 890, 230, 310, 260, "应用服务器", "接收状态 / 事件\n展示业务结果\n下发自然语言任务", dark=True)
    d.line((410, 360, 870, 360), fill=(42, 150, 101), width=4)
    packets(d, (410, 360), (870, 360), t, 9)
    for i, lab in enumerate(["状态", "事件", "业务数据"]):
        pill(d, 495 + i*125, 295 + 18*math.sin(t*2+i), lab, i == int(t*2) % 3)
    txt(d, (640, 620), "数据不被困在中间平台里，直接回到客户应用。", 18, (45, 119, 78), True, "ma")
    return im, d


def shift(t):
    im, d = canvas(True)
    txt(d, (640, 60), "从接平台，到设备直达业务", 38, (255, 255, 255), True, "ma")
    for i, lab in enumerate(["业务需求", "控制接口", "IoT 平台", "设备协议", "硬件动作"]):
        y = 160 + i * 78
        card(d, 95, y, 270, 52, lab, "", dark=True)
        if i < 4:
            txt(d, (230, y + 66), "↓", 18, (86, 120, 101), True, "mm")
    card(d, 475, 230, 330, 260, "Nexa Module", "自然语言输入\n模组理解与执行\n数据直达应用", accent=True)
    card(d, 915, 260, 250, 190, "业务应用", "拿到结果\n看到状态\n形成闭环", dark=True)
    d.line((805, 360, 915, 360), fill=(202, 255, 99), width=4)
    packets(d, (805, 360), (915, 360), t, 3, (202, 255, 99))
    return im, d


def final(t):
    im, d = canvas(True)
    glow(im, 640, 335, 300, a=120)
    d = ImageDraw.Draw(im, "RGBA")
    chip(d, 640, 250, .58)
    txt(d, (640, 430), "让设备听懂人话", 54, (255, 255, 255), True, "ma")
    txt(d, (640, 500), "并直接连到你的业务", 54, (91, 235, 160), True, "ma")
    txt(d, (640, 610), "Natural Language In · Module Acts · Data Direct To App", 14, (153, 177, 164), True, "ma")
    return im, d


SCENES = [(0, 6, intro), (6, 13, inputs), (13, 20, module), (20, 28, direct), (28, 36, shift), (36, 42, final)]
ff = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
poster = None
for frame in range(FPS * DURATION):
    t = frame / FPS
    for a, b, fn in SCENES:
        if a <= t < b:
            im, d = fn(t - a)
            fade(d, t, a, b)
            break
    if frame == FPS * 2:
        poster = im.copy()
    p.stdin.write(im.tobytes())
p.stdin.close()
p.wait()
if poster:
    poster.save(POSTER, quality=92)
print(os.path.abspath(OUT), os.path.getsize(OUT))
print(os.path.abspath(POSTER), os.path.getsize(POSTER))
