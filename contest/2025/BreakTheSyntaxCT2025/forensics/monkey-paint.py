import re
import pickle
import pyshark

try:
    with open("d.pickle", "rb") as f:
        d = pickle.load(f)
except:
    capture = pyshark.FileCapture('monkey-paint.pcapng')

    d=[]
    for packet in capture:
        try:
            ds=packet.layers[1].usb_capdata
            d.append(ds)
        except:
            pass

    capture.close()

    with open('d.pickle', 'wb') as f:
        pickle.dump(d, f)

from PIL import Image

data = []
for rep in d:
    parts = rep.split(':')
    row = []
    for x in parts:
        v = int(x, 16)
        v = v - 256 if v >= 0x80 else v
        row.append(v)
    data.append(row)

picture = Image.new("RGB", (1200, 1200), "white")
pixels = picture.load()

INIT_X, INIT_Y = 600, 600
x, y = INIT_X, INIT_Y

for step, dt in enumerate(data):
    x += dt[1]
    y += dt[2]
    if dt[0] == 1 or dt[0] == 3:
        for i in range(-1, 1):
            for j in range(-1, 1):
                try:pixels[x + i , y + j] = (0, 0, 255, 50)
                except:pass
    if dt[0] == 2 or dt[0] == 3:
        try:pixels[x, y] = (0, 255, 0, 50)
        except: pass
    #if dt[0] == 0:
        #try:pixels[x, y] = (255, 0, 0, 200)
        #except:pass

picture.save("flag.png", "PNG")

# `BtSCTF{yeah_it_does!11!}`
