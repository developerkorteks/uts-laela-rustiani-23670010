#!/usr/bin/env bash
# ==============================================================================
# Script Otomatis Setup Django + Apache mod_wsgi di Local VPS (Ubuntu/Debian)
# UTS Administrasi Server
# ==============================================================================

set -e

PROJECT_DIR="/var/www/administrasi-server"

echo "=== [1/6] Memperbarui paket sistem & menginstal Apache + mod_wsgi ==="
sudo apt-get update
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3 python3 python3-venv python3-pip git

echo "=== [2/6] Memeriksa virtual environment di $PROJECT_DIR ==="
cd "$PROJECT_DIR"
if [ ! -d "venv" ]; then
    echo "Membuat virtual environment Python..."
    python3 -m venv venv
fi

echo "=== [3/6] Menginstal dependensi Python dari requirements.txt ==="
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo "=== [4/6] Menjalankan Migrate, Collectstatic, dan Seed Demo Data ==="
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
venv/bin/python manage.py seed_demo

echo "=== [5/6] Mengatur izin folder untuk user Apache (www-data) ==="
# Catatan penting SQLite: folder yang memuat db.sqlite3 harus writable oleh www-data
sudo chown -R www-data:www-data "$PROJECT_DIR"
sudo chmod -R 775 "$PROJECT_DIR"
# Pastikan user saat ini juga masuk ke group www-data
sudo usermod -aG www-data "$USER"

echo "=== [6/6] Menerapkan konfigurasi Apache VirtualHost ==="
sudo cp "$PROJECT_DIR/deploy/apache-django.conf" /etc/apache2/sites-available/administrasi-server.conf
sudo a2enmod wsgi rewrite
sudo a2dissite 000-default.conf || true
sudo a2ensite administrasi-server.conf
sudo apache2ctl configtest
sudo systemctl restart apache2

echo "======================================================================"
echo " Setup Sukses! Apache2 sekarang melayani Django via mod_wsgi."
echo " Tes akses dari browser: http://127.0.0.1/ atau port forwarding Anda"
echo "======================================================================"
