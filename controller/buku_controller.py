import tkinter.messagebox as messagebox
from model.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        # --- TAMBAHAN: Binding tombol update, delete, dan logout ---
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_delete.configure(command=self.delete_data)
        self.view.btn_logout.configure(command=self.logout)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol aksi (Tugas 2)
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled", fg_color="gray") # Tombol Update dikunci
            self.view.btn_delete.configure(state="disabled", fg_color="gray") # Tombol Delete dikunci
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def simpan_data(self):
        # Proteksi ganda di Level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def update_data(self):
        # Proteksi tambahan RBAC
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui!")
            return
            
        item = self.view.tabel.item(selected_item)
        id_buku = item['values'][0]
        
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()
        
        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
            
        berhasil = self.model.update_buku(id_buku, judul, penulis, tahun)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def delete_data(self):
        # Proteksi tambahan RBAC
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return
            
        item_data = self.view.tabel.item(selected_item)
        id_buku = item_data['values'][0]
        
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data buku ini?"):
            berhasil = self.model.delete_buku(id_buku)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_tahun.delete(0, 'end')
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data.")

    def logout(self):
        """Fungsi Logout (Tugas 3) untuk menutup BukuView dan kembali ke Login via AuthController"""
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar dari sistem?"):
            # 1. Tutup jendela dashboard saat ini
            self.view.destroy()
            
            # 2. Panggil kembali AuthController agar halaman login siap digunakan dengan fungsionalitas penuh
            from controller.auth_controller import AuthController
            auth_app = AuthController()
            auth_app.run()

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()