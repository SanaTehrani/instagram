import sqlite3

DB_PATH = "database/db.sqlite3"

class ProfileManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def view_profile(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, email, bio FROM users WHERE id = ?", (user_id,))
            user = cur.fetchone()

        if user:
            print("\n👤 پروفایل شما:")
            print(f"نام کاربری: @{user[0]}")
            print(f"ایمیل: {user[1]}")
            print(f"بیو: {user[2]}")
        else:
            print("❌ پروفایل یافت نشد.")

    def edit_profile(self, user_id):
        new_username = input("نام کاربری جدید (Enter = بدون تغییر): ")
        new_email = input("ایمیل جدید (Enter = بدون تغییر): ")
        new_bio = input("بیو جدید (Enter = بدون تغییر): ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            if new_username:
                cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            if new_email:
                cur.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            if new_bio:
                cur.execute("UPDATE users SET bio = ? WHERE id = ?", (new_bio, user_id))

            conn.commit()
            print("✅ پروفایل به‌روزرسانی شد.")
