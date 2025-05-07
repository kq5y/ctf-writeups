```js
  const sanitized = str.replaceAll(" ", "");
  if (sanitized.length < 10) {
    return `error: no flag for you. sanitized string is ${sanitized}, length is ${sanitized.length.toString()}`;
  }
  const array = JSON.parse(sanitized);
  if (array.length < 0) {
    // hmm...??
    return FLAG;
  }
```

`curl -X POST -d 'array={"length":-1}' http://challs.tsukuctf.org:28888`で:ok:

`TsukuCTF25{l4n_l1n_lun_l4n_l0n}`
