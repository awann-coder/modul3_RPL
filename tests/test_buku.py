from unittest.mock import MagicMock
from model.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar terisolasi
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Mensimulasikan data tiruan (mock data) yang dikembalikan oleh database saat fetchall()
    mock_cursor.fetchall.return_value = [
        (1, "Pemrograman Python MVC", "Guido van Rossum", 2023)
    ]

    # Melakukan eksekusi fungsi get_all_buku
    hasil = model.get_all_buku()

    # Memverifikasi apakah hasil kembaliannya berupa list
    assert isinstance(hasil, list)
    # Memverifikasi apakah kueri pengambilan data (execute) benar-benar dipanggil
    mock_cursor.execute.assert_called_once()