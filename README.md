# Sistem Inventori Gudang - UAS Struktur Data

### Deskripsi
Aplikasi manajemen inventori gudang berbasis CLI menggunakan file CSV sebagai database. Dibuat untuk memenuhi UAS mata kuliah Struktur Data.

### Fitur
1. **CRUD**: Tambah, Lihat, Update, Hapus data barang
2. **Searching**: Cari barang berdasarkan nama
3. **Sorting**: Urutkan barang berdasarkan stok terkecil menggunakan Bubble Sort
4. **Undo**: Mengembalikan data yang terakhir dihapus

### Struktur Data yang Digunakan
1. **Linked List**: Untuk menyimpan seluruh data inventori di memori
2. **Stack**: Untuk fitur Undo hapus barang

### Cara Menjalankan
1. Pastikan sudah install Python 3
2. Jalankan di terminal: `python inventori_app.py`
3. File `inventori.csv` akan otomatis dibuat saat pertama kali dijalankan

### Flowchart
Lihat file `flowchart.png`