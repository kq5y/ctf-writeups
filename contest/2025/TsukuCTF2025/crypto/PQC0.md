openssl 3.5.0をインスコするところから

```py
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

enc = "5f2b9c04a67523dac3e0b0d17f79aa2879f91ad60ba8d822869ece010a7f78f349ab75794ff4cb08819d79c9f44467bd"
enc_b = bytes.fromhex(enc)

ciphertext = "83daaca5593e84b6b902645a25920e6f60c7c72ca8101b56b878434f20cd838f0f2086d3385e528f2687625a38822b74097d109f6d7b3ac730b7fd6a47c988324a6f3b3133b868d3db8b473b597151df4e4091e..."
ciphertext_b = bytes.fromhex(ciphertext)

with open("ciphertext.dat","wb") as f:
    f.write(ciphertext_b)

os.system("openssl pkeyutl -decap -inkey priv.pem -in ciphertext.dat -secret shared.dat")

with open("shared.dat", "rb") as f:
    shared_secret = f.read()

m=AES.new(shared_secret, AES.MODE_ECB)
res=m.decrypt(enc_b)
print(unpad(res, 16).decode())
```

`TsukuCTF25{W3lc0me_t0_PQC_w0r1d!!!}`
