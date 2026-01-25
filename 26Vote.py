import requests
import json
import threading
import sys
from concurrent.futures import ThreadPoolExecutor
from pyfiglet import figlet_format

# --- CONFIGURATION ---
MAX_THREADS = 150  # Sesuaikan dengan kekuatan VPS-mu
TIMEOUT = 7        # Waktu tunggu tiap proxy
# ---------------------

# Counter Global
sukses = 0
gagal = 0
lock = threading.Lock()

print(figlet_format("VOTE BRUTE", font="slant"))

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all"
]

def get_proxies():
    raw_list = []
    print("[*] Sedang memanen proxy...")
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                raw_list.extend(r.text.strip().split('\n'))
        except:
            continue
    return list(set(raw_list))

def update_display():
    """Menampilkan counter yang terus bertambah di satu baris"""
    sys.stdout.write(f"\r[STATUS] Sukses: {sukses} | Gagal: {gagal} ")
    sys.stdout.flush()

def do_vote(proxy):
    global sukses, gagal
    url = "https://api.strawpoll.com/v3/polls/e7ZJarKMMg3/vote"
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    headers = {
        "x-csrf-token": "a49e2870a5dcbdb5a2b7d7cdf29dda9d7de0abdc",
        "user-agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "content-type": "text/plain;charset=UTF-8",
        "cookie": "session=eyJjb3VudHJ5X2NvZGUiOiJpZCIsImNzcmZfdG9rZW4iOiJhNDllMjg3MGE1ZGNiZGI1YTJiN2Q3Y2RmMjlkZGE5ZDdkZTBhYmRjIiwiZXhwaXJlcyI6MTgwMDkxNTg1NSwiaWQiOiI2NjBkMDdmMi1mYTNjLTExZjAtODk3OS1hZTI3OGJhZTk3OGYifQ----9d2b51a1a4beccf53a2fe3c711e517f6453aeb1c081e4b6b1508116558ab4a3d"
    }

    payload = {
        "pv": "08c0a6c2-f9f0-11f0-a644-f383aefb4ecc",
        "v": {
            "pollVotes": [{"id": "05ZdjXavmn6", "value": 1}],
            "voteType": "add",
            "isEmbed": False
        }
    }

    try:
        # Langsung tembak tanpa ba-bi-bu
        res = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies, timeout=TIMEOUT)
        
        with lock:
            if res.status_code in [200, 201]:
                sukses += 1
            else:
                gagal += 1
            update_display()
            
    except:
        with lock:
            gagal += 1
            update_display()

def main():
    proxy_list = get_proxies()
    total = len(proxy_list)
    print(f"[*] Total amunisi: {total} proxy.")
    print(f"[*] Menyerang dengan {MAX_THREADS} threads...\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(do_vote, proxy_list)

    print(f"\n\n[DONE] Selesai! Skor Akhir -> Sukses: {sukses}, Gagal: {gagal}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Dihentikan paksa oleh user.")
