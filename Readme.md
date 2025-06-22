1. **Jalankan Aplikasi Flask**
   Untuk menjalankan aplikasi Flask, jalankan perintah berikut:

   ```bash
      pip install -r requirements.txt

   ```

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
