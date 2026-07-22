from PIL import Image,ImageDraw,ImageFont
import math,subprocess,imageio_ffmpeg,os
W,H,FPS,DURATION=1280,720,24,42
FONT="C:/Windows/Fonts/msyh.ttc"; FONT_B="C:/Windows/Fonts/msyhbd.ttc"
def f(n,b=False):return ImageFont.truetype(FONT_B if b else FONT,n)
def tx(d,xy,s,n,fill=(13,20,16),b=False,anchor=None):d.text(xy,s,font=f(n,b),fill=fill,anchor=anchor)
def box(d,b,r,fill,outline=None,w=1):d.rounded_rectangle(b,r,fill,outline,w)
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def chip(d,cx,cy,s=1):
    box(d,(cx-105*s,cy-137*s,cx+105*s,cy+137*s),28*s,(10,32,23,255),(55,94,74,255),3)
    box(d,(cx-88*s,cy-120*s,cx+88*s,cy+120*s),20*s,(16,45,33,255),(62,106,83,255),2)
    box(d,(cx-60*s,cy-62*s,cx+60*s,cy+58*s),24*s,(104,236,166,255))
    tx(d,(cx,cy-7*s),"NEXA",int(28*s),(10,38,26),True,"mm");tx(d,(cx,cy+27*s),"AGENT MODULE",int(7*s),(10,38,26),True,"mm")
    tx(d,(cx,cy-103*s),"AGENT ONLINE",int(7*s),(105,244,177),True,"mm")
def arrow(d,a,b,label,color=(50,166,111,255)):
    d.line((*a,*b),fill=color,width=3);d.polygon([(b[0],b[1]),(b[0]-12,b[1]-7),(b[0]-12,b[1]+7)],fill=color)
    tx(d,((a[0]+b[0])//2,(a[1]+b[1])//2-18),label,10,(70,112,90),True,"mm")
def base():
    im=Image.new("RGB",(W,H),(244,246,242));d=ImageDraw.Draw(im,"RGBA")
    for x in range(0,W,64):d.line((x,0,x,H),fill=(20,60,40,10))
    for y in range(0,H,64):d.line((0,y,W,y),fill=(20,60,40,10))
    return im,d
ff=imageio_ffmpeg.get_ffmpeg_exe();out="nexa-module-intro.mp4"
p=subprocess.Popen([ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-crf","19","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
for n in range(FPS*DURATION):
    t=n/FPS;im,d=base()
    if t<5:
        u=ease(t/4);tx(d,(70,62),"NEXA MODULE · MG PRODUCT FILM",12,(34,128,88),True)
        tx(d,(70,205),"让设备，",62,(12,20,15),True);tx(d,(70,292),"理解自然语言。",70,(38,151,101),True)
        tx(d,(72,405),"自然语言进入 · 云端匹配意图 · 端侧执行 Skills",18,(96,108,100))
        chip(d,1000,355,.95+.025*math.sin(t*2))
        box(d,(785,110,1195,600),36,(49,218,145,12),(49,174,117,35),2)
    elif t<11:
        u=(t-5)/6;tx(d,(640,62),"一句话，进入真实设备场景",38,(12,20,15),True,"ma")
        scenes=[("工业控制","启动 3 号产线巡检","PLC · CAN"),("楼宇园区","关闭会议室空调","HVAC · BACnet"),("智慧农业","湿度低于 40% 开始灌溉","Sensor · Relay"),("移动终端","上报当前位置与设备状态","4G · GNSS")]
        for i,(a,b,c) in enumerate(scenes):
            x=55+i*305;y=205+12*math.sin(u*5+i)
            box(d,(x,y,x+275,y+330),20,(255,255,255,255),(214,222,216,255),2)
            box(d,(x+22,y+22,x+70,y+70),14,(75,229,157,255));tx(d,(x+46,y+46),f"0{i+1}",11,(8,42,27),True,"mm")
            tx(d,(x+22,y+112),a,24,(13,20,16),True);tx(d,(x+22,y+166),f"“{b}”",15,(56,72,62));tx(d,(x+22,y+280),c,10,(38,143,95),True)
    elif t<17:
        u=(t-11)/6;tx(d,(640,56),"多种输入，统一成为自然语言",38,(12,20,15),True,"ma")
        inputs=[("本地文字","屏幕 / 键盘"),("UART 串口","文本输入"),("语音转写","ASR 文本"),("远程控制","应用服务器")]
        for i,(a,b) in enumerate(inputs):
            y=150+i*105;x=80
            box(d,(x,y,x+260,y+76),14,(255,255,255,255),(213,222,215,255),2);tx(d,(x+22,y+29),a,16,(13,20,16),True);tx(d,(x+22,y+54),b,10,(103,115,106))
            endx=685;d.line((x+260,y+38,endx,y+38),fill=(56,157,108,110),width=2)
        chip(d,890,345,.78)
        box(d,(1050,260,1215,430),18,(10,42,30,255));tx(d,(1132,308),"统一输入对象",14,(255,255,255),True,"mm");tx(d,(1132,350),"NATURAL",12,(108,240,174),True,"mm");tx(d,(1132,375),"LANGUAGE",12,(108,240,174),True,"mm")
        arrow(d,(1010,345),(1040,345),"")
    elif t<24:
        u=(t-17)/7;tx(d,(640,54),"设备携带上下文，请求 AI 意图匹配",38,(12,20,15),True,"ma")
        chip(d,245,365,.72)
        box(d,(450,205,795,530),18,(9,39,28,255));tx(d,(480,242),"INTENT_RESOLVE_REQ",10,(99,236,169),True)
        rows=[("input","“打开 2 号风机 15 分钟”"),("skills","fan.control · timer.schedule"),("state","fan_2: off · signal: good"),("device","fixed IPv6 · certificate")]
        for i,(k,v) in enumerate(rows):
            tx(d,(485,302+i*48),k,10,(99,236,169),True);tx(d,(560,302+i*48),v,12,(219,232,224))
        box(d,(945,210,1200,520),20,(255,255,255,255),(210,221,214,255),2);tx(d,(1072,264),"AI 意图服务器",21,(13,20,16),True,"mm")
        tx(d,(1072,320),"意图识别",14,(38,137,94),True,"mm");tx(d,(1072,360),"参数抽取",14,(38,137,94),True,"mm");tx(d,(1072,400),"Skill 匹配",14,(38,137,94),True,"mm")
        arrow(d,(795,365),(930,365),"TCP + TLS")
    elif t<30:
        u=(t-24)/6;tx(d,(640,52),"Skill Plan 返回设备，本地校验并执行",38,(12,20,15),True,"ma")
        box(d,(65,190,360,545),18,(9,39,28,255));tx(d,(212,240),"AI RESPONSE",12,(99,236,169),True,"mm")
        tx(d,(100,305),"intent: fan.timed_run",14,(255,255,255));tx(d,(100,350),"confidence: 0.98",14,(192,211,200));tx(d,(100,395),"plan: 2 skills",14,(192,211,200))
        arrow(d,(375,365),(520,365),"Skill Plan")
        chip(d,650,365,.67)
        arrow(d,(770,365),(905,365),"Result")
        box(d,(920,190,1210,545),18,(255,255,255,255),(210,221,214,255),2);tx(d,(1065,240),"应用服务器",21,(13,20,16),True,"mm")
        for i,s in enumerate(["fan_2 = ON","auto_off = 900s","request = completed"]):
            box(d,(955,300+i*55,1175,338+i*55),9,(232,242,235,255));tx(d,(1065,319+i*55),s,12,(30,80,54),True,"mm")
        tx(d,(650,565),"端侧权限 · 参数 · 风险策略校验",13,(45,129,89),True,"mm")
    elif t<35:
        u=(t-30)/5;tx(d,(640,55),"两款产品，共享同一套 Agent 能力",38,(12,20,15),True,"ma")
        cards=[(85,("Nexa Module Flex","4G + Wi‑Fi + BLE","多链路切换 · BLE 近场维护")),(665,("Nexa Module 4G","Pure 4G","独立联网 · 户外与移动部署"))]
        for x,(a,b,c) in cards:
            box(d,(x,175,x+530,555),24,(9,39,28,255) if x==85 else (255,255,255,255),(45,100,73,255),2)
            tx(d,(x+38,230),"NEXA PRODUCT",10,(99,236,169),True);tx(d,(x+38,300),a,29,(255,255,255) if x==85 else (13,20,16),True)
            tx(d,(x+38,345),b,17,(127,240,180) if x==85 else (37,144,96),True);tx(d,(x+38,445),c,13,(166,190,177) if x==85 else (91,107,97))
            chip(d,x+430,390,.38)
    elif t<39:
        u=(t-35)/4;tx(d,(640,55),"固定 IPv6 管控与在线兜底",38,(12,20,15),True,"ma")
        items=[("固定 IPv6","可寻址"),("设备证书","可确认"),("心跳重连","可恢复"),("离线缓存","可补传"),("失联告警","可追踪")]
        for i,(a,b) in enumerate(items):
            x=55+i*245;box(d,(x,230,x+220,470),20,(255,255,255,255),(210,221,214,255),2)
            box(d,(x+24,255,x+66,297),13,(76,230,158,255));tx(d,(x+45,276),f"{i+1}",11,(8,42,27),True,"mm")
            tx(d,(x+24,355),a,19,(13,20,16),True);tx(d,(x+24,394),b,13,(38,143,95),True)
    else:
        tx(d,(640,108),"NEXA MODULE",14,(35,128,88),True,"ma");tx(d,(640,250),"自然语言进入，",58,(13,20,16),True,"ma");tx(d,(640,332),"设备能力发生。",58,(38,151,101),True,"ma")
        box(d,(480,440,800,502),13,(9,39,28,255));tx(d,(640,471),"NATURAL LANGUAGE → ACTION",12,(255,255,255),True,"mm")
        tx(d,(640,585),"nexa module · agent-native device connectivity",11,(111,123,115),False,"ma")
    tx(d,(1210,682),f"{min(8,int(t/5.25)+1):02d} / 08",9,(118,129,121),True,"ra")
    p.stdin.write(im.tobytes())
p.stdin.close();p.wait();print(os.path.abspath(out),os.path.getsize(out))

