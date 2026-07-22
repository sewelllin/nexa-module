import numpy as np,wave,subprocess,imageio_ffmpeg,os
SR=48000;D=48;N=SR*D;music=np.zeros((N,2),dtype=np.float64)
tempo=96;beat=60/tempo
chords=[[130.81,164.81,196.00,246.94],[110.00,130.81,164.81,220.00],[87.31,130.81,174.61,220.00],[98.00,146.83,196.00,220.00]]
# soft evolving pads
for ci,start in enumerate(np.arange(0,D,beat*4)):
    dur=beat*4.6;i0=int(start*SR);i1=min(N,int((start+dur)*SR));tt=np.arange(i1-i0)/SR
    env=np.minimum(1,tt/.45)*np.minimum(1,(dur-tt)/.7);ch=chords[ci%4]
    for j,fr in enumerate(ch):
        tone=np.sin(2*np.pi*fr*tt)+.18*np.sin(2*np.pi*fr*2*tt)
        pan=.25+.5*(j/(len(ch)-1));music[i0:i1,0]+=tone*env*(1-pan)*.065;music[i0:i1,1]+=tone*env*pan*.065
# melodic glass plucks, no high-frequency noise
scale=[261.63,329.63,392.00,493.88,440.00,392.00,329.63,293.66]
for k,start in enumerate(np.arange(0,D,beat/2)):
    if k%4 in (0,2,3):
        fr=scale[k%len(scale)];dur=.42;i0=int(start*SR);i1=min(N,i0+int(dur*SR));tt=np.arange(i1-i0)/SR
        env=np.exp(-tt*8)*(1-np.exp(-tt*80));tone=np.sin(2*np.pi*fr*tt)+.22*np.sin(2*np.pi*fr*2*tt)
        pan=.35+.3*((k%8)/7);music[i0:i1,0]+=tone*env*(1-pan)*.13;music[i0:i1,1]+=tone*env*pan*.13
# restrained kick and low pulse
for k,start in enumerate(np.arange(0,D,beat)):
    dur=.22;i0=int(start*SR);i1=min(N,i0+int(dur*SR));tt=np.arange(i1-i0)/SR
    freq=72-22*(tt/dur);phase=2*np.pi*np.cumsum(freq)/SR;kick=np.sin(phase)*np.exp(-tt*18)*.22
    music[i0:i1,0]+=kick;music[i0:i1,1]+=kick
# gentle stereo echo
delay=int(.19*SR);music[delay:,0]+=music[:-delay,1]*.10;music[delay:,1]+=music[:-delay,0]*.10
# fade and normalize safely
fade=int(1.3*SR);music[:fade]*=np.linspace(0,1,fade)[:,None];music[-fade:]*=np.linspace(1,0,fade)[:,None]
music/=max(1,np.max(np.abs(music))/.72)
pcm=(music*32767).astype(np.int16)
wav="nexa-bg-music.wav"
with wave.open(wav,"wb") as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
ff=imageio_ffmpeg.get_ffmpeg_exe();tmp="nexa-module-premium.mp4"
cmd=[ff,"-y","-i","nexa-module-intro.mp4","-i",wav,"-filter_complex","[0:a]volume=1.0,pan=stereo|c0=c0|c1=c0[voice];[1:a]volume=0.20,lowpass=f=5200[music];[voice][music]amix=inputs=2:duration=first:dropout_transition=0,alimiter=limit=0.82:attack=8:release=100[a]","-map","0:v:0","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-t","48","-movflags","+faststart",tmp]
subprocess.check_call(cmd);os.replace(tmp,"nexa-module-intro.mp4");os.remove(wav)
print("Original background music mixed under narration")
