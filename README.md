# Sistem Manajemen Perpustakaan (MVC)

Aplikasi desktop Sistem Manajemen Perpustakaan yang dibangun menggunakan bahasa pemrograman Python dengan menerapkan arsitektur **Model-View-Controller (MVC)**, otentikasi kata sandi terenkripsi **SHA-256**, serta otorisasi berbasis peran (**Role-Based Access Control / RBAC**).

---

## 🛠️ Fitur Utama

- **Autentikasi Aman (SHA-256):** Enkripsi *one-way hash* SHA-256 pada kata sandi pengguna untuk melindungi kredensial dari kebocoran data.
- **Otorisasi Berbasis Peran (RBAC):**
  - **Admin:** Memiliki akses penuh untuk menambah (Create), memperbarui (Update), dan menghapus (Delete) data buku.
  - **Anggota:** Akses terbatas *read-only* (melihat daftar buku). Form input serta tombol *Update* dan *Delete* dikunci secara otomatis (`state="disabled"`).
- **Manajemen Sesi & Logout:** Fitur untuk keluar dari aplikasi secara aman dan mengembalikan pengguna ke halaman *Login*.
- **CI/CD Pipeline:** Pengujian otomatis dengan `pytest` dan pengecekan kualitas kode menggunakan `flake8` di GitHub Actions.

---

## 📁 Struktur Direktori MVC

Proyek ini disusun berdasarkan pola arsitektur MVC untuk memastikan pemisahan tanggung jawab (*separation of concerns*) yang bersih:

```text
├── config/
│   └── database.py          # Konfigurasi dan koneksi ke basis data MySQL
├── controllers/
│   ├── auth_controller.py   # Pengendali alur autentikasi login
│   └── buku_controller.py   # Pengendali logika bisnis data buku, RBAC, dan logout
├── models/
│   ├── buku_model.py        # Kueri database terkait operasi CRUD data buku
│   └── user_model.py        # Kueri database terkait akun pengguna & hashing SHA-256
├── views/
│   ├── login_view.py        # Antarmuka grafis (GUI) halaman login
│   └── buku_view.py         # Antarmuka grafis (GUI) manajemen data buku
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml  # Konfigurasi CI Pipeline (Flake8 & Pytest)
├── main.py                  # Titik masuk utama (entry point) aplikasi
├── requirements.txt         # Daftar pustaka/dependensi Python
└── README.md                # Dokumentasi teknis proyek