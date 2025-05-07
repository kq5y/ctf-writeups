SEED: http://challs.tsukuctf.org:50000/static/seed.txt

1,2,3,8,9,10のそれぞれのdigits(7個)は表示されるのでそれを下に疑似乱数を再現し、残りの部分を出す 

```python
import json
import base64
import hmac
import hashlib

s_cookie = input('session: ')
decoded_s = base64.b64decode(s_cookie).decode('utf-8','ignore').split('}')[0]+'}'
session_id = json.loads(decoded_s)["session_id"]

SEED = bytes.fromhex('b7c4c422a93fdc991075b22b79aa12bb19770b1c9b741dd44acbafd4bc6d1aabc1b9378f3b68ac345535673fcf07f089a8492dc1b05343a80b3d002f070771c6')
DIGITS_PER_ROUND = 7
TOTAL_ROUNDS = 10

def lcg_params(seed: bytes, session_id: str):
    m = 2147483693
    raw_a = hmac.new(seed, (session_id + "a").encode(), hashlib.sha256).digest()
    a = (int.from_bytes(raw_a[:8], 'big') % (m - 1)) + 1
    raw_c = hmac.new(seed, (session_id + "c").encode(), hashlib.sha256).digest()
    c = (int.from_bytes(raw_c[:8], 'big') % (m - 1)) + 1
    return m, a, c

def generate_round_digits(seed: bytes, session_id: str, round_index: int):
    LCG_M, LCG_A, LCG_C = lcg_params(seed, session_id)

    h0 = hmac.new(seed, session_id.encode(), hashlib.sha256).digest()
    state = int.from_bytes(h0, 'big') % LCG_M

    for _ in range(DIGITS_PER_ROUND * round_index):
        state = (LCG_A * state + LCG_C) % LCG_M

    digits = []
    for _ in range(DIGITS_PER_ROUND):
        state = (LCG_A * state + LCG_C) % LCG_M
        digits.append(state % 10)

    return digits

correct_sum = 0
for round_index in range(TOTAL_ROUNDS):
    digits = generate_round_digits(SEED, session_id, round_index)
    number = int(''.join(map(str, digits)))
    correct_sum += number

print(correct_sum)
```

flaskのsessionのcookieを無理やりbase64でdecodeできるからsession_id獲得、これで未知の値はないため答えを生成

`TsukuCTF25{Tr4d1on4l_P4th_Trav3rs4l}`
