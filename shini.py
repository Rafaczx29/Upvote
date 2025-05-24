import requests
import time
import random
import threading
from rich.console import Console

console = Console()

def auto_comment_thread(token, thread_id, comment_base, jumlah_per_thread):
    url = "https://commento.shngm.io/api/comment?lang=en"
    headers = {
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://id.shinigami.asia",
        "user-agent": "Mozilla/5.0",
        "x-requested-with": "com.cookiegames.smartcookie",
    }
    for _ in range(jumlah_per_thread):
        rand_number = random.randint(1000, 9999)
        comment_text = f"{comment_base} #{rand_number}"
        payload = {
            "comment": comment_text,
            "nick": "auto_user",
            "mail": "auto_user@example.com",
            "link": None,
            "url": thread_id,
            "ua": headers["user-agent"]
        }
        try:
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                console.print(f"[green]Komentar terkirim: {comment_text}[/green]")
            else:
                console.print(f"[red]Gagal kirim komentar HTTP {res.status_code}[/red]")
        except Exception as e:
            console.print(f"[red]Error kirim komentar: {e}[/red]")
        time.sleep(random.uniform(0.5, 1.5))

def login_account(email, password):
    url = "https://commento.shngm.io/api/token?lang=en"
    payload = {
        "email": email,
        "password": password,
        "code": ""
    }
    headers = {
        "content-type": "application/json",
        "origin": "https://commento.shngm.io",
        "user-agent": "Mozilla/5.0"
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            data = res.json()
            token = data.get("data", {}).get("token")
            if token:
                console.print(f"[green]Login berhasil[/green]")
                return token
            else:
                console.print(f"[red]Token tidak ditemukan[/red]")
        else:
            console.print(f"[red]Login gagal HTTP {res.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error login: {e}[/red]")
    return None

def fitur_4_multithread_1akun():
    email = console.input("Masukkan email akun: ").strip()
    password = console.input("Masukkan password akun: ").strip()
    thread_id = console.input("Masukkan Thread ID (URL komik): ").strip()
    comment_base = console.input("Masukkan isi komentar dasar: ").strip()

    try:
        total_komentar = int(console.input("Total komentar yang mau dikirim: ").strip())
        jumlah_thread = int(console.input("Jumlah thread yang mau dijalankan: ").strip())
        if total_komentar <= 0 or jumlah_thread <= 0:
            console.print("[red]Jumlah harus lebih dari 0[/red]")
            return
    except:
        console.print("[red]Input tidak valid![/red]")
        return

    token = login_account(email, password)
    if not token:
        console.print("[red]Login gagal, program dihentikan[/red]")
        return

    komentar_per_thread = total_komentar // jumlah_thread
    sisa = total_komentar % jumlah_thread

    threads = []
    for i in range(jumlah_thread):
        # Distribusikan sisa komentar ke thread pertama
        jml = komentar_per_thread + (1 if i < sisa else 0)
        t = threading.Thread(target=auto_comment_thread, args=(token, thread_id, comment_base, jml))
        threads.append(t)
        t.start()
        time.sleep(0.2)  # jeda biar gak ngacir semua barengan

    for t in threads:
        t.join()

    console.print("[bold green]Selesai mengirim komentar![/bold green]")

if __name__ == "__main__":
    fitur_4_multithread_1akun()