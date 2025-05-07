key の長さを超えると、既に生成した暗号化文字列を次の鍵文字として再利用する

```py
cipher = "ayb wpg uujmz pwom jaaaaaa aa tsukuctf, hj vynj? mml ogyt re ozbiymvrosf bfq nvjwsum mbmm ef ntq gudwy fxdzyqyc, yeh sfypf usyv nl imy kcxbyl ecxvboap, epa 'avb' wxxw unyfnpzklrq."

letters = [c for c in cipher if c.islower()]

p = ['?'] * len(letters)
for j in range(8, len(letters)):
    Cj = ord(letters[j]) - ord('a')
    Cjm8 = ord(letters[j - 8]) - ord('a')
    pj = (Cj - Cjm8) % 26
    p[j] = chr(pj + ord('a'))

plaintext = list(cipher)
li = 0
for i, c in enumerate(plaintext):
    if c.islower():
        plaintext[i] = p[li]
        li += 1

result = ''.join(plaintext)
print(result)
```

`??? ??? ??joy this problem or tsukuctf, or both? the flag is concatenate the seventh word in the first sentence, the third word in the second sentence, and 'fun' with underscores.`

`TsukuCTF25{tsukuctf_is_fun}`
