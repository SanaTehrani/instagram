import sqlite3
from datetime import datetime

DB_PATH = "database/db.sqlite3"

class MessageManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
    def send_message(self, sender_id):
        receiver_username = input("👤 نام کاربری گیرنده: ")
        content = input("💬 متن پیام: ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # دریافت آیدی گیرنده از روی یوزرنیم
            cur.execute("SELECT id FROM users WHERE username = ?", (receiver_username,))
            receiver = cur.fetchone()

            if not receiver:
                print("❌ کاربر گیرنده پیدا نشد.")
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cur.execute(
                "INSERT INTO messages (sender_id, receiver_id, content, timestamp) VALUES (?, ?, ?, ?)",
                (sender_id, receiver[0], content, timestamp)
            )
            conn.commit()
            print("✅ پیام ارسال شد.")
    def view_inbox(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT users.username, messages.content, messages.timestamp
                FROM messages
                JOIN users ON messages.sender_id = users.id
                WHERE messages.receiver_id = ?
                ORDER BY messages.timestamp DESC
            """, (user_id,))
            messages = cur.fetchall()

        if not messages:
            print("📭 هیچ پیامی نداری.")
            return

        print("\n📥 پیام‌های دریافتی:")
        for msg in messages:
            print(f"\nاز: @{msg[0]} 🕒 {msg[2]}\nمتن: {msg[1]}")
