import requests, json, os, time
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import pyfiglet

console = Console()

def banner():
    ascii_art = pyfiglet.figlet_format("RAFACZX")
    console.print(f"[bold cyan]{ascii_art}[/bold cyan]")

def save_accounts(accounts, filename):
    with open(filename, "w") as f:
        for acc in accounts:
            f.write(f"{acc['email']}|{acc['password']}|{acc['token']}\n")

def load_accounts(filename):
    accounts = []
    if not os.path.exists(filename):
        console.print(f"[red]File {filename} tidak ditemukan![/red]")
        return accounts
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) == 3:
                    email, password, token = parts
                    accounts.append({"email": email, "password": password, "token": token})
    return accounts

def login_account(email, password):
    url = "https://commento.shngm.io/api/token?lang=en"
    payload = {"email": email, "password": password, "code": ""}
    headers = {
        "content-type": "application/json",
        "origin": "https://commento.shngm.io",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; M2007J20CG)"
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data.get("data", {}).get("token")
    return None

def _register_one(index):
    url = "https://commento.shngm.io/api/user?lang=en"
    email = f"user{int(time.time() * 1000) + index}@rafaczx.io"
    password = "1"
    payload = {"display_name": email, "email": email, "password": password}
    headers = {
        "content-type": "application/json",
        "origin": "https://commento.shngm.io",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; M2007J20CG)"
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            token = login_account(email, password)
            if token:
                console.print(f"[green][+] Registered & Logged In: {email}[/green]")
                return {"email": email, "password": password, "token": token}
            else:
                console.print(f"[red][-] Login gagal: {email}[/red]")
        else:
            console.print(f"[red][-] HTTP {res.status_code} saat register: {email}[/red]")
    except Exception as e:
        console.print(f"[red][-] Error register {email}: {e}[/red]")
    return None

def register_account(num):
    accounts = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(_register_one, range(num))
    for acc in results:
        if acc:
            accounts.append(acc)
    return accounts

def _like_one(comment_id, acc):
    url = f"https://commento.shngm.io/api/comment/{comment_id}?lang=en"
    headers = {
        "authorization": f"Bearer {acc['token']}",
        "content-type": "application/json",
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; M2007J20CG)"
    }
    payload = {"like": True}
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            console.print(f"[green][+] Like by {acc['email']} success[/green]")
        else:
            console.print(f"[red][-] Like by {acc['email']} failed: HTTP {res.status_code}[/red]")
    except Exception as e:
        console.print(f"[red][-] Like error {acc['email']}: {e}[/red]")

def auto_like(comment_id, accounts):
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda acc: _like_one(comment_id, acc), accounts)

def list_account_files():
    return [f for f in os.listdir() if f.endswith(".txt")]

def main_menu():
    banner()
    while True:
        console.print(Panel("[bold yellow]AUTO-LIKER FOR SHINIGAMI.AE[/bold yellow]\n1. AUTO LIKE\n2. BUAT AKUN BAHAN\n3. CEK AKUN BAHAN YANG TERSEDIA\n0. KELUAR", title="RAFACZX"))
        choice = console.input("[bold cyan]Pilih menu > [/bold cyan]")
        if choice == "1":
            comment_id = console.input("[bold magenta]Masukkan ID komentar tujuan: [/bold magenta]").strip()
            files = list_account_files()
            if not files:
                console.print("[red]Tidak ada file akun ditemukan, silakan buat akun terlebih dahulu.[/red]")
                continue
            console.print("[bold green]File akun yang tersedia:[/bold green]")
            for idx, file in enumerate(files):
                console.print(f"{idx+1}. {file}")
            file_choice = console.input("[bold cyan]Pilih file akun (nomor): [/bold cyan]").strip()
            try:
                file_idx = int(file_choice) - 1
                if 0 <= file_idx < len(files):
                    accounts = load_accounts(files[file_idx])
                    if accounts:
                        auto_like(comment_id, accounts)
                    else:
                        console.print("[red]File akun kosong atau format salah![/red]")
                else:
                    console.print("[red]Pilihan tidak valid![/red]")
            except:
                console.print("[red]Input tidak valid![/red]")

        elif choice == "2":
            num = console.input("[bold magenta]Jumlah akun buat generate: [/bold magenta]")
            try:
                num_acc = int(num)
                if num_acc > 0:
                    accounts = register_account(num_acc)
                    if accounts:
                        filename = console.input("[bold cyan]Simpan file akun dengan nama: [/bold cyan]").strip()
                        if not filename.endswith(".txt"):
                            filename += ".txt"
                        save_accounts(accounts, filename)
                        console.print(f"[green]File akun berhasil disimpan: {filename}[/green]")
                    else:
                        console.print("[red]Gagal membuat akun baru.[/red]")
                else:
                    console.print("[red]Jumlah akun harus lebih dari 0.[/red]")
            except:
                console.print("[red]Input tidak valid![/red]")

        elif choice == "3":
            files = list_account_files()
            if files:
                console.print("[bold green]File akun yang tersedia:[/bold green]")
                for file in files:
                    console.print(f"- {file}")
            else:
                console.print("[red]Tidak ada file akun ditemukan.[/red]")

        elif choice == "0":
            console.print("[bold yellow]Terima kasih sudah menggunakan RAFACZX. Sampai jumpa![/bold yellow]")
            break
        else:
            console.print("[red]Pilihan tidak valid! Silakan coba lagi.[/red]")

if __name__ == "__main__":
    main_menu()