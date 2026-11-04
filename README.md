# Administrasi Server &mdash; Profile Pribadi & Toko E-commerce

Proyek aplikasi web monolit modular yang dibangun menggunakan **Python 3.11** dan **Django 5.2**, menggabungkan dua fungsionalitas utama:
1. **Website Profile Pribadi**: Menampilkan biodata dinamis, daftar keahlian (*skills*), pengalaman kerja, proyek portofolio, dan form kontak. Seluruh konten dapat diedit secara dinamis melalui UI langsung maupun Django Admin.
2. **Website Toko E-commerce**: Katalog produk dengan filter kategori, pencarian, pengurutan harga, sistem keranjang belanja (*cart session*), formulir checkout pesanan dengan pengurangan stok otomatis, pelacakan status pesanan, pratinjau invoice cetak, serta dashboard pengelolaan pesanan untuk staf/admin.

---

## 🛠️ Teknologi & Fitur Desain
- **Python:** 3.11 (`/usr/bin/python3.11`)
- **Backend:** Django 5.2, SQLite3 (dev / default)
- **UI & Tampilan:** Minimalis, clean monospace & sans-serif, dark-mode netral, responsif, tanpa elemen artifisial berlebihan (*no AI-slop design*).

---

## 🚀 Cara Menjalankan Server

1. **Jalankan development server:**
   ```bash
   venv/bin/python manage.py runserver
   ```
   Akses aplikasi di browser pada: `http://127.0.0.1:8000/`

2. **Jalankan pengujian unit test:**
   ```bash
   venv/bin/python manage.py test
   ```

---

## 🔑 Akun Default Staf & Administrasi
Jika data demo sudah diinisialisasi (melalui `manage.py seed_demo`):
- **Username:** `admin`
- **Password:** `admin123`
- **Akses Django Admin:** `http://127.0.0.1:8000/admin/`

---

## 📌 Peta Rute URL Utama

### 1. Website Profile Pribadi
- `/` &mdash; Halaman Beranda Profil, Keahlian, Pengalaman, Portofolio, dan Form Kontak.
- `/edit/` &mdash; Manajemen Profil Dinamis (Biodata, Tambah/Hapus Skill, Pengalaman, dan Proyek Portofolio). Khusus staf.
- `/project/<slug>/` &mdash; Halaman detail proyek portofolio.

### 2. Website Toko E-commerce
- `/store/` &mdash; Katalog produk, filter kategori, pencarian, dan pengurutan harga.
- `/store/product/<slug>/` &mdash; Detail produk dan tombol beli.
- `/store/cart/` &mdash; Halaman keranjang belanja (*cart detail & edit quantity*).
- `/store/checkout/` &mdash; Formulir pemesanan & pemilihan metode pembayaran.
- `/store/order/success/<order_number>/` &mdash; Konfirmasi pesanan dan instruksi pembayaran.
- `/store/order/track/` &mdash; Lacak status pengiriman/pesanan dengan nomor invoice.
- `/store/order/invoice/<order_number>/` &mdash; Lembar cetak invoice ramah printer (*print/PDF-ready*).
- `/store/dashboard/orders/` &mdash; Dashboard manajemen status pesanan pelanggan khusus staf.
