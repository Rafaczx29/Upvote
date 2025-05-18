import requests
import threading
import time

# ANSI warna
GREEN = '\033[92m'
RESET = '\033[0m'

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=https",
    "https://www.proxyscan.io/download?type=socks4",
    "https://www.proxyscan.io/download?type=socks5",
    "https://openproxy.space/list/http",
    "https://openproxy.space/list/https",
    "https://openproxy.space/list/socks4",
    "https://openproxy.space/list/socks5",
    "https://spys.me/proxy.txt",
    "https://www.geonode.com/free-proxy-list/",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&page=1&sort_by=lastChecked&sort_type=desc",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks4.txt",
    "https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/main/All_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/main/http_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/main/socks4_proxies.txt",
    "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/main/socks5_proxies.txt",
    "https://raw.githubusercontent.com/vmheaven/VMHeaven-Free-Proxy-Updated/main/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/test/proxy.txt",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://www.socks-proxy.net/",
    "https://www.proxynova.com/proxy-server-list/",
    "https://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc",
    "https://www.my-proxy.com/free-proxy-list.html",
    "https://www.proxy-listen.de/Proxy/Proxyliste.html",
    "https://www.proxylists.net/",
    "https://www.proxynova.com/proxy-server-list/country-us/",
    "https://www.proxynova.com/proxy-server-list/country-de/",
    "https://www.proxynova.com/proxy-server-list/country-fr/",
    "https://www.proxynova.com/proxy-server-list/country-gb/",
    "https://www.proxynova.com/proxy-server-list/country-ca/",
    "https://www.proxynova.com/proxy-server-list/country-au/",
    "https://www.proxynova.com/proxy-server-list/country-jp/",
    "https://www.proxynova.com/proxy-server-list/country-cn/",
    "https://www.freeproxy.world/",
    "https://www.proxy-list.org/english/index.php",
    "https://www.proxynova.com/proxy-server-list/country-br/",
    "https://www.proxynova.com/proxy-server-list/country-in/",
    "https://www.proxynova.com/proxy-server-list/country-ru/",
    "https://www.proxydocker.com/en/proxylist/country/US",
    "https://www.proxydocker.com/en/proxylist/country/DE",
    "https://www.proxydocker.com/en/proxylist/country/FR",
    "https://www.proxydocker.com/en/proxylist/country/GB",
    "https://www.proxydocker.com/en/proxylist/country/CA",
    "https://www.proxydocker.com/en/proxylist/country/AU",
    "https://www.proxydocker.com/en/proxylist/country/JP",
    "https://www.proxydocker.com/en/proxylist/country/CN",
    "https://proxy-daily.com/",
    "https://premproxy.com/list/",
    "https://advanced.name/freeproxy",
    "https://ghostealth.com/proxy-scraper",
    "https://iproyal.com/free-proxy-list/",
    "https://hide.mn/en/proxy-list/",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://proxy-spider.com/api/proxies.example",
    "https://www.freeproxylists.net/",
    "https://proxylist.me/",
    "https://www.cool-proxy.net/",
    "https://www.proxies24.com/",
    "https://www.socks-proxy.net/",
    "https://www.advanced-proxy.com/",
    "https://www.getproxylist.com/api/proxy",
    "https://multiproxy.org/txt_all/proxy.txt",
    "https://www.proxyserverlist24.top/",
    "https://proxyhub.me/en/free-proxy-list.html",
    "https://www.proxynova.com/proxy-server-list/",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://www.socks-proxy.net/",
    "https://free-proxy-list.net/",
    "https://www.proxy-list.download/HTTP",
    "https://www.proxy-list.download/HTTPS",
    "https://www.proxy-list.download/SOCKS4",
    "https://www.proxy-list.download/SOCKS5",
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=https",
    "https://www.proxyscan.io/download?type=socks4",
    "https://www.proxyscan.io/download?type=socks5",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/",
    "https://proxy-daily.com/",
    "https://www.proxylists.net/",
    "https://www.proxylists.net/http_highanon.txt",
    "https://www.proxylists.net/https_highanon.txt",
    "https://www.proxylists.net/socks4.txt",
    "https://www.proxylists.net/socks5.txt",
    "https://www.my-proxy.com/free-proxy-list.html",
    "https://www.my-proxy.com/free-anonymous-proxy.html",
    "https://www.my-proxy.com/free-elite-proxy.html",
    "https://www.my-proxy.com/free-transparent-proxy.html",
    "https://www.my-proxy.com/free-socks-4-proxy.html",
    "https://www.my-proxy.com/free-socks-5-proxy.html",
    "https://www.my-proxy.com/free-proxy-list-1.html",
    "https://www.my-proxy.com/free-proxy-list-2.html",
    "https://www.my-proxy.com/free-proxy-list-3.html",
    "https://www.my-proxy.com/free-proxy-list-4.html",
    "https://www.my-proxy.com/free-proxy-list-5.html",
    "https://www.my-proxy.com/free-proxy-list-6.html",
    "https://www.my-proxy.com/free-proxy-list-7.html",
    "https://www.my-proxy.com/free-proxy-list-8.html",
    "https://www.my-proxy.com/free-proxy-list-9.html",
    "https://www.my-proxy.com/free-proxy-list-10.html",
    "https://www.my-proxy.com/free-proxy-list-11.html",
    "https://www.my-proxy.com/free-proxy-list-12.html",
    "https://www.my-proxy.com/free-proxy-list-13.html",
    "https://www.my-proxy.com/free-proxy-list-14.html",
    "https://www.my-proxy.com/free-proxy-list-15.html",
    "https://www.my-proxy.com/free-proxy-list-16.html",
    "https://www.my-proxy.com/free-proxy-list-17.html",
    "https://www.my-proxy.com/free-proxy-list-18.html",
    "https://www.my-proxy.com/free-proxy-list-19.html",
    "https://www.my-proxy.com/free-proxy-list-20.html",
    "https://www.my-proxy.com/free-proxy-list-21.html",
    "https://www.my-proxy.com/free-proxy-list-22.html",
    "https://www.my-proxy.com/free-proxy-list-23.html",
    "https://www.my-proxy.com/free-proxy-list-24.html",
    "https://www.my-proxy.com/free-proxy-list-25.html",
    "https://www.my-proxy.com/free-proxy-list-26.html",
    "https://www.my-proxy.com/free-proxy-list-27.html",
    "https://www.my-proxy.com/free-proxy-list-28.html",
    "https://www.my-proxy.com/free-proxy-list-29.html",
    "https://www.my-proxy.com/free-proxy-list-30.html",
    "https://www.my-proxy.com/free-proxy-list-31.html",
    "https://www.my-proxy.com/free-proxy-list-32.html",
    "https://www.my-proxy.com/free-proxy-list-33.html",
    "https://www.my-proxy.com/free-proxy-list-34.html",
    "https://www.my-proxy.com/free-proxy-list-35.html",
    "https://www.my-proxy.com/free-proxy-list-36.html",
    "https://www.my-proxy.com/free-proxy-list-37.html",
    "https://www.my-proxy.com/free-proxy-list-38.html",
    "https://www.my-proxy.com/free-proxy-list-39.html",
    "https://www.my-proxy.com/free-proxy-list-40.html",
    "https://www.my-proxy.com/free-proxy-list-41.html",
    "https://www.my-proxy.com/free-proxy-list-42.html",
    "https://www.my-proxy.com/free-proxy-list-43.html",
    "https://www.my-proxy.com/free-proxy-list-44.html",
    "https://www.my-proxy.com/free-proxy-list-45.html",
    "https://www.my-proxy.com/free-proxy-list-46.html",
    "https://www.my-proxy.com/free-proxy-list-47.html",
    "https://www.my-proxy.com/free-proxy-list-48.html",
    "https://www.my-proxy.com/free-proxy-list-49.html",
    "https://www.my-proxy.com/free-proxy-list-50.html",
    "https://www.my-proxy.com/free-proxy-list-51.html",
    "https://www.my-proxy.com/free-proxy-list-52.html",
    "https://www.my-proxy.com/free-proxy-list-53.html",
    "https://www.my-proxy.com/free-proxy-list-54.html",
    "https://www.my-proxy.com/free-proxy-list-55.html",
    "https://www.my-proxy.com/free-proxy-list-56.html",
    "https://www.my-proxy.com/free-proxy-list-57.html",
    "https://www.my-proxy.com/free-proxy-list-58.html",
    "https://www.my-proxy.com/free-proxy-list-59.html",
    "https://www.my-proxy.com/free-proxy-list-60.html",
    "https://www.my-proxy.com/free-proxy-list-61.html",
    "https://www.my-proxy.com/free-proxy-list-62.html",
    "https://www.my-proxy.com/free-proxy-list-63.html",
    "https://www.my-proxy.com/free-proxy-list-64.html",
    "https://www.my-proxy.com/free-proxy-list-65.html",
    "https://www.my-proxy.com/free-proxy-list-66.html",
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
        for _ in range(200000):
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