import customtkinter as ctk
from tkinter import ttk, messagebox
from model.anggota_model import AnggotaModel  # Pastikan folder bernama 'model' (tanpa 's')

class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan - Anggota")
        self.geometry("900x500")
        
        # Inisialisasi Model Anggota
        self.model = AnggotaModel()
        self.selected_id = None  # Menyimpan ID anggota yang sedang dipilih

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ==================== FRAME KIRI: FORMULIR INPUT ANGGOTA ====================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input (Nama Anggota dan Alamat)
        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Anggota")
        self.entry_nama.pack(pady=10, padx=15, fill="x")
        
        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Alamat")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        # Tombol Aksi (Dihubungkan ke Fungsi)
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green", command=self.tambah_anggota)
        self.btn_simpan.pack(pady=8, padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data", fg_color="blue", command=self.update_anggota)
        self.btn_update.pack(pady=8, padx=15, fill="x")

        self.btn_delete = ctk.CTkButton(self.frame_kiri, text="Hapus Data", fg_color="red", command=self.delete_anggota)
        self.btn_delete.pack(pady=8, padx=15, fill="x")

        # ==================== FRAME KANAN: TABEL DAFTAR ANGGOTA ====================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kanan, text="Daftar Anggota Perpustakaan", font=("Arial", 16, "bold")).pack(pady=15)

        kolom = ("id_anggota", "nama", "alamat")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id_anggota", text="ID")
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id_anggota", width=40, anchor="center")
        self.tabel.column("nama", width=160)
        self.tabel.column("alamat", width=220)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

        # Event: Ketika baris tabel diklik, datanya masuk ke form input
        self.tabel.bind("<<TreeviewSelect>>", self.select_anggota)

        # Muat data dari database saat aplikasi dibuka
        self.load_data()

    def load_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        
        daftar_anggota = self.model.get_all_anggota()
        for anggota in daftar_anggota:
            self.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def tambah_anggota(self):
        nama = self.entry_nama.get()
        alamat = self.entry_alamat.get()

        if nama and alamat:
            self.model.create_anggota(nama, alamat)
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan ke database!")
            self.load_data()
            self.clear_form()
        else:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")

    def select_anggota(self, event):
        selected_item = self.tabel.selection()
        if selected_item:
            item_data = self.tabel.item(selected_item)
            values = item_data['values']
            if values:
                self.selected_id = values[0]
                self.entry_nama.delete(0, 'end')
                self.entry_nama.insert(0, values[1])
                self.entry_alamat.delete(0, 'end')
                self.entry_alamat.insert(0, values[2])

    def update_anggota(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel terlebih dahulu untuk diperbarui!")
            return

        nama = self.entry_nama.get()
        alamat = self.entry_alamat.get()

        if nama and alamat:
            self.model.update_anggota(self.selected_id, nama, alamat)
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.load_data()
            self.clear_form()
            self.selected_id = None
        else:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")

    def delete_anggota(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel terlebih dahulu untuk dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data anggota ini?"):
            self.model.delete_anggota(self.selected_id)
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
            self.load_data()
            self.clear_form()
            self.selected_id = None

    def clear_form(self):
        self.entry_nama.delete(0, 'end')
        self.entry_alamat.delete(0, 'end')

if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()