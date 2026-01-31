from Crypto.Util.number import *

N_ROUNDS = 10

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

def expand_key(master_key):
    """
    Expands and returns a list of key matrices for the given master_key.
    """

    # Round constants https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants
    r_con = (
        0, 64, 198, 239, 128, 16, 27, 212, 57, 77, 108, 125, 94, 54, 216, 47, 32, 2, 171, 53, 4, 8, 1, 99, 197, 106, 188, 151, 179, 145, 250, 154
    )

    # Initialize round keys with raw key material.
    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4

    # Each iteration has exactly as many columns as the key material.
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        # Copy previous word.
        word = list(key_columns[-1])

        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift.
            word.append(word.pop(0))
            # Map to S-BOX.
            word = [s_box[b] for b in word]
            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            # Run word through S-box in the fourth iteration when using a
            # 256-bit key.
            word = [s_box[b] for b in word]

        # XOR with equivalent word from previous iteration.
        word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)

    # Group key words in 4x4 byte matrices.
    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return b''.join(bytes([a]) for row in matrix for a in row)

def add_round_key(s, k):
    return [[s[i][j]^k[i][j] for j in range(4)] for i in range(4)]

def inv_shift_rows(s):
    s[1][1], s[2][1], s[3][1], s[0][1] = s[0][1], s[1][1], s[2][1], s[3][1]
    s[2][2], s[3][2], s[0][2], s[1][2] = s[0][2], s[1][2], s[2][2], s[3][2]
    s[3][3], s[0][3], s[1][3], s[2][3] = s[0][3], s[1][3], s[2][3], s[3][3]

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns(s)

def sub_bytes(s, sbox=s_box):
    return [[int(sbox[a]) for a in row] for row in s]

def decrypt(key, ciphertext):
    round_keys = expand_key(key)
    
    state = bytes2matrix(ciphertext)
    
    state = add_round_key(state, round_keys[0])
    
    for i in range(N_ROUNDS, 0, -1):
        state = add_round_key(state, round_keys[i])
        inv_mix_columns(state)
        inv_shift_rows(state)
        state = sub_bytes(state, sbox=inv_s_box)
    
    state = add_round_key(state, round_keys[0])
    
    plaintext = matrix2bytes(state)
    return plaintext

def encrypt(key, plaintext):
    round_keys = expand_key(key)
    
    state = bytes2matrix(plaintext)
    
    state = add_round_key(state, round_keys[0])
    
    for i in range(1, N_ROUNDS + 1):
        state = sub_bytes(state, sbox=s_box)
        shift_rows(state)                   
        mix_columns(state)                  
        state = add_round_key(state, round_keys[i])
    
    state = add_round_key(state, round_keys[0])
    
    ciphertext = matrix2bytes(state)
    return ciphertext

ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def conv(inp):
	v11 = inp
	v12 = ror(inp, 7, 32)
	v11 ^= v12
	v13 = ror(inp, 15, 32)
	v11 ^= v13
	v14 = ror(inp, 21, 32)
	v11 ^= v14
	v15 = ror(inp, 3, 32)
	v11 ^= v15
	v16 = ror(inp, 19, 32)
	v11 ^= v16
	return v11

def func_1(x):
    r = 0
    for i in range(0, 32, 8):
        r |= sbox[(x >> i) & 0xff] << i
    return r

def func_2(inp):
	tmp = func_1(inp)
	return conv(tmp)

flagg = b""
sbox = [231, 111, 249, 56, 63, 138, 216, 95, 106, 218, 192, 108, 112, 122, 171, 4, 207, 43, 137, 155, 83, 252, 32, 60, 205, 5, 44, 78, 133, 225, 29, 245, 42, 34, 47, 185, 173, 113, 199, 219, 70, 149, 40, 250, 98, 66, 68, 187, 36, 107, 194, 193, 97, 57, 247, 166, 55, 99, 143, 177, 0, 164, 181, 159, 21, 235, 89, 132, 184, 215, 73, 201, 71, 244, 17, 145, 59, 204, 128, 119, 52, 20, 163, 116, 238, 37, 131, 153, 48, 62, 65, 61, 168, 167, 136, 196, 209, 144, 82, 161, 240, 222, 241, 87, 142, 162, 75, 49, 233, 96, 150, 23, 237, 27, 121, 169, 115, 118, 12, 25, 93, 46, 226, 125, 109, 243, 230, 251, 94, 45, 11, 7, 157, 248, 134, 170, 254, 35, 8, 74, 58, 221, 232, 104, 86, 91, 81, 3, 39, 22, 64, 197, 13, 126, 158, 80, 213, 160, 18, 239, 103, 191, 77, 117, 102, 183, 203, 31, 30, 26, 217, 130, 114, 140, 85, 28, 67, 156, 139, 174, 172, 53, 1, 180, 19, 54, 6, 208, 220, 229, 9, 15, 129, 92, 79, 227, 100, 33, 176, 198, 110, 76, 101, 152, 141, 2, 224, 38, 195, 200, 88, 84, 151, 51, 228, 146, 186, 154, 50, 72, 223, 189, 124, 242, 210, 175, 135, 236, 123, 178, 14, 69, 148, 16, 214, 90, 10, 190, 188, 120, 182, 147, 127, 246, 255, 41, 212, 211, 253, 165, 234, 24, 105, 206, 202, 179]
static_buf =  [4117152022, 249169712, 2337874715, 2493289063, 192746926, 2123354537, 587869043, 82996534, 4193785999, 3279033102, 4064299809, 79675858, 3039174743, 3201296038, 1302647935, 2884253364, 2599066875, 2983860211, 654684473, 3940014023, 3170974465, 3877616887, 4047936464, 1621268348, 443542672, 2292178319, 3712799943, 604158684, 2737657835, 1219219026, 1761140900, 2544355926]

ct = bytes.fromhex("2a4c85cc2107f9aaa0c093c7a3afb07b9cc1d7d2a7b022a25fd8ccd6cfa9770d68670c568e193135440f15ca7e16c952")
real_ct = []
for i in range(0, len(ct), 4):
	real_ct.append(bytes_to_long(ct[i:i+4][::-1]))

ct2 = []
for x in range(0, len(real_ct), 4):
	
	ct = real_ct[x:x+4]	

	for i in range(32):
		tmp = ct[0]^ct[1]^ct[2]^static_buf[len(static_buf) - 1 - i]
		ct.insert(0, func_2(tmp) ^ ct[3])
	
	found = b""
	
	for i in range(4):
		found += long_to_bytes(ct[i])[::-1]
	if(x % 4 == 0):
		ct2.append(found)

flag = b""
key = bytes([74, 47, 201, 176, 33, 68, 106, 236, 243, 66, 64, 123, 113, 21, 131, 206])
for i in range(len(ct2)):
	flag += decrypt(key, ct2[i])
print(flag)

