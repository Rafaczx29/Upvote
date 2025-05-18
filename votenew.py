import requests
import threading
import time

# ANSI warna
GREEN = '\033[92m'
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

def fetch_proxies():
    proxies = set()
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                text = r.text
                if 'geonode' in url:
                    data = r.json()
                    for item in data.get('data', []):
                        ip = item.get('ip')
                        port = item.get('port')
                        if ip and port:
                            proxies.add(f"{ip}:{port}")
                else:
                    lines = text.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and ':' in line:
                            proxies.add(line)
        except Exception:
            pass
    return list(proxies)

def vote(proxy, path):
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
            print(f"{GREEN}Vote sukses via proxy {proxy}{RESET}")
    except Exception:
        pass

def worker(path, proxies, index_lock):
    while True:
        with index_lock:
            if not proxies:
                break
            proxy = proxies.pop()
        vote(proxy, path)
        time.sleep(1)

def main():
    path = input("Input Link Tujuan Lu: ").strip()
    loop_count = input("Mau diulang berapa kali? (ketik angka): ").strip()

    try:
        loop_count = int(loop_count)
        if loop_count < 1:
            print("Minimal loop 1 ya, jadi default 1")
            loop_count = 1
    except ValueError:
        print("Input bukan angka, default loop = 1")
        loop_count = 1

    for i in range(loop_count):
        print(f"\n=== Loop ke-{i+1} dimulai ===")
        print("Mengambil proxy gratisan...")
        proxies = fetch_proxies()
        print(f"Proxy ditemukan: {len(proxies)}")

        index_lock = threading.Lock()
        threads = []
        for _ in range(1000):
            t = threading.Thread(target=worker, args=(path, proxies, index_lock))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(f"Selesai vote loop ke-{i+1}.\n")
        # Bisa tambahin delay di sini kalau mau, misal time.sleep(5)

    print("Semua loop selesai.")

if __name__ == "__main__":
    main()