#!/usr/bin/env python3
"""Draws the Pulse Lanes app icons. usage: python3 build/icons.py OPTION OUTDIR   (OPTION a|b|c; 'sheet' draws all three side by side)"""
import sys,os
from PIL import Image,ImageDraw,ImageFilter
S=1024
def bg(top,bot):
    im=Image.new('RGB',(S,S));d=ImageDraw.Draw(im)
    for y in range(S):
        t=y/(S-1);d.line([(0,y),(S,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    return im
def glow(im,box,col,r,blur):
    g=Image.new('RGBA',(S,S),(0,0,0,0));ImageDraw.Draw(g).rounded_rectangle(box,r,fill=col+(255,))
    g=g.filter(ImageFilter.GaussianBlur(blur));im.paste(g,(0,0),g)
def opt_a():   # three rising bars, the logo on the main screen
    im=bg((44,30,82),(14,10,26)).convert('RGBA')
    cols=[(255,107,90),(255,194,61),(79,140,255)];hs=[0.46,0.72,0.58];w=170;gap=60;x0=(S-3*w-2*gap)//2;base=800
    for i,(c,h) in enumerate(zip(cols,hs)):
        x=x0+i*(w+gap);top=int(base-h*S);glow(im,(x,top,x+w,base),c,85,40)
        ImageDraw.Draw(im).rounded_rectangle((x,top,x+w,base),85,fill=c+(255,))
    return im
def opt_b():   # a black stone with a glowing dash on a white lane, purple stage
    im=bg((120,70,230),(30,14,70)).convert('RGBA');d=ImageDraw.Draw(im)
    d.rounded_rectangle((300,-40,724,S+40),40,fill=(238,241,246,255))
    d.rounded_rectangle((330,700,694,860),26,outline=(150,110,240,255),width=16,fill=(255,255,255,255))
    d.rounded_rectangle((330,330,694,560),40,fill=(18,19,24,255))
    glow(im,(400,430,624,462),(255,255,255),16,14);d.rounded_rectangle((400,430,624,462),16,fill=(255,255,255,255))
    return im
def opt_c():   # three lanes with falling notes in the three colours
    im=bg((20,15,34),(8,6,14)).convert('RGBA');d=ImageDraw.Draw(im)
    cols=[(255,107,90),(255,194,61),(79,140,255)];lw=250;x0=(S-3*lw)//2
    for i in range(3):d.rectangle((x0+i*lw,0,x0+(i+1)*lw,S),fill=(30,23,49,255) if i==1 else (25,19,41,255))
    d.rectangle((x0,770,x0+3*lw,782),fill=(244,239,252,255))
    for i,y in [(0,330),(1,560),(2,170),(2,690)]:
        c=cols[i];glow(im,(x0+i*lw+30,y,x0+(i+1)*lw-30,y+90),c,45,22);d.rounded_rectangle((x0+i*lw+30,y,x0+(i+1)*lw-30,y+90),45,fill=c+(255,))
    return im
OPTS={'a':opt_a,'b':opt_b,'c':opt_c}
which,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True)
if which=='sheet':
    sheet=Image.new('RGB',(3*360+80,440),(245,245,248));d=ImageDraw.Draw(sheet)
    for i,k in enumerate('abc'):
        ic=OPTS[k]().convert('RGB').resize((320,320),Image.LANCZOS);m=Image.new('L',(320,320),0);ImageDraw.Draw(m).rounded_rectangle((0,0,319,319),72,fill=255)
        sheet.paste(ic,(40+i*360,40),m);d.text((40+i*360+150,385),'ABC'[i],fill=(30,30,40))
    sheet.save(os.path.join(out,'icon-options.png'))
else:
    ic=OPTS[which]().convert('RGB')
    for sz in (180,192,512):ic.resize((sz,sz),Image.LANCZOS).save(os.path.join(out,f'pulse-lanes-{sz}.png'))
