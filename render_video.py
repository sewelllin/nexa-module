from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, subprocess, imageio_ffmpeg, os

W,H,FPS,DURATION=1280,720,24,36
OUT="nexa-module-intro.mp4"
TMP="nexa-silent.mp4"
FONT="C:/Windows/Fonts/msyh.ttc"
FONT_B="C:/Windows/Fonts/msyhbd.ttc"
def font(size,b=False): return ImageFont.truetype(FONT_B if b else FONT,size)
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def fade(t,a,b,edge=.55): return min(ease((t-a)/edge),ease((b-t)/edge))
def text(draw,xy,s,size,fill=(17,23,18),bold=False,anchor=None):
    draw.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
def rounded(draw,box,r,fill,outline=None,width=1): draw.rounded_rectangle(box,r,fill,outline,width)
def scene_time(t,a,b): return max(0,min(1,(t-a)/(b-a)))
def chip(img,cx,cy,scale=1):
    d=ImageDraw.Draw(img,"RGBA"); w,h=int(250*scale),int(310*scale)
    rounded(d,(cx-w//2,cy-h//2,cx+w//2,cy+h//2),int(34*scale),(20,36,28,255),(57,79,68,255),4)
    rounded(d,(cx-w//2+18,cy-h//2+18,cx+w//2-18,cy+h//2-18),int(24*scale),(25,44,35,255),(68,91,79,255),2)
    text(d,(cx,cy-110*scale),"NEXA AGENT ONLINE",int(9*scale),(104,255,178),True,"mm")
    rounded(d,(cx-70*scale,cy-72*scale,cx+70*scale,cy+68*scale),int(26*scale),(96,229,163,255))
    text(d,(cx,cy-10*scale),"NEXA",int(34*scale),(13,42,31),True,"mm")
    text(d,(cx,cy+30*scale),"AGENT MODULE",int(9*scale),(13,42,31),True,"mm")
    for i in range(5): rounded(d,(cx-38*scale+i*19*scale,cy+115*scale,cx-30*scale+i*19*scale,cy+132*scale),4,(88,112,99,255))

ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",TMP]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for n in range(FPS*DURATION):
    t=n/FPS
    img=Image.new("RGB",(W,H),(247,248,246)); d=ImageDraw.Draw(img,"RGBA")
    # subtle grid
    for x in range(0,W,64): d.line((x,0,x,H),fill=(22,54,39,10))
    for y in range(0,H,64): d.line((0,y,W,y),fill=(22,54,39,10))
    if t<6:
        a=fade(t,0,6); k=ease(scene_time(t,0,5))
        text(d,(80,68),"NEXA MODULE",16,(35,123,88),True)
        text(d,(80,210-int((1-k)*25)),"让每台设备成为",52,(17,23,18),True)
        text(d,(80,282-int((1-k)*25)),"能理解自然语言的",62,(35,131,93),True)
        text(d,(80,366-int((1-k)*25)),"Agent Module。",62,(35,131,93),True)
        text(d,(82,475),"云端理解意图 · 端侧执行 Skills · IPv6 直连业务",20,(102,113,105))
        chip(img,1015,350,0.9+0.03*math.sin(t*2))
    elif t<13:
        u=scene_time(t,6,13); text(d,(640,72),"一句自然语言，成为一个可执行计划",38,(17,23,18),True,"ma")
        items=[("01","自然语言输入","“把 2 号风机打开 15 分钟”"),("02","设备能力上下文","fan.control · timer.schedule"),("03","云端意图匹配","fan.timed_run · confidence 0.98")]
        for i,(num,title,sub) in enumerate(items):
            x=90+i*400; y=230; delay=i*.16; v=ease(max(0,min(1,(u-delay)*2.2)))
            rounded(d,(x,y+30*(1-v),x+330,y+250+30*(1-v)),18,(255,255,255,255),(219,228,221,255),2)
            rounded(d,(x+24,y+25+30*(1-v),x+67,y+68+30*(1-v)),12,(57,217,138,255))
            text(d,(x+45,y+47+30*(1-v)),num,12,(10,47,31),True,"mm")
            text(d,(x+24,y+105+30*(1-v)),title,23,(17,23,18),True)
            text(d,(x+24,y+160+30*(1-v)),sub,15,(105,117,108))
            if i<2:
                d.line((x+340,y+140,x+390,y+140),fill=(43,139,99,255),width=3)
                d.polygon([(x+390,y+140),(x+378,y+133),(x+378,y+147)],fill=(43,139,99,255))
    elif t<20:
        u=scene_time(t,13,20); text(d,(640,68),"云端负责理解，设备负责决定",38,(17,23,18),True,"ma")
        # cloud
        rounded(d,(80,190,535,570),22,(9,42,32,255))
        text(d,(120,232),"NEXA INTENT",14,(102,255,182),True)
        text(d,(120,292),"理解意图",36,(255,255,255),True)
        for i,s in enumerate(["识别目标与参数","匹配设备现有 Skills","返回结构化 Skill Plan"]):
            text(d,(125,370+i*48),"✓  "+s,18,(179,204,192))
        # edge
        rounded(d,(745,190,1200,570),22,(255,255,255,255),(219,228,221,255),2)
        text(d,(785,232),"NEXA MODULE",14,(35,123,88),True)
        text(d,(785,292),"校验并执行",36,(17,23,18),True)
        for i,s in enumerate(["权限与参数校验","风险策略与二次确认","本地 Skill 安全执行"]):
            text(d,(790,370+i*48),"✓  "+s,18,(91,106,96))
        # animated packet
        x=550+180*((math.sin(u*math.pi*4)+1)/2)
        rounded(d,(x,340,x+95,382),10,(200,255,101,255))
        text(d,(x+47,361),"PLAN",11,(13,42,31),True,"mm")
    elif t<27:
        u=scene_time(t,20,27); text(d,(640,65),"去平台化业务链路",38,(17,23,18),True,"ma")
        text(d,(640,115),"固定 IPv6 · TCP + TLS · 设备与应用服务器直连",17,(100,113,104),False,"ma")
        chip(img,260,385,.72)
        rounded(d,(880,255,1160,520),24,(9,42,32,255))
        text(d,(1020,320),"应用服务器",27,(255,255,255),True,"mm")
        text(d,(1020,365),"BUSINESS SERVER",11,(101,240,174),True,"mm")
        for i in range(3): rounded(d,(930,410+i*27,1110,425+i*27),6,(53,86,72,255))
        d.line((455,385,865,385),fill=(54,129,95,255),width=3)
        for i in range(4):
            px=455+((u*360+i*.25)%1)*410
            d.ellipse((px-7,378,px+7,392),fill=(83,239,169,255))
        text(d,(660,350),"不经过传统 IoT 业务中转平台",15,(35,123,88),True,"mm")
        text(d,(660,420),"端到端身份 · 幂等 · 防重放 · 离线降级",15,(104,116,107),False,"mm")
    elif t<32:
        u=scene_time(t,27,32); text(d,(640,76),"一个模组，连接更多设备能力",38,(17,23,18),True,"ma")
        labels=[("工业设备","PLC · Modbus · CAN"),("楼宇园区","照明 · 门禁 · 空调"),("智慧农业","灌溉 · 补光 · 采集"),("开发者模组","GPIO · UART · I²C")]
        for i,(title,sub) in enumerate(labels):
            x=70+i*300; y=235+18*math.sin(u*4+i)
            rounded(d,(x,y,x+260,y+250),20,(255,255,255,255),(219,228,221,255),2)
            text(d,(x+28,y+48),f"0{i+1}",12,(35,139,96),True)
            text(d,(x+28,y+116),title,25,(17,23,18),True)
            text(d,(x+28,y+165),sub,14,(102,113,105))
    else:
        u=scene_time(t,32,36); a=fade(t,32,36,.7)
        text(d,(640,105),"NEXA MODULE",17,(35,123,88),True,"ma")
        text(d,(640,235),"让每台设备成为",55,(17,23,18),True,"ma")
        text(d,(640,315),"能理解自然语言的 Agent Module。",46,(35,131,93),True,"ma")
        rounded(d,(490,440,790,502),12,(17,23,18,255))
        text(d,(640,471),"NATURAL LANGUAGE → ACTION",13,(255,255,255),True,"mm")
        text(d,(640,585),"nexa module · product concept",13,(121,132,123),False,"ma")
    # scene number
    text(d,(1195,675),f"{min(6,int(t//6)+1):02d} / 06",10,(126,138,129),True,"ra")
    p.stdin.write(img.tobytes())
p.stdin.close(); p.wait()
# add a restrained generated ambient soundtrack
audio="0.035*sin(2*PI*110*t)+0.025*sin(2*PI*164.81*t)+0.018*sin(2*PI*220*t)"
cmd2=[ff,"-y","-i",TMP,"-f","lavfi","-i",f"aevalsrc={audio}:s=44100:d={DURATION}","-filter:a",f"afade=t=in:st=0:d=2,afade=t=out:st={DURATION-3}:d=3","-c:v","copy","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",OUT]
subprocess.check_call(cmd2)
os.remove(TMP)
print(os.path.abspath(OUT),os.path.getsize(OUT))

