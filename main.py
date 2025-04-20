from modules.auth import AuthManager
from modules.feed import FeedManager
from modules.explore import ExploreManager
from modules.profile import ProfileManager
from modules.messaging import MessageManager

def main():
    auth = AuthManager()
    explore = ExploreManager()
    profile = ProfileManager()
    messaging = MessageManager()

    while True:
        print("\n👤 حساب کاربری")
        print("1. ورود")
        print("2. ثبت‌نام")
        print("3. خروج")

        choice = input("انتخاب کن: ")

        if choice == "1":
            user = auth.login()
            if user:
                feed = FeedManager()
                while True:
                    print("\n🏠 صفحه اصلی")
                    print("۱. پست‌ها")
                    print("۲. جست‌وجو")
                    print("۳. پروفایل")
                    print("۴. پیام‌ها")
                    print("۵. تنظیمات و خروج")

                    section = input("بخش مورد نظر: ")

                    # --------------------- بخش ۱: پست‌ها ---------------------
                    if section == "1":
                        print("\n📝 مدیریت پست‌ها")
                        print("1. دیدن پست‌ها")
                        print("2. ساخت پست")
                        print("3. ثبت کامنت")
                        print("4. لایک پست")
                        print("5. ذخیره پست")
                        print("6. دیدن پست‌های ذخیره‌شده")
                        print("7. دیدن پست‌های من")
                        print("8. حذف پست")
                        print("9. ویرایش پست")
                        print("10. بازگشت")

                        p = input("انتخاب: ")
                        if p == "1": feed.show_feed(user.id)
                        elif p == "2": feed.create_post(user.id)
                        elif p == "3": feed.add_comment(user.id)
                        elif p == "4": feed.like_post(user.id)
                        elif p == "5": feed.save_post(user.id)
                        elif p == "6": feed.view_saved_posts(user.id)
                        elif p == "7": feed.view_user_posts(user.id)
                        elif p == "8": feed.delete_post(user.id)
                        elif p == "9": feed.edit_post(user.id)
                        elif p == "10": continue
                        else: print("❌ گزینه نامعتبر")

                    # --------------------- بخش ۲: جست‌وجو ---------------------
                    elif section == "2":
                        explore.search_user(user.id)

                    # --------------------- بخش ۳: پروفایل ---------------------
                    elif section == "3":
                        print("\n👤 پروفایل شما")
                        print("1. مشاهده پروفایل")
                        print("2. ویرایش پروفایل")
                        print("3. بازگشت")

                        p = input("انتخاب: ")
                        if p == "1": profile.view_profile(user.id)
                        elif p == "2": profile.edit_profile(user.id)
                        elif p == "3": continue
                        else: print("❌ گزینه نامعتبر")

                    # --------------------- بخش ۴: پیام‌ها ---------------------
                    elif section == "4":
                        print("\n📨 پیام‌ها")
                        print("1. ارسال پیام")
                        print("2. مشاهده صندوق ورودی")
                        print("3. بازگشت")

                        p = input("انتخاب: ")
                        if p == "1": messaging.send_message(user.id)
                        elif p == "2": messaging.view_inbox(user.id)
                        elif p == "3": continue
                        else: print("❌ گزینه نامعتبر")

                    # --------------------- بخش ۵: خروج ---------------------
                    elif section == "5":
                        print("📤 خروج از حساب")
                        break
                    else:
                        print("❌ گزینه نامعتبر")

        elif choice == "2":
            auth.register()

        elif choice == "3":
            print("👋 خروج از برنامه")
            break
        else:
            print("❌ گزینه نامعتبر")

# اجرای اصلی
if __name__ == "__main__":
    main()
