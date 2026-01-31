import requests
from datetime import datetime, timezone
import hashlib
from Crypto.Cipher import ChaCha20
from pwn import *
import tqdm

class CustomCrc32:
    
    def __init__(self, polynomial, initial_value, final_xor, reflect_input, reflect_output):
        if polynomial == 0:
            raise ValueError("Polynomial cannot be zero")
        
        if initial_value < 0 or initial_value > 0xFFFFFFFF:
            raise ValueError("Initial value must be a 32-bit unsigned integer")
            
        if final_xor < 0 or final_xor > 0xFFFFFFFF:
            raise ValueError("Final XOR must be a 32-bit unsigned integer")
        
        self.polynomial = polynomial & 0xFFFFFFFF
        self.initial_value = initial_value & 0xFFFFFFFF
        self.final_xor = final_xor & 0xFFFFFFFF
        self.reflect_input = reflect_input
        self.reflect_output = reflect_output
        
        self.table = self._generate_table()
    
    def _generate_table(self):
        table = []
        
        for i in range(256):
            crc = i
            
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ self.polynomial
                else:
                    crc >>= 1
                crc &= 0xFFFFFFFF
            
            table.append(crc)
        
        return table
    
    def _reflect_byte(self, byte):
        result = 0
        for i in range(8):
            if byte & (1 << i):
                result |= 1 << (7 - i)
        return result
    
    def _reflect_u32(self, value):
        result = 0
        for i in range(32):
            if value & (1 << i):
                result |= 1 << (31 - i)
        return result & 0xFFFFFFFF
    
    def checksum(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        crc = self.initial_value
        
        for byte in data:
            if self.reflect_input:
                input_byte = self._reflect_byte(byte)
            else:
                input_byte = byte
            
            table_index = (crc ^ input_byte) & 0xFF
            crc = ((crc >> 8) ^ self.table[table_index]) & 0xFFFFFFFF
        
        if self.reflect_output:
            final_crc = self._reflect_u32(crc)
        else:
            final_crc = crc
        
        return (final_crc ^ self.final_xor) & 0xFFFFFFFF
    
    def checksum_two_strings(self, str1, ident, str2):
        concatenated = f"{str1}_{ident}_{str2}"
        return self.checksum(concatenated)
    
    @classmethod
    def custom_polynomial(cls, polynomial):
        return cls(polynomial, 0xFFFFFFFF, 0xFFFFFFFF, True, True)

def base64_decode(encoded_str: str, base64_alphabet: str) -> str:
    padding_count = encoded_str.count('=')
    encoded_str = encoded_str.rstrip('=')
    
    base64_reverse_map = {char: index for index, char in enumerate(base64_alphabet)}
    
    output = bytearray()

    for i in range(0, len(encoded_str), 4):
        char1 = base64_reverse_map.get(encoded_str[i], 0)
        char2 = base64_reverse_map.get(encoded_str[i + 1], 0)
        char3 = base64_reverse_map.get(encoded_str[i + 2], 0) if i + 2 < len(encoded_str) else 0
        char4 = base64_reverse_map.get(encoded_str[i + 3], 0) if i + 3 < len(encoded_str) else 0

        combined = (char1 << 18) | (char2 << 12) | (char3 << 6) | char4

        output.append((combined >> 16) & 0xFF)
        if i + 2 < len(encoded_str) or padding_count < 2:
            output.append((combined >> 8) & 0xFF)
        if i + 3 < len(encoded_str) or padding_count < 1:
            output.append(combined & 0xFF)

    return output

def get_key(seed):
	r = process(["./seed_brute/target/debug/seed_brute", str(seed)])
	out = bytes.fromhex(r.recvline().strip().decode())
	r.close()
	return out

context.log_level = 'error'

headers = {
	"Accept" : "application/vnd.github+json",
  	"Authorization" : "Bearer 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",
  	"X-GitHub-Api-Version" : "2022-11-28"
}

repo_name = "s3cr3t_b4db10c"
github_username = "inyourheap"

URL = f"https://api.github.com/repos/{github_username}/{repo_name}/issues/comments"

resp = requests.get(URL, headers = headers).json()
dt = datetime.strptime(resp[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
leaked_seed = int(dt.timestamp() - 5) * 10000 # diff

data = resp[0]['body'].split(", ")
hostname = data[0].split(": ")[-1]
os = data[1].split(": ")[-1]
username = data[2].split(": ")[-1]
ciphertext = data[3].split(": ")[-1]
print(hostname, username, ciphertext)
custom_crc = CustomCrc32.custom_polynomial(0xdeadb33f)

base64_alphabet = "KdauhQCHrjc9GyWAYgoU72x8kzVRlZ3BSN14vsieIptX6JTDPmEq5FOL0nMwfb+/"
ciphertext2 = base64_decode(ciphertext, base64_alphabet)

for i in range(len(ciphertext2)):
	crc32_out = custom_crc.checksum_two_strings(username, i + 0xcbc, repo_name)
	ciphertext2[i] = (crc32_out & 0xff) ^ ciphertext2[i]

print(leaked_seed, leaked_seed - 10000)
for i in tqdm.tqdm(range(leaked_seed, leaked_seed - 20000, -1)):
	key = get_key(i)
	nonce = hashlib.md5(hostname.encode()).digest()[:12]
	cipher = ChaCha20.new(key=key, nonce=nonce)
	pt = cipher.decrypt(ciphertext2)
	try:
		if b"CBC" in pt:
			print(pt)
	except Exception as e:
		continue
	
	