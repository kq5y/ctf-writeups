import re
import pyshark

capture = pyshark.FileCapture('monkey-see.pcapng', display_filter='usb.src == 1.9.1 && usb')

hid_usage_table = {
    0x00: '',
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e',
    0x09: 'f', 0x0A: 'g', 0x0B: 'h', 0x0C: 'i', 0x0D: 'j',
    0x0E: 'k', 0x0F: 'l', 0x10: 'm', 0x11: 'n', 0x12: 'o',
    0x13: 'p', 0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't',
    0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x', 0x1C: 'y', 0x1D: 'z',
    0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4', 0x22: '5',
    0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n',  # Enter
    0x2C: ' ',   # Space
    0x2D: '-',  # -
    0x2E: '=',  # =
    0x2F: '[',  # [
    0x30: ']',  # ]
    0x38: '/'
}

UPPER_MAP = {
    '-': '_',
    '[': '{',
    ']': '}',
    '1': '!',
    '2': '@',
    '3': '#',
    '/': '?'
}

# 復元された文字列
reconstructed_input = []
s = ""
for packet in capture:
    try:
        m=int(packet.layers[1].usbhid_data.split(":")[1],16)
        nsn=int(packet.layers[1].usbhid_data_array.split(":")[0],16)
        ns=''
        if nsn in hid_usage_table:
            ns=hid_usage_table[nsn]
        if nsn == 0x2a:
            s=s[:-1]
            continue
        if m == 2:
            if ns != ns.upper():
                ns=ns.upper()
            #else:
            #    print(packet.number)
            #    print("ns",f"+{ns}+")
            if ns in UPPER_MAP:
                ns = UPPER_MAP[ns]
        #elif m != 0:
        #    print("m",m)
        s+=ns
    except:
        pass

capture.close()

print(s)

match = re.search(r'BtSCTF\{.*?\}', s)
print(match.group())

# `BtSCTF{m0nk3y_tYpE!!1!!oneone!}`
