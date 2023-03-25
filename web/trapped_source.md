# Trapped Source (very easy)
This challenge will test if we can inspect source code of web pages.

Upon loading the website, we can inspect the source and find the following inline javascript:
```javascript
window.CONFIG = window.CONFIG || {
    buildNumber: "v20190816",
    debug: false,
    modelName: "Valencia",
    correctPin: "8291",
}
```

Entering the correct pin on the keypad will give us the flag
