import sqlite3
from modules.models import Post
from datetime import datetime

DB_PATH = "database/db.sqlite3"

class FeedManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.create_table()
        self.create_comment_table()

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

    def show_feed(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT posts.id, users.username, posts.caption, posts.likes, posts.created_at
                FROM posts
                JOIN users ON posts.user_id = users.id
                ORDER BY posts.created_at DESC
                LIMIT 10
            """)
            posts = cur.fetchall()

            for post in posts:
                print("\n════════════════════════════")
                print(f"کاربر @{post[1]}  زمان {post[4]}")
                print(f"پست {post[2]}")
                print(f"لایک ها: {post[3]}")
                
                cur.execute("""
                    SELECT users.username, comments.content
                    FROM comments
                    JOIN users ON comments.user_id = users.id
                    WHERE comments.post_id = ?
                """, (post[0],))
                comments = cur.fetchall()

            if comments:
                print("کامنت‌ها:")
                for com in comments:
                    print(f"   ─ @{com[0]}: {com[1]}")
            print("════════════════════════════")