# Scanner.py - SQL Injection Vulnerability Scanner

🚨 *Disclaimer:* This tool is for *educational and authorized security testing only*. Do not scan or attack any system without explicit permission. 

---

## 🔍 Description

scanner.py is a lightweight SQL Injection scanner inspired by SQLMap, designed for beginners and ethical hackers learning web vulnerability exploitation.

It can:
- Detect basic SQL Injection vulnerabilities
- Determine number of columns
- Test for UNION-based injection
- Dump database 
- Dump all available databases

---

## 🛠 Installation

### Clone the repo
```
git clone https://github.com/Rexploit505/scanner.py.git
cd scanner.py

```
## Install dependencies
pip install -r requirements.txt

## Usage
python scanner.py -u "<target_url>" [options]


## Options 
⚙️ Opsi yang Tersedia

| Option         | Deskripsi                                                                           |
| -------------- | ----------------------------------------------------------------------------------- |
| `-u` / `--url` | Target URL dengan parameter yang rentan (contoh: `http://target.com/page.php?id=1`) |
| `--check`      | Mengecek apakah parameter rentan terhadap SQL Injection                             |
| `--columns`    | Mendeteksi jumlah kolom dalam query                                                 |
| `--union`      | Menguji injeksi menggunakan UNION SELECT                                            |
| `--dump-db`    | Menampilkan nama database saat ini                                                  |
| `--dump-all`   | Menampilkan semua nama database yang tersedia                                       |



## Example
# Basic scan
python scanner.py -u "http://localhost/dvwa/vulnerabilities/sqli/?id=1" --check

# Dump database
python scanner.py -u "http://localhost/dvwa/vulnerabilities/sqli/?id=1" --dump-db


## Author 
Made with ❤️ by Rexploit