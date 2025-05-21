Here’s an updated version of the README file to include instructions for using Flask:

```markdown
# Aplikasi Pengolahan Gambar dengan Flask

Aplikasi ini menggunakan Flask untuk membuat antarmuka web yang memungkinkan pengguna untuk mengunggah gambar dan memprosesnya dengan berbagai tahap pengolahan, seperti segmentasi dan transformasi.

## Prasyarat

Pastikan kamu sudah menginstal semua dependensi yang diperlukan untuk menjalankan aplikasi ini. Kamu bisa menginstalnya menggunakan `pip`:

```bash
pip install -r requirements.txt
````

`requirements.txt` harus berisi dependensi seperti `Flask`, `Pillow`, dan lainnya yang diperlukan untuk aplikasi ini.

## Menjalankan Aplikasi

1. **Install Flask dan Dependensi Lainnya**
   Jika belum menginstal Flask dan dependensi lainnya, pastikan untuk menginstalnya terlebih dahulu:

   ```bash
   pip install flask
   ```

2. **Mengupload Gambar**
   Aplikasi ini memungkinkan pengguna untuk mengupload gambar melalui antarmuka web (`index.html`). Setelah gambar diunggah, aplikasi akan memprosesnya dengan skrip Python.

3. **Pengolahan Gambar**
   Skrip Python berikut digunakan untuk memproses gambar yang diunggah:

   - **filter.py**: Skrip untuk menerapkan filter tertentu pada gambar.
   - **segmentasi.py**: Skrip untuk membagi gambar menjadi segmen-segmen yang lebih kecil.
   - **transform.py**: Skrip untuk melakukan transformasi pada gambar.
   - **studicase.py**: Skrip untuk menganalisis hasil pengolahan gambar pada studi kasus tertentu.

4. **Melihat Hasil**
   Setelah pengolahan selesai, hasilnya akan disimpan dalam folder `processed/` dan dapat diakses oleh pengguna.

## Cara Menjalankan Aplikasi Flask

1. **Jalankan Aplikasi Flask**
   Untuk menjalankan aplikasi Flask, jalankan perintah berikut:

   ```bash
   python main.py
   ```

   Pastikan kamu berada di direktori yang sama dengan `main.py`. Aplikasi akan berjalan di `http://127.0.0.1:5000/` secara default.

2. **Akses Antarmuka Web**
   Setelah aplikasi berjalan, buka browser dan akses `http://127.0.0.1:5000/` untuk mengunggah gambar dan melihat hasil pengolahan.

3. **Fungsi Upload**
   Gambar yang diunggah akan diproses oleh aplikasi sesuai dengan fungsi yang telah ditentukan, dan hasilnya akan ditampilkan pada halaman web.

## Lisensi

Aplikasi ini dilisensikan di bawah [MIT License](LICENSE).

```

### Penjelasan:
1. **Flask Setup**: Flask digunakan untuk membangun aplikasi web. Dalam `main.py`, aplikasi akan disetup untuk mengakses antarmuka HTML (`index.html`) dan memproses gambar yang diunggah.
2. **File Upload**: Menggunakan `Flask` untuk menerima file yang diunggah dan kemudian memproses file tersebut dengan skrip Python yang sesuai.
3. **Folder**: File gambar yang diunggah akan disimpan di dalam folder `uploads/`, dan hasil pengolahan disimpan dalam folder `processed/`.

Pastikan di dalam `main.py` sudah ada kode untuk menangani rute-rute Flask dan memproses gambar sesuai dengan kebutuhan aplikasi. Let me know if you'd like further details!
```
