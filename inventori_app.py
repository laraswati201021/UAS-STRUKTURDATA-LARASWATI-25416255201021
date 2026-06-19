import csv
import os

CSV_FILE = 'inventori.csv'
FIELDNAMES = ['id_barang', 'nama_barang', 'kategori', 'stok', 'harga']

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items
    
    def display(self):
        items = self.to_list()
        if not items:
            print("Inventori kosong.")
            return
        print(f"{'ID':<5} {'Nama Barang':<20} {'Kategori':<15} {'Stok':<8} {'Harga':<10}")
        print("-"*65)
        for item in items:
            print(f"{item['id_barang']:<5} {item['nama_barang']:<20} {item['kategori']:<15} {item['stok']:<8} {item['harga']:<10}")

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

class InventoriManager:
    def __init__(self):
        self.inventori = LinkedList()
        self.undo_stack = Stack()
        self.load_from_csv()

    def load_from_csv(self):
        self.inventori = LinkedList()
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
            return
        
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.inventori.append(row)

    def save_to_csv(self):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(self.inventori.to_list())

    def create_barang(self):
        print("\n--- Tambah Barang Baru ---")
        id_barang = input("ID Barang: ")
        nama = input("Nama Barang: ")
        kategori = input("Kategori: ")
        stok = input("Stok: ")
        harga = input("Harga: ")
        data_baru = {'id_barang': id_barang, 'nama_barang': nama, 'kategori': kategori, 'stok': stok, 'harga': harga}
        self.inventori.append(data_baru)
        self.save_to_csv()
        print("Barang berhasil ditambahkan!")

    def read_barang(self):
        print("\n--- Daftar Seluruh Inventori ---")
        self.inventori.display()

    def update_barang(self):
        id_target = input("\nMasukkan ID Barang yang mau diupdate: ")
        found = False
        current = self.inventori.head
        while current:
            if current.data['id_barang'] == id_target:
                print("Data ditemukan. Masukkan data baru:")
                current.data['nama_barang'] = input(f"Nama Baru [{current.data['nama_barang']}]: ") or current.data['nama_barang']
                current.data['kategori'] = input(f"Kategori Baru [{current.data['kategori']}]: ") or current.data['kategori']
                current.data['stok'] = input(f"Stok Baru [{current.data['stok']}]: ") or current.data['stok']
                current.data['harga'] = input(f"Harga Baru [{current.data['harga']}]: ") or current.data['harga']
                self.save_to_csv()
                print("Data berhasil diupdate!")
                found = True
                break
            current = current.next
        if not found:
            print("ID Barang tidak ditemukan.")

    def delete_barang(self):
        id_target = input("\nMasukkan ID Barang yang mau dihapus: ")
        current = self.inventori.head
        prev = None
        
        while current and current.data['id_barang']!= id_target:
            prev = current
            current = current.next

        if current is None:
            print("ID Barang tidak ditemukan.")
            return

        self.undo_stack.push(current.data) # Simpan ke stack untuk undo
        
        if prev is None:
            self.inventori.head = current.next
        else:
            prev.next = current.next
            
        self.save_to_csv()
        print(f"Barang {id_target} berhasil dihapus. Gunakan menu Undo untuk mengembalikan.")

    def undo_hapus(self):
        data_terakhir = self.undo_stack.pop()
        if data_terakhir:
            self.inventori.append(data_terakhir)
            self.save_to_csv()
            print(f"Undo berhasil. Barang {data_terakhir['id_barang']} dikembalikan.")
        else:
            print("Tidak ada data yang bisa di-undo.")

    def search_barang(self):
        keyword = input("\nMasukkan nama barang yang dicari: ").lower()
        results = []
        current = self.inventori.head
        while current:
            if keyword in current.data['nama_barang'].lower():
                results.append(current.data)
            current = current.next
        
        if results:
            print("\n--- Hasil Pencarian ---")
            for item in results:
                print(item)
        else:
            print("Barang tidak ditemukan.")

    def sort_by_stok(self):
        items = self.inventori.to_list()
        n = len(items)
        # Bubble Sort
        for i in range(n):
            for j in range(0, n-i-1):
                if int(items[j]['stok']) > int(items[j+1]['stok']):
                    items[j], items[j+1] = items[j+1], items[j]
        
        print("\n--- Inventori Diurutkan Berdasarkan Stok Terkecil ---")
        for item in items:
            print(item)

def main():
    manager = InventoriManager()
    while True:
        print("\n===== SISTEM INVENTORI GUDANG =====")
        print("1. Lihat Semua Barang")
        print("2. Tambah Barang")
        print("3. Update Barang")
        print("4. Hapus Barang")
        print("5. Cari Barang")
        print("6. Urutkan Berdasarkan Stok")
        print("7. Undo Hapus Terakhir")
        print("8. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1': manager.read_barang()
        elif pilihan == '2': manager.create_barang()
        elif pilihan == '3': manager.update_barang()
        elif pilihan == '4': manager.delete_barang()
        elif pilihan == '5': manager.search_barang()
        elif pilihan == '6': manager.sort_by_stok()
        elif pilihan == '7': manager.undo_hapus()
        elif pilihan == '8':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()