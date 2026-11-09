import hashlib
from config.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # Mengubah plain text password menjadi hash SHA-256
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def autentikasi(self, username, password):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)

            # Parameterized Query untuk mencegah SQL Injection
            query = f"SELECT id_user, username, role FROM {self.table_name} WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user
        return None

    def register_user(self, username, password, role):
        """
        Menambahkan pengguna baru ke database dengan password terenkripsi SHA-256.
        """
        if self.conn:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)

            # Parameterized Query untuk insert data aman
            query = f"INSERT INTO {self.table_name} (username, password, role) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, (username, password_hash, role))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Gagal registrasi user: {e}")
                cursor.close()
                return False
        return False