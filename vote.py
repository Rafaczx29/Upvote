import requests
import threading
import time
import os
import re
from pyfiglet import figlet_format
from tqdm import tqdm

# ANSI warna
GREEN, RED, YELLOW, CYAN, MAGENTA, RESET = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[95m', '\033[0m'

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=https",
    "https://www.proxyscan.io/download?type=socks4",
    "https://www.proxyscan.io/download?type=socks5",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/all.txt",
    "https://spys.me/proxy.txt",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
]

vote_success_count = 0
success_lock = threading.Lock()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def fetch_proxies():
    proxies = set()
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                if 'geonode' in url:
                    data = r.json()
                    for item in data.get('data', []):
                        proxies.add(f"{item.get('ip')}:{item.get('port')}")
                else:
                    # Mencari pola IP:Port pakai Regex biar lebih akurat
                    found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
                    proxies.update(found)
        except: continue
    return list(proxies)

def vote(proxy, path, pbar, target):
    global vote_success_count
    url = "https://commento.shngm.io/api/article?lang=en"
    
    # Deteksi jenis proxy (nyoba HTTP dulu karena list-nya campur)
    # Catatan: pastikan sudah pip install requests[socks]
    proxy_config = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    headers = {
        "Host": "commento.shngm.io",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://shinigami.asia",
        "Referer": f"https://shinigami.asia/{path}",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    payload = {"path": path, "type": "reaction0"}

    try:
        # Timeout diperkecil biar nggak ngegantung di proxy mati
        resp = requests.post(url, headers=headers, json=payload, proxies=proxy_config, timeout=7)
        if resp.status_code == 200:
            with success_lock:
                if vote_success_count < target:
                    vote_success_count += 1
                    pbar.update(1)
    except:
        pass

def worker(path, proxies, pbar, target):
    while vote_success_count < target and proxies:
        try:
            proxy = proxies.pop()
        except IndexError:
            break
        vote(proxy, path, pbar, target)

def main():
    clear_screen()
    print(f"{GREEN}{figlet_format('Auto Vote', font='slant')}{RESET}")
    print(f"{CYAN}Dibuat oleh {MAGENTA}@Rafaczx{CYAN} | Optimized by Gemini{RESET}\n")

    print(f"{YELLOW}[?]{RESET} Input Link/Path: ", end="")
    raw_path = input().strip()
    
    # --- LOGIKA AUTO CLEAN ---
    # Jika input berupa URL utuh, ambil bagian 'chapter/uuid'
    if "shinigami.asia/" in raw_path:
        path = raw_path.split("shinigami.asia/")[-1].split('?')[0].lstrip('/')
    else:
        path = raw_path.lstrip('/')

    try:
        print(f"{YELLOW}[?]{RESET} Target vote: ", end="")
        target = int(input().strip())
    except:
        target = 100

    global vote_success_count
    vote_success_count = 0
    pbar = tqdm(total=target, desc="Progress", bar_format="{l_bar}%s{bar}%s{r_bar}" % (GREEN, RESET))

    while vote_success_count < target:
        print(f"\n{YELLOW}[i]{RESET} Scraper sedang mencari proxy baru...")
        all_proxies = fetch_proxies()
        print(f"{MAGENTA}[+]{RESET} Berhasil dapet {len(all_proxies)} proxy. Memulai serangan...")

        threads = []
        # Menggunakan 150 thread agar lebih stabil di VPS
        for _ in range(150):
            t = threading.Thread(target=worker, args=(path, all_proxies, pbar, target))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
        
        if vote_success_count < target:
            print(f"\n{RED}[!] Proxy habis tapi target belum tercapai. Mengulang scrape...{RESET}")
            time.sleep(2)

    pbar.close()
    print(f"\n{GREEN}DONE! {target} vote sukses terkirim ke {path}{RESET}")

if __name__ == "__main__":
    main()
