
import string

hex_encoded = "1f7c3f1c137a551e09170e4c0626173f00110c000a5a00540227780b0f3639400b5716394c3d151e"
xored_bytes = bytes.fromhex(hex_encoded)

known_prefix = "THM{"
prefix_bytes = known_prefix.encode()

# İlk 4 karakterden key'in 4 byte'ını bul
key = [0]*5
for i in range(4):
    key[i] = xored_bytes[i] ^ prefix_bytes[i]

# 5. karakteri brute-force ile dene
for c in string.ascii_letters + string.digits:
    key[4] = ord(c)
    
    # Key tekrarlayarak flag1’i çöz
    flag_bytes = bytearray()
    for i in range(len(xored_bytes)):
        flag_bytes.append(xored_bytes[i] ^ key[i%5])
    
    flag_str = flag_bytes.decode(errors='ignore')
    
    if flag_str.startswith("THM{") and flag_str.endswith("}"):
        print("Possible key:", ''.join(chr(k) for k in key))
        print("Flag1:", flag_str)
