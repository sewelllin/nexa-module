from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import subprocess

import imageio_ffmpeg

W, H, FPS, DURATION = 1280, 720, 30, 42
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_REGULAR = "C:/Windows/Fonts/msyh.ttc"
OUTPUT = "nexa-module-intro.mp4"
POSTER = "nexa-video-poster.jpg"

GREEN = (94, 235, 159)
LIME = (194, 255, 89)
DARK = (6, 14, 10)
DEEP = (13, 45, 32)
INK = (11, 30, 20)
MUTED = (141, 168, 152)
WHITE = (248, 255, 250)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def text(draw, xy, value, size, color, bold=False, anchor=None, spacing=8):
    draw.multiline_text(xy, value, font=font(size, bold), fill=color, anchor=anchor, spacing=spacing, align="center" if anchor else "left")


def rounded(draw, bounds, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=width)


def background(dark=True):
    image = Image.new("RGB", (W, H), DARK if dark else (246, 249, 246))
    draw = ImageDraw.Draw(image, "RGBA")
    grid = (112, 246, 178, 13) if dark else (22, 90, 58, 10)
    for x in range(0, W, 64):
        draw.line((x, 0, x, H), fill=grid)
    for y in range(0, H, 64):
        draw.line((0, y, W, y), fill=grid)
    return image, draw


def glow(image, x, y, radius, alpha=90):
    layer = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*GREEN, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius // 2))
    image.paste(layer, (0, 0), layer)


def module(draw, x, y, scale=1.0):
    outer_w, outer_h = 220 * scale, 268 * scale
    rounded(draw, (x-outer_w/2, y-outer_h/2, x+outer_w/2, y+outer_h/2), 30*scale, (9, 31, 22, 255), (76, 132, 97, 255), 3)
    rounded(draw, (x-outer_w/2+18*scale, y-outer_h/2+18*scale, x+outer_w/2-18*scale, y+outer_h/2-18*scale), 22*scale, (15, 52, 37, 255), (58, 108, 80, 255), 2)
    rounded(draw, (x-62*scale, y-62*scale, x+62*scale, y+62*scale), 24*scale, (*LIME, 255))
    text(draw, (x, y-9*scale), "NEXA", max(16, int(29*scale)), INK, True, "mm")
    text(draw, (x, y+27*scale), "AGENT MODULE", max(6, int(8*scale)), INK, True, "mm")
    for index in range(6):
        pin_x = x - 47*scale + index*19*scale
        rounded(draw, (pin_x, y+104*scale, pin_x+8*scale, y+122*scale), 3*scale, (83, 113, 96, 255))


def title(draw, value, dark=True):
    text(draw, (640, 72), value, 38, WHITE if dark else INK, True, "ma")


def card(draw, bounds, heading, body="", accent=False, dark=False, centered=False):
    x1, y1, x2, y2 = bounds
    if accent:
        fill, outline, heading_color, body_color = (*LIME, 255), (*LIME, 255), INK, (55, 79, 63)
    elif dark:
        fill, outline, heading_color, body_color = (*DEEP, 248), (80, 142, 105, 255), WHITE, MUTED
    else:
        fill, outline, heading_color, body_color = (255, 255, 255, 248), (211, 224, 215, 255), INK, (73, 94, 81)
    rounded(draw, bounds, 22, fill, outline, 2)
    if centered:
        center_x, center_y = (x1+x2)/2, (y1+y2)/2
        text(draw, (center_x, center_y), heading, 19, heading_color, True, "mm")
        return
    text(draw, (x1+28, y1+28), heading, 22, heading_color, True)
    if body:
        text(draw, (x1+28, y1+76), body, 15, body_color, False, spacing=9)


def packet_line(draw, start, end, t, count=7, color=GREEN):
    draw.line((*start, *end), fill=(*color, 170), width=3)
    for index in range(count):
        progress = (t * 0.42 + index / count) % 1
        x = start[0] + (end[0] - start[0]) * progress
        y = start[1] + (end[1] - start[1]) * progress
        draw.ellipse((x-5, y-5, x+5, y+5), fill=(*color, 245))


def fade(draw, global_time, start, end):
    edge = min((global_time-start)/0.45, (end-global_time)/0.45, 1)
    alpha = int(255 * (1 - max(0, edge)))
    if alpha > 0:
        draw.rectangle((0, 0, W, H), fill=(*DARK, alpha))


def scene_intro(t):
    image, draw = background(True)
    glow(image, 930, 350, 270)
    draw = ImageDraw.Draw(image, "RGBA")
    for index in range(3):
        radius = 150 + index*60 + 5*math.sin(t*1.4+index)
        draw.ellipse((930-radius, 350-radius, 930+radius, 350+radius), outline=(112, 246, 178, 32), width=2)
    text(draw, (96, 110), "NEXA MODULE", 14, GREEN, True)
    text(draw, (96, 190), "自然语言进入", 54, WHITE, True)
    text(draw, (96, 260), "设备能力发生", 54, GREEN, True)
    text(draw, (100, 350), "设备直接理解、执行，\n并把结果送回业务。", 19, MUTED, False, spacing=10)
    labels = ["自然语言输入", "设备自主工作", "业务直接连接"]
    for index, label in enumerate(labels):
        card(draw, (100+index*220, 455, 300+index*220, 515), label, accent=index == 0, centered=True)
    module(draw, 930, 350, 0.9)
    return image, draw


def scene_inputs(t):
    image, draw = background(False)
    title(draw, "所有入口，都能直接说人话", False)
    input_cards = [
        ((90, 170, 330, 250), "串口文字"),
        ((90, 470, 330, 550), "远程控制"),
        ((950, 170, 1190, 250), "语音输入"),
        ((950, 470, 1190, 550), "本地界面"),
    ]
    centers = [(330, 210), (330, 510), (950, 210), (950, 510)]
    module_center = (640, 360)
    for index, (bounds, label) in enumerate(input_cards):
        card(draw, bounds, label, accent=int(t*2) % 4 == index, centered=True)
        packet_line(draw, centers[index], module_center, t+index*0.25, 4)
    module(draw, *module_center, 0.62)
    text(draw, (640, 640), "一种表达方式，覆盖所有设备入口", 18, (46, 119, 78), True, "ma")
    return image, draw


def scene_module(t):
    image, draw = background(True)
    glow(image, 640, 365, 225)
    draw = ImageDraw.Draw(image, "RGBA")
    title(draw, "意图理解，是 Module 的内置能力", True)
    capabilities = [
        ((110, 190, 350, 270), "理解输入", (350, 230)),
        ((930, 190, 1170, 270), "判断任务", (930, 230)),
        ((110, 470, 350, 550), "调度能力", (350, 510)),
        ((930, 470, 1170, 550), "本地执行", (930, 510)),
    ]
    for index, (bounds, label, point) in enumerate(capabilities):
        card(draw, bounds, label, accent=int(t*1.5) % 4 == index, centered=True)
        packet_line(draw, point, (640, 365), t+index*0.2, 3)
    module(draw, 640, 365, 0.68)
    text(draw, (640, 635), "设备会听懂、会判断、会行动", 18, MUTED, True, "ma")
    return image, draw


def scene_direct(t):
    image, draw = background(False)
    title(draw, "设备直接连接业务终点", False)
    card(draw, (70, 205, 390, 505), "Nexa Module", "理解自然语言\n执行设备能力\n主动上报数据", accent=True)
    card(draw, (890, 205, 1210, 505), "应用服务器", "接收状态与事件\n展示业务结果\n下发自然语言任务", dark=True)
    packet_line(draw, (410, 360), (870, 360), t, 8, (43, 157, 103))
    tags = [(480, 270, 580, 320, "状态"), (590, 270, 690, 320, "事件"), (700, 270, 820, 320, "业务数据")]
    for index, (x1, y1, x2, y2, label) in enumerate(tags):
        card(draw, (x1, y1, x2, y2), label, accent=int(t*1.8) % 3 == index, centered=True)
    text(draw, (640, 625), "绕过中间平台，数据直接回到客户应用", 18, (46, 119, 78), True, "ma")
    return image, draw


def scene_shift(t):
    image, draw = background(True)
    title(draw, "从层层接入，到设备直达业务", True)
    text(draw, (235, 145), "传统链路", 15, MUTED, True, "ma")
    stages = ["业务需求", "控制接口", "IoT 平台", "设备协议", "硬件动作"]
    for index, label in enumerate(stages):
        y = 175 + index*82
        card(draw, (95, y, 375, y+54), label, dark=True, centered=True)
        if index < len(stages)-1:
            text(draw, (235, y+68), "↓", 15, (107, 154, 127), True, "mm")
    text(draw, (430, 355), "→", 38, GREEN, True, "mm")
    card(draw, (500, 225, 805, 495), "Nexa Module", "自然语言输入\n模组理解与执行\n数据主动上报", accent=True)
    packet_line(draw, (825, 360), (900, 360), t, 3, LIME)
    card(draw, (920, 255, 1185, 465), "业务应用", "拿到结果\n看到状态\n形成闭环", dark=True)
    return image, draw


def scene_final(t):
    image, draw = background(True)
    glow(image, 640, 310, 280, 110)
    draw = ImageDraw.Draw(image, "RGBA")
    module(draw, 640, 235, 0.54)
    text(draw, (640, 430), "让设备听懂人话", 50, WHITE, True, "ma")
    text(draw, (640, 500), "并直接连接你的业务", 50, GREEN, True, "ma")
    text(draw, (640, 610), "Natural Language In  ·  Module Acts  ·  Data Direct To App", 14, MUTED, True, "ma")
    return image, draw


SCENES = [
    (0, 6, scene_intro),
    (6, 13, scene_inputs),
    (13, 20, scene_module),
    (20, 28, scene_direct),
    (28, 36, scene_shift),
    (36, 42, scene_final),
]

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
command = [
    ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
    "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "18",
    "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUTPUT,
]
process = subprocess.Popen(command, stdin=subprocess.PIPE)
poster = None
for frame_index in range(FPS * DURATION):
    global_time = frame_index / FPS
    for start, end, renderer in SCENES:
        if start <= global_time < end:
            frame, frame_draw = renderer(global_time - start)
            fade(frame_draw, global_time, start, end)
            break
    if frame_index == FPS * 2:
        poster = frame.copy()
    process.stdin.write(frame.tobytes())

process.stdin.close()
process.wait()
if poster:
    poster.save(POSTER, quality=92)
print(os.path.abspath(OUTPUT), os.path.getsize(OUTPUT))
