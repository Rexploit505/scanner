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
```bash
git clone https://github.com/Rexploit505/scanner.py.git
cd scanner.py


## Install dependencies
pip install -r requirements.txt

## Usage
python scanner.py -u "<target_url>" [options]


## Options
| Option          | Description                                                                    |
| --------------- | ------------------------------------------------------------------------------ |
| -u or --url | Target URL with vulnerable parameter (e.g., http://target.com/page.php?id=1) |
| --check       | Check if the parameter is vulnerable to SQL Injection                          |
| --columns     | Detect number of
columns                                                       |
| --union       | Test UNION SELECT injection                                                    |
| --dump-db     | Dump current database name                                                     |
| --dump-all    | Dump all available database names                                              |


## Example
# Basic scan
python scanner.py -u "http://localhost/dvwa/vulnerabilities/sqli/?id=1" --check

# Dump database
python scanner.py -u "http://localhost/dvwa/vulnerabilities/sqli/?id=1" --dump-db


## Author 
Made with ❤️ by Rexploit