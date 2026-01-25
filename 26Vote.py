import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyfiglet import figlet_format

# --- CONFIGURATION ---
MAX_THREADS_CHECKER = 200  # Jumlah thread buat ngecek proxy
MAX_THREADS_VOTER = 100    # Jumlah thread buat kirim vote
TIMEOUT = 5               # Detik nunggu respon proxy
# ---------------------

print(figlet_format("VOTE MULTI-THREAD", font="slant"))

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all"
]

live_proxies = []

def get_raw_proxies():
    raw_list = []
    print("[*] Mengambil data dari sumber proxy...")
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                raw_list.extend(r.text.strip().split('\n'))
        except:
            continue
    return list(set(raw_list))

def check_proxy(proxy):
    """Cek apakah proxy hidup dengan mencoba akses StrawPoll"""
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        # Kita tes lsg ke target biar yakin gak di-block
        r = requests.get("https://api.strawpoll.com/", proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            return proxy
    except:
        return None

def send_vote(proxy):
    url = "https://api.strawpoll.com/v3/polls/e7ZJarKMMg3/vote"
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    headers = {
        "x-csrf-token": "a49e2870a5dcbdb5a2b7d7cdf29dda9d7de0abdc", # Ganti jika expired
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
        res = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies, timeout=TIMEOUT)
        if res.status_code in [200, 201]:
            print(f"[VOTE SUCCESS] IP: {proxy}")
        else:
            print(f"[VOTE FAILED] Status: {res.status_code} | IP: {proxy}")
    except:
        pass

def main():
    raw_proxies = get_raw_proxies()
    print(f"[*] Total Proxy ditemukan: {len(raw_proxies)}")
    print(f"[*] Memulai validasi proxy (Threads: {MAX_THREADS_CHECKER})...")

    # --- BAGIAN CHECKER ---
    with ThreadPoolExecutor(max_workers=MAX_THREADS_CHECKER) as executor:
        futures = [executor.submit(check_proxy, p) for p in raw_proxies]
        for future in as_completed(futures):
            result = future.result()
            if result:
                live_proxies.append(result)
                print(f"[LIVE] {result}", end='\r')

    print(f"\n[+] Validasi selesai. Proxy Live: {len(live_proxies)}")

    if not live_proxies:
        print("[-] Tidak ada proxy yang bisa dipakai.")
        return

    # --- BAGIAN VOTER ---
    print(f"[*] Memulai Voting (Threads: {MAX_THREADS_VOTER})...")
    with ThreadPoolExecutor(max_workers=MAX_THREADS_VOTER) as executor:
        # Loop terus menggunakan proxy yang live
        while True:
            executor.map(send_vote, live_proxies)
            time.sleep(2) # Jeda antar batch biar VPS gak meledak

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Berhenti...")