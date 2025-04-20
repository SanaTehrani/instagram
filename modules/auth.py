import sqlite3
from getpass import getpass
from modules.models import User

DB_PATH = "database/db.sqlite3"

class AuthManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

    def register(self):
        print("ثبت‌نام کاربر جدید")
        username = input("نام کاربری: ")
        email = input("ایمیل: ")
        password = getpass("رمز عبور: ")

        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password)
                )
                conn.commit()
                print("ثبت‌نام با موفقیت انجام شد.")
        except sqlite3.IntegrityError:
            print("این نام کاربری یا ایمیل قبلاً استفاده شده.")

    def login(self):
        print("ورود")
        username = input("نام کاربری: ")
        password = getpass("رمز عبور: ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, username, email, password FROM users WHERE username=? AND password=?", (username, password))
            row = cur.fetchone()
            if row:
                return User(*row)

            print("نام کاربری یا رمز اشتباهه.")
            return None

    def add_bio_column():
        with sqlite3.connect("database/db.sqlite3") as conn:
            cur = conn.cursor()
            cur.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT ''")
            print("بیو اضافه شد")
    
    def add_bio_column(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT ''")
            print("بیو اضافه شد")


