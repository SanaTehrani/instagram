import sqlite3
from modules.models import User

DB_PATH = "database/db.sqlite3"

class ExploreManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_follow_table()

    def create_follow_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS follows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    followed_id INTEGER NOT NULL,
                    UNIQUE(user_id, followed_id)
                )
            """)
    def search_user(self, current_user_id):
        keyword = input("🔍 نام کاربری موردنظر: ").strip()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, username FROM users WHERE username LIKE ?", (f"%{keyword}%",))
            results = cur.fetchall()

        if not results:
            print("❌ کاربری پیدا نشد.")
            return

        for user in results:
            if user[0] == current_user_id:
                continue  # خودت رو نشون نده

            print(f"\n👤 کاربر: @{user[1]} (ID: {user[0]})")
            action = input("👉 دنبال کردن (f) / لغو دنبال (u) / رد (Enter): ").strip().lower()

            if action == "f":
                self.follow_user(current_user_id, user[0])
            elif action == "u":
                self.unfollow_user(current_user_id, user[0])
    def follow_user(self, user_id, followed_id):
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("INSERT INTO follows (user_id, followed_id) VALUES (?, ?)", (user_id, followed_id))
                print("✅ دنبال کردی.")
            except sqlite3.IntegrityError:
                print("⚠️ قبلاً دنبال کردی.")

    def unfollow_user(self, user_id, followed_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM follows WHERE user_id = ? AND followed_id = ?", (user_id, followed_id))
            print("❎ دنبال‌کردن لغو شد.")

