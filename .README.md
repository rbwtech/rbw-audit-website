# RBW Safe Browser Checker

Aplikasi desktop untuk mengecek keamanan website menggunakan Google Safe Browsing API.

## Fitur

- Scan kategori website (Pendidikan, E-Commerce, Berbahaya)
- Input URL manual dengan auto-detect protokol
- Validasi domain sebelum scan
- Deteksi 4 jenis ancaman: Malware, Social Engineering, Unwanted Software, Potentially Harmful Application
- GUI sederhana menggunakan PySide6

## Instalasi
```bash
# Clone repository
git clone https://github.com/rbwtech/rbw-safe-browser.git
cd rbw-safe-browser

# Install dependencies
pip install -r requirements.txt

# Isi dan rename config
mv config.py.example config.py

# Jalankan aplikasi
python main.py