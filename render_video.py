from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math,subprocess,imageio_ffmpeg,os,random
W,H,FPS,DURATION=1280,720,24,48
FB="C:/Windows/Fonts/msyhbd.ttc";FR="C:/Windows/Fonts/msyh.ttc"
def F(n,b=False):return ImageFont.truetype(FB if b else FR,n)
def tx(d,p,s,n,c,b=False,a=None):d.text(p,s,font=F(n,b),fill=c,anchor=a)
def box(d,b,r,c,o=None,w=1):d.rounded_rectangle(b,r,fill=c,outline=o,width=w)
def E(x):x=max(0,min(1,x));return x*x*(3-2*x)
def bg(dark=False):
 im=Image.new("RGB",(W,H),(6,14,10) if dark else (243,246,242));d=ImageDraw.Draw(im,"RGBA")
 col=(89,235,164,13) if dark else (20,70,45,10)
 for x in range(0,W,64):d.line((x,0,x,H),fill=col)
 for y in range(0,H,64):d.line((0,y,W,y),fill=col)
 return im,d
def glow(im,x,y,r,c=(72,229,157)):
 lay=Image.new("RGBA",(W,H));q=ImageDraw.Draw(lay);q.ellipse((x-r,y-r,x+r,y+r),fill=(*c,85));lay=lay.filter(ImageFilter.GaussianBlur(r//2));im.paste(lay,(0,0),lay)
def chip(d,x,y,s=1,rot=0):
 box(d,(x-105*s,y-138*s,x+105*s,y+138*s),30*s,(8,31,21,255),(60,106,82,255),3)
 box(d,(x-88*s,y-121*s,x+88*s,y+121*s),22*s,(14,49,34,255),(55,103,78,255),2)
 box(d,(x-61*s,y-62*s,x+61*s,y+60*s),25*s,(116,239,169,255))
 tx(d,(x,y-8*s),"NEXA",int(29*s),(7,36,23),True,"mm");tx(d,(x,y+28*s),"AGENT MODULE",int(7*s),(7,36,23),True,"mm")
 for i in range(5):box(d,(x-40*s+i*20*s,y+103*s,x-32*s+i*20*s,y+120*s),4*s,(73,103,87,255))
def bubble(d,x,y,w,s,accent=False):
 box(d,(x,y,x+w,y+58),14,(202,255,101,255) if accent else (255,255,255,245),None)
 tx(d,(x+18,y+21),"NATURAL LANGUAGE",7,(34,129,87),True);tx(d,(x+18,y+43),s,11,(16,28,21),True)
def factory(d,x,y,s=1):
 d.rectangle((x,y+80*s,x+220*s,y+190*s),fill=(17,54,39));d.polygon([(x,y+80*s),(x+65*s,y+40*s),(x+65*s,y+80*s),(x+130*s,y+40*s),(x+130*s,y+80*s)],fill=(26,88,61))
 d.rectangle((x+175*s,y,x+205*s,y+80*s),fill=(32,117,78))
 for i in range(4):d.rectangle((x+22*s+i*47*s,y+120*s,x+48*s+i*47*s,y+150*s),fill=(112,239,170))
def building(d,x,y,s=1):
 box(d,(x,y,x+180*s,y+210*s),10,(18,58,42))
 for r in range(4):
  for c in range(3):box(d,(x+24*s+c*48*s,y+25*s+r*42*s,x+50*s+c*48*s,y+48*s+r*42*s),3,(202,255,101) if (r+c)%3==0 else (68,130,99))
def greenhouse(d,x,y,s=1):
 d.arc((x,y,x+220*s,y+190*s),180,360,fill=(37,139,94),width=max(2,int(5*s)));d.line((x,y+95*s,x+220*s,y+95*s),fill=(37,139,94),width=4)
 for i in range(4):
  xx=x+35*s+i*48*s;d.line((xx,y+165*s,xx,y+115*s),fill=(26,112,72),width=4);d.ellipse((xx-15*s,y+120*s,xx+2*s,y+138*s),fill=(75,224,150))
def truck(d,x,y,s=1):
 box(d,(x,y+60*s,x+150*s,y+145*s),12,(15,55,39));box(d,(x+150*s,y+85*s,x+225*s,y+145*s),10,(35,137,91))
 for xx in (x+48*s,x+180*s):d.ellipse((xx-18*s,y+128*s,xx+18*s,y+164*s),fill=(7,20,13));d.ellipse((xx-8*s,y+138*s,xx+8*s,y+154*s),fill=(101,239,171))
def server(d,x,y,s=1):
 box(d,(x,y,x+210*s,y+260*s),22,(11,43,30),(49,102,76),2)
 for i in range(4):box(d,(x+28*s,y+56*s+i*42*s,x+182*s,y+80*s+i*42*s),7,(31,77,56));d.ellipse((x+150*s,y+64*s+i*42*s,x+160*s,y+74*s+i*42*s),fill=(98,240,171))
def packets(d,a,b,t,count=5,c=(91,239,168)):
 for i in range(count):
  u=(t*.55+i/count)%1;x=a[0]+(b[0]-a[0])*u;y=a[1]+(b[1]-a[1])*u;d.ellipse((x-6,y-6,x+6,y+6),fill=(*c,255))
def fade(d,t,a,b):
 alpha=int(255*max(1-E((t-a)/.35),1-E((b-t)/.35)))
 if alpha>0:d.rectangle((0,0,W,H),fill=(5,13,9,alpha))
ff=imageio_ffmpeg.get_ffmpeg_exe();out="nexa-module-intro.mp4"
p=subprocess.Popen([ff,"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
scenes=[(0,6),(6,13),(13,19),(19,26),(26,33),(33,39),(39,44),(44,48)]
for n in range(FPS*DURATION):
 t=n/FPS
 if t<6:
  im,d=bg(True);u=E(t/5);glow(im,930,350,250);d=ImageDraw.Draw(im,"RGBA")
  # animated assembly rings
  for k in range(3):
   r=150+k*55+10*math.sin(t*1.4+k);d.ellipse((930-r,350-r,930+r,350+r),outline=(95,240,170,35),width=2)
  chip(d,930,350,.95);bubble(d,100,360,350,"“启动生产线巡检”",True)
  tx(d,(100,100),"NEXA MODULE",12,(104,241,173),True);tx(d,(100,168),"让设备理解意图，",52,(255,255,255),True);tx(d,(100,235),"让能力直接发生。",52,(79,231,158),True)
  tx(d,(102,475),"场景驱动 · 意图匹配 · 端侧执行 · 业务直连",15,(142,163,151))
 elif t<13:
  im,d=bg(False);u=(t-6)/7
  tx(d,(640,58),"自然语言进入真实设备场景",36,(12,22,16),True,"ma")
  items=[(factory,"工业控制","启动产线巡检"),(building,"楼宇园区","关闭会议室空调"),(greenhouse,"智慧农业","湿度低时自动灌溉"),(truck,"移动终端","上报位置和设备状态")]
  for i,(fn,title,line) in enumerate(items):
   x=40+i*310;y=170+12*math.sin(u*5+i)
   box(d,(x,y,x+285,y+410),22,(255,255,255),(211,221,214),2);fn(d,x+35,y+35,.85)
   tx(d,(x+25,y+270),title,20,(12,22,16),True);bubble(d,x+20,y+310,245,line,i==0)
   # active pulse
   if int(u*8)%4==i:d.ellipse((x+235,y+24,x+263,y+52),fill=(81,233,160,255))
 elif t<19:
  im,d=bg(True);u=(t-13)/6;glow(im,640,360,180);d=ImageDraw.Draw(im,"RGBA")
  chip(d,640,365,.72)
  inputs=[("本地文字",(110,170)),("UART 串口",(110,500)),("语音转写",(980,170)),("远程控制",(980,500))]
  for label,(x,y) in inputs:
   box(d,(x,y,x+190,y+72),15,(245,250,247,245));tx(d,(x+95,y+28),label,14,(13,32,21),True,"mm");tx(d,(x+95,y+52),"NATURAL INPUT",7,(36,139,93),True,"mm")
   target=(535,365) if x<640 else (745,365);d.line((x+190 if x<640 else x,y+36,*target),fill=(75,222,151,90),width=2);packets(d,(x+190 if x<640 else x,y+36),target,u+i*.11,3)
  tx(d,(640,70),"多源输入，在设备端统一",36,(255,255,255),True,"ma");tx(d,(640,650),"Natural Language Object",12,(97,235,166),True,"ma")
 elif t<26:
  im,d=bg(False);u=(t-19)/7;tx(d,(640,55),"设备上下文，通过加密链路流向 AI",36,(12,22,16),True,"ma")
  chip(d,210,360,.62);server(d,975,235,.9)
  tx(d,(1070,180),"AI INTENT SERVER",10,(35,136,91),True,"mm")
  d.line((350,360,940,360),fill=(49,150,101),width=3);packets(d,(350,360),(940,360),u,7)
  # orbiting data tokens
  labels=[("INPUT","自然语言"),("SKILLS","能力清单"),("STATE","设备状态"),("IPv6","固定地址")]
  for i,(a,b) in enumerate(labels):
   x=420+i*125;y=235+18*math.sin(t*2+i);box(d,(x,y,x+105,y+72),12,(255,255,255),(202,216,207),2);tx(d,(x+52,y+25),a,8,(38,142,95),True,"mm");tx(d,(x+52,y+49),b,10,(31,45,36),True,"mm")
  tx(d,(645,410),"TCP + TLS",12,(31,122,81),True,"ma")
 elif t<33:
  im,d=bg(True);u=(t-26)/7;tx(d,(640,52),"AI 匹配 Skill，设备完成可信执行",36,(255,255,255),True,"ma")
  # cloud brain nodes
  box(d,(80,180,370,540),22,(16,50,37),(45,98,72),2);tx(d,(225,225),"AI 意图匹配",20,(107,241,174),True,"mm")
  nodes=[("识别目标",150,300),("抽取参数",280,300),("匹配 Skill",215,400)]
  for label,x,y in nodes:d.ellipse((x-42,y-42,x+42,y+42),fill=(34,104,72));tx(d,(x,y),label,10,(255,255,255),True,"mm")
  d.line((150,300,215,400),fill=(99,237,170),width=2);d.line((280,300,215,400),fill=(99,237,170),width=2)
  # plan flying
  x=410+220*((math.sin(u*math.pi)+1)/2);box(d,(x,325,x+125,385),12,(202,255,101));tx(d,(x+62,355),"SKILL PLAN",10,(10,42,27),True,"mm")
  chip(d,735,355,.55)
  # fan execution
  cx,cy=1040,355;box(d,(900,180,1190,540),22,(244,249,246),(67,111,87),2);tx(d,(1045,225),"本地执行",20,(16,38,24),True,"mm")
  for k in range(4):
   ang=t*5+k*math.pi/2;ex=cx+75*math.cos(ang);ey=cy+75*math.sin(ang);d.ellipse((ex-22,ey-10,ex+22,ey+10),fill=(55,187,123))
  d.ellipse((cx-18,cy-18,cx+18,cy+18),fill=(12,55,37));tx(d,(1045,485),"fan.control · ON",11,(36,139,92),True,"mm")
 elif t<39:
  im,d=bg(False);u=(t-33)/6;tx(d,(640,55),"结果直达应用服务器",36,(12,22,16),True,"ma")
  chip(d,240,350,.66);server(d,985,220,.9)
  # dual route arcs
  d.arc((300,145,1050,565),190,350,fill=(44,157,104),width=3);packets(d,(375,350),(960,350),u,8)
  # dashboard
  box(d,(500,205,790,500),20,(255,255,255),(205,217,209),2);tx(d,(645,245),"EXECUTION RESULT",9,(35,138,92),True,"mm")
  rows=[("status","completed"),("fan_2","ON"),("auto_off","900 sec"),("device","online")]
  for i,(a,b) in enumerate(rows):tx(d,(535,310+i*45),a,10,(98,110,102));tx(d,(740,310+i*45),b,11,(27,83,54),True,"ra")
  tx(d,(640,620),"固定 IPv6 · TCP + TLS · 不经过 IoT 业务中转节点",12,(45,132,88),True,"ma")
 elif t<44:
  im,d=bg(True);u=(t-39)/5;tx(d,(640,55),"双产品形态，连接与恢复能力同步在线",34,(255,255,255),True,"ma")
  for i,(name,net) in enumerate([("Nexa Module Flex","4G · Wi‑Fi · BLE"),("Nexa Module 4G","Pure 4G")]):
   x=70+i*610;box(d,(x,155,x+540,555),24,(13,44,32),(48,98,73),2);chip(d,x+150,355,.58);tx(d,(x+285,260),name,24,(255,255,255),True);tx(d,(x+285,305),net,13,(103,238,171),True)
   for j,label in enumerate(["IPv6","HEARTBEAT","RECONNECT"]):box(d,(x+285,y:=350+j*50,x+475,y+34),9,(28,75,53));tx(d,(x+380,y+17),label,8,(179,212,193),True,"mm")
  # link switch pulse
  if int(u*8)%2==0:d.ellipse((566,338,586,358),fill=(202,255,101))
 else:
  im,d=bg(True);u=(t-44)/4;glow(im,640,330,250);d=ImageDraw.Draw(im,"RGBA")
  tx(d,(640,105),"NEXA MODULE",13,(104,241,173),True,"ma");tx(d,(640,235),"自然语言进入，",58,(255,255,255),True,"ma");tx(d,(640,318),"设备能力发生。",58,(77,232,158),True,"ma")
  box(d,(475,430,805,493),13,(202,255,101));tx(d,(640,461),"NATURAL LANGUAGE → ACTION",11,(8,35,23),True,"mm")
  tx(d,(640,585),"Agent-native connectivity for every device",11,(121,145,132),False,"ma")
 # cinematic fade
 for a,b in scenes:
  if a<=t<b:fade(d,t,a,b);break
 p.stdin.write(im.tobytes())
p.stdin.close();p.wait();print(os.path.abspath(out),os.path.getsize(out))

