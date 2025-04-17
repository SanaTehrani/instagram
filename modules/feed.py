import sqlite3
from modules.models import Post
from datetime import datetime

DB_PATH = "database/db.sqlite3"

class FeedManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_table()
        self.create_comment_table()
        self.create_saved_table()

    def create_comment_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL
                )
            """)

    def add_comment(self, user_id):
        post_id = input("🆔 شناسه پست موردنظر برای کامنت: ")
        content = input("💬 متن کامنت: ")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
                (post_id, user_id, content)
            )
        print("کامنت ثبت شد.")

    def create_post(self, user_id):
        caption = input("متن پست: ")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO posts (user_id, caption, created_at) VALUES (?, ?, ?)",
                (user_id, caption, created_at)
            )
        print("پست ساخته شد")

    def show_feed(self, current_user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # 👇 فقط ID اونایی که کاربر فعلی دنبال کرده رو بگیر
            cur.execute("SELECT followed_id FROM follows WHERE user_id = ?", (current_user_id,))
            followed_ids = [row[0] for row in cur.fetchall()]

            if not followed_ids:
                print("😕 هنوز کسی رو دنبال نکردی.")
                return

            # 👇 حالا فقط پست‌های اون فالو شده‌ها رو بگیر
            placeholders = ','.join(['?'] * len(followed_ids))  # درست‌کردن ?,?,? برای IN
            query = f"""
                SELECT posts.id, users.username, posts.caption, posts.likes, posts.created_at
                FROM posts
                JOIN users ON posts.user_id = users.id
                WHERE posts.user_id IN ({placeholders})
                ORDER BY posts.created_at DESC
                LIMIT 10
            """
            cur.execute(query, followed_ids)
            posts = cur.fetchall()

            if not posts:
                print("📭 هنوز پستی برای دیدن نیست.")
                return

            for post in posts:
                print("\n════════════════════════════")
                print(f"👤 @{post[1]}  🕒 {post[4]}")
                print(f"📝 {post[2]}")
                print(f"❤️ Likes: {post[3]}")

                # کامنت‌ها
                cur.execute("""
                    SELECT users.username, comments.content
                    FROM comments
                    JOIN users ON comments.user_id = users.id
                    WHERE comments.post_id = ?
                """, (post[0],))
                comments = cur.fetchall()
                if comments:
                    print("💬 کامنت‌ها:")
                    for com in comments:
                        print(f"   ─ @{com[0]}: {com[1]}")
                print("════════════════════════════")

    def like_post(self, user_id):
        post_id = input("🆔 شناسه پست موردنظر برای لایک: ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # فقط چک کنیم پست وجود داره
            cur.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
            if not cur.fetchone():
                print("❌ پست پیدا نشد.")
                return

            # بعداً می‌تونی چک کنی کاربر قبلاً لایک کرده یا نه (با جدول جدا)
            cur.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
            conn.commit()
            print("❤️ پست لایک شد!")

    def create_saved_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS saved_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    post_id INTEGER NOT NULL,
                    UNIQUE(user_id, post_id)
                )
            """)
    def save_post(self, user_id):
        post_id = input("🆔 شناسه پست برای ذخیره: ")

        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("INSERT INTO saved_posts (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
                conn.commit()
                print("✅ پست ذخیره شد.")
            except sqlite3.IntegrityError:
                print("⚠️ این پست قبلاً ذخیره شده.")

    def view_saved_posts(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT posts.id, users.username, posts.caption, posts.likes, posts.created_at
                FROM saved_posts
                JOIN posts ON saved_posts.post_id = posts.id
                JOIN users ON posts.user_id = users.id
                WHERE saved_posts.user_id = ?
                ORDER BY posts.created_at DESC
            """, (user_id,))
            posts = cur.fetchall()

        if not posts:
            print("📭 هیچ پستی ذخیره نکردی.")
            return

        print("\n📌 پست‌های ذخیره‌شده:")
        for post in posts:
            print("\n════════════════════════════")
            print(f"👤 @{post[1]}  🕒 {post[4]}")
            print(f"📝 {post[2]}")
            print(f"❤️ Likes: {post[3]}")
            print("════════════════════════════")

    def view_my_posts(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT caption, likes, created_at
                FROM posts
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
            posts = cur.fetchall()

        if not posts:
            print("📭 هنوز پستی منتشر نکردی.")
            return

        print("\n🧑‍💻 پست‌های شما:")

    def view_user_posts_with_ids(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, caption, created_at, likes
                FROM posts
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
            posts = cur.fetchall()

        if not posts:
            print("📭 هیچ پستی برای نمایش نیست.")
            return

        print("\n🗂 لیست پست‌های شما:")
        for post in posts:
            print("\n════════════════════════════")
            print(f"🆔 ID: {post[0]}")
            print(f"📝 {post[1]}")
            print(f"🕒 {post[2]}   ❤️ Likes: {post[3]}")
            print("════════════════════════════")

    def delete_post(self, user_id):
        self.view_user_posts_with_ids(user_id)
        post_id = input("🆔 شناسه پستی که می‌خوای حذف کنی: ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # فقط پستی که مال خود کاربره اجازه حذف داره
            cur.execute("SELECT id FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
            if not cur.fetchone():
                print("❌ همچین پستی پیدا نشد یا متعلق به شما نیست.")
                return

            cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            conn.commit()
            print("✅ پست با موفقیت حذف شد.")

    def edit_post(self, user_id):
        self.view_user_posts_with_ids(user_id)
        post_id = input("🆔 شناسه پستی که می‌خوای ویرایش کنی: ")

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # چک می‌کنیم که پست متعلق به خود کاربر باشه
            cur.execute("SELECT caption FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
            result = cur.fetchone()

            if not result:
                print("❌ پست پیدا نشد یا مال شما نیست.")
                return

            print(f"\n📝 متن فعلی پست:\n{result[0]}")
            new_caption = input("✏️ متن جدید پست: ")

            if not new_caption.strip():
                print("⚠️ متن جدید نمی‌تونه خالی باشه.")
                return

            cur.execute("UPDATE posts SET caption = ? WHERE id = ?", (new_caption.strip(), post_id))
            conn.commit()
            print("✅ پست با موفقیت ویرایش شد.")






