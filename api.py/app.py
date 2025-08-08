import os
import sys
import subprocess
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__, template_folder='templates')

def find_links(base_url):
    try:
        response = requests.get(base_url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [urljoin(base_url, link.get("href")) for link in soup.find_all("a", href=True)]
        return list(set(links))
    except:
        return []

def test_sqli(url):
    try:
        if "?" in url:
            test_url = url + "'"
            response = requests.get(test_url, timeout=5)
            if any(error in response.text.lower() for error in ["mysql", "syntax", "warning", "sql"]):
                return f"[!] SQL Injection Açığı: {test_url}"
        return "[+] SQL Injection açığı bulunamadı."
    except:
        return "[HATA] SQL Injection testinde hata oluştu."

def test_xss(url):
    try:
        if "?" in url:
            payload = "<script>alert('xss')</script>"
            test_url = url + payload
            response = requests.get(test_url, timeout=5)
            if payload in response.text:
                return f"[!] XSS Açığı: {test_url}"
        return "[+] XSS açığı bulunamadı."
    except:
        return "[HATA] XSS testinde hata oluştu."

def test_csrf(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')

        if not forms:
            return "[i] Sayfada form bulunamadı."

        csrf_eksik = False
        sonuc = []
        for i, form in enumerate(forms, start=1):
            hidden_inputs = form.find_all('input', {'type': 'hidden'})
            token_found = any('csrf' in (inp.get('name', '') + inp.get('id', '')).lower() for inp in hidden_inputs)
            if not token_found:
                csrf_eksik = True
                sonuc.append(f"[!] Form {i} üzerinde CSRF token bulunamadı. Sayfa: {url}")
        if not csrf_eksik:
            return "[+] Tüm formlarda CSRF token bulundu."
        return "\n".join(sonuc)
    except:
        return "[HATA] CSRF testi sırasında hata oluştu."

def test_broken_auth(url):
    try:
        response = requests.get(url, timeout=5)
        cookies = response.cookies
        soup = BeautifulSoup(response.text, 'html.parser')
        zafiyet = []

        if not any('session' in c.name.lower() for c in cookies):
            zafiyet.append("[!] Cookie bulunamadı! Oturum yönetimi eksik olabilir.")
        logout_links = soup.find_all('a', href=True)
        if not any('logout' in a['href'].lower() for a in logout_links):
            zafiyet.append("[!] Logout bağlantısı görünmüyor.")

        return "\n".join(zafiyet) if zafiyet else "[+] Oturum yönetimi güvenli görünüyor."
    except:
        return "[HATA] Oturum yönetimi testinde hata oluştu."

def test_file_upload(url):
    try:
        if any(x in url.lower() for x in ["upload", "file", "submit"]):
            return f"[!] Dosya yükleme alanı tespit edildi. ({url})\n[?] Gerçekten zararlı dosya yüklemek ister misiniz? (Simülasyon yapılır)"
        return "[+] Dosya yükleme zafiyeti bulunamadı."
    except:
        return "[HATA] Dosya yükleme testinde hata oluştu."

def test_all(url, selected_tests):
    results = []
    results.append(f"[*] URL test ediliyor: {url}")
    links = find_links(url)

    if not links:
        results.append("[!] Sayfada bağlantı bulunamadı veya siteye erişilemedi.")
        return results

    for link in links:
        results.append(f"\nLink: {link}")

        if "sqli" in selected_tests:
            results.append(test_sqli(link))
        if "xss" in selected_tests:
            results.append(test_xss(link))
        if "csrf" in selected_tests:
            results.append(test_csrf(link))
        if "auth" in selected_tests:
            results.append(test_broken_auth(link))
        if "fileupload" in selected_tests:
            results.append(test_file_upload(link))

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        target_url = request.form['url']
        selected_tests = ["sqli", "xss", "csrf", "auth", "fileupload"]

        try:
            results = test_all(target_url, selected_tests)
        except Exception as e:
            results = [f"[HATA] Test sırasında beklenmeyen bir hata oluştu: {str(e)}"]

        return render_template('result.html', lines=results, target=target_url)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
