from model.anggota_model import AnggotaModel

model_anggota = AnggotaModel()

print("1. Menambah Data Anggota Baru (Create)")
model_anggota.create_anggota("Moh Arif Sigit", "Jl. Merpati No. 3")
model_anggota.create_anggota("Bimo Prakoso", "Jl. Layana Indah")
print("Data anggota berhasil ditambahkan!")

print("\n2. Menampilkan Seluruh Data Anggota (Read)")
daftar_anggota = model_anggota.get_all_anggota()
for anggota in daftar_anggota:
    print(f"ID: {anggota['id_anggota']} | Nama: {anggota['nama']} | Alamat: {anggota['alamat']}")