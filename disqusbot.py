import requests
import random
import threading
import time

# SUMBER PROXY TERBARU (Langsung digunakan tanpa validasi)
proxy_sources = [
    # ProxyScrape (Update Harian)
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",

    # Proxy-List (Update Harian)
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",

    # Free Proxy Lists (Update Berkala)
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=https",
    "https://www.proxyscan.io/download?type=socks4",
    "https://www.proxyscan.io/download?type=socks5",

    # Open Proxy Space (Banyak yang aktif)
    "https://openproxy.space/list/http",
    "https://openproxy.space/list/https",
    "https://openproxy.space/list/socks4",
    "https://openproxy.space/list/socks5",

    # Spys.me (Beberapa proxy premium suka bocor)
    "https://spys.me/proxy.txt",

    # Geonode (Kadang ada premium proxy)
    "https://www.geonode.com/free-proxy-list/",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&page=1&sort_by=lastChecked&sort_type=desc",

    # Sumber Proxy dari GitHub (Update Cepat)
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

    # Proxy dari berbagai negara (Update tidak menentu)
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
]

url_vote = "https://disqus.com/api/3.0/threadReactions/vote"
thread_id = input("Masukkan Thread ID: ").strip()
loop_count = int(input("Berapa kali loop auto-vote? ").strip())

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/537.36",
]

#GANTI VOTE ID
payload = {
    "thread": thread_id,
    "reaction": "3860161",
    "api_key": "E8Uh5l5fHZ6gD8U3KycjAIAk46f68Zw7C6eW8WSjZvCLXebZ7p0r1yrYDrLilk2F"
}

# Ambil semua proxy tanpa validasi
def get_proxies():
    proxies = set()
    threads = []

    def fetch_proxy(url):
        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200:
                for proxy in response.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy and ":" in proxy:
                        proxies.add(proxy)
        except:
            pass

    for url in proxy_sources:
        t = threading.Thread(target=fetch_proxy, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return list(proxies)

# Fungsi voting dengan proxy tertentu
def vote(proxy):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://disqus.com/embed/comments/",
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    try:
        response = requests.post(url_vote, data=payload, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200 and '"code":0' in response.text:
            print(f"✅ Vote berhasil! (Proxy: {proxy})")
        else:
            print(f"❌ Vote gagal. Status: {response.status_code}")
    except:
        pass

# Main function dengan loop otomatis
def main():
    for loop in range(loop_count):
        print(f"\n🔄 Loop {loop+1} dari {loop_count} - Mengambil proxy terbaru...")
        proxies_list = get_proxies()

        if not proxies_list:
            print("⛔ Tidak ada proxy yang tersedia.")
            return

        print(f"✅ Dapat {len(proxies_list)} proxy! Mulai voting...")

        num_threads = 5000  # Jalankan 50 vote sekaligus
        for i in range(0, len(proxies_list), num_threads):
            threads = []
            for proxy in proxies_list[i:i + num_threads]:
                t = threading.Thread(target=vote, args=(proxy,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

        print(f"✅ Loop {loop+1} selesai! Menunggu sebelum loop berikutnya...\n")
        time.sleep(random.uniform(1, 2))  # Delay sebelum loop berikutnya untuk keamanan

if __name__ == "__main__":
    main()