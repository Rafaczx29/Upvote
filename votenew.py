import requests
import threading
import time
import os
from pyfiglet import figlet_format
from tqdm import tqdm

# ANSI warna
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://openproxy.space/list/http",
    "https://openproxy.space/list/https",
    "https://spys.me/proxy.txt",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&page=1&sort_by=lastChecked&sort_type=desc",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
]

vote_success_count = 0
success_lock = threading.Lock()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def fetch_proxies():
    proxies = set()
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                if 'geonode' in url:
                    data = r.json()
                    for item in data.get('data', []):
                        ip = item.get('ip')
                        port = item.get('port')
                        if ip and port:
                            proxies.add(f"{ip}:{port}")
                else:
                    lines = r.text.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and ':' in line:
                            proxies.add(line)
        except Exception:
            pass
    return list(proxies)

def vote(proxy, path, pbar, target):
    global vote_success_count
    url = "https://commento.shngm.io/api/article?lang=en"
    headers = {
        "Host": "commento.shngm.io",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J20CG Build/SKQ1.211019.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/136.0.7103.125 Mobile Safari/537.36",
        "Origin": "https://dev.shinigami.asia",
        "Referer": "https://dev.shinigami.asia/",
        "X-Requested-With": "com.cookiegames.smartcookie",
    }
    payload = {
        "path": path,
        "type": "reaction0"
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=10)
        if resp.status_code == 200:
            with success_lock:
                if vote_success_count < target:
                    vote_success_count += 1
                    pbar.update(1)
    except Exception:
        pass

def worker(path, proxies, index_lock, pbar, target):
    while True:
        with success_lock:
            if vote_success_count >= target:
                break
        with index_lock:
            if not proxies:
                break
            proxy = proxies.pop()
        vote(proxy, path, pbar, target)
        time.sleep(0.3)

def tampil_banner():
    print(f"{GREEN}{figlet_format('Auto Vote', font='slant')}{RESET}")
    print(f"{CYAN}Dibuat oleh {MAGENTA}@Rafaczx{CYAN} | Powered by AutoProxy{RESET}\n")

def main():
    clear_screen()
    tampil_banner()

    print(f"{YELLOW}[?]{RESET} Input Link Tujuan Lu: ", end="")
    path = input().strip()

    try:
        print(f"{YELLOW}[?]{RESET} Total vote yang lu inginkan berapa banyak?: ", end="")
        target = int(input().strip())
    except ValueError:
        print(f"{RED}[!] Input bukan angka. Default = 100{RESET}")
        target = 100

    global vote_success_count
    vote_success_count = 0
    loop_count = 0

    pbar = tqdm(total=target, desc="Total Vote Sukses", bar_format="{l_bar}%s{bar}%s{r_bar}" % (GREEN, RESET))

    while vote_success_count < target:
        loop_count += 1
        print(f"\n{CYAN}=== Loop ke-{loop_count} dimulai ==={RESET}")
        print(f"{YELLOW}[i]{RESET} Mengambil proxy untuk memproses...")
        proxies = fetch_proxies()
        print(f"{MAGENTA}[+] Proxy ditemukan: {len(proxies)}{RESET}")

        index_lock = threading.Lock()
        threads = []

        for _ in range(200):  # jumlah thread
            t = threading.Thread(target=worker, args=(path, proxies, index_lock, pbar, target))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(f"{CYAN}Selesai vote loop ke-{loop_count}.{RESET}")

    pbar.close()
    print(f"\n{GREEN}{'='*44}")
    print(f"   Target {target} vote sukses tercapai!")
    print(f"{'='*44}{RESET}")
    print(f"{MAGENTA}Terima kasih telah menggunakan AutoProxy by Rafaczx!{RESET}")

if __name__ == "__main__":
    main()