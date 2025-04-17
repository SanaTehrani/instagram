from modules.auth import AuthManager
from modules.feed import FeedManager
from modules.explore import ExploreManager

explore = ExploreManager()

from modules.profile import ProfileManager
...
profile = ProfileManager()

from modules.messaging import MessageManager
...
messaging = MessageManager()


def main():
    auth = AuthManager()

    while True:
        print("1. ورود")
        print("2. ثبت‌نام")
        print("3. خروج")

        choice = input("انتخاب کن: ")

        if choice == "1":
            user = auth.login()
            if user:
                feed = FeedManager()
                while True:
                    print("\nصفحه اصلی")
                    print("1. دیدن پست‌ها")
                    print("2. ساخت پست")
                    print("3. خروج")

                    choice2 = input("انتخاب: ")
                    if choice2 == "1":
                        feed.show_feed(user.id)
                    elif choice2 == "2":
                        feed.create_post(user.id)
                    elif choice2 == "3":
                        feed.add_comment(user.id)
                    elif choice2 == "4":
                        explore.search_user(user.id)
                    elif choice2 == "5":
                        feed.like_post(user.id)
                    elif choice2 == "6":
                        profile.view_profile(user.id)
                    elif choice2 == "7":
                        profile.edit_profile(user.id)
                    elif choice2 == "8":
                        messaging.send_message(user.id)
                    elif choice2 == "9":
                        messaging.view_inbox(user.id)
                    elif choice2 == "10":
                        feed.save_post(user.id)
                    elif choice2 == "11":
                        feed.view_saved_posts(user.id)
                    elif choice2 == "12":
                        feed.view_user_posts(user.id)
                    elif choice2 == "13":
                        feed.delete_post(user.id)
                    elif choice2 == "15":
                        feed.edit_post(user.id)
                    elif choice2 == "16":
                        break


                    else:
                        print("گزینه نامعتبر")

        elif choice == "2":
            auth.register()
        elif choice == "3":
            print("خروج از برنامه")
            break
        else:
            print("گزینه نامعتبر")
        

print("1. دیدن پست‌ها")
print("2. ساخت پست")
print("3. ثبت کامنت")
print("4. جستجو و دنبال کردن")
print("5. لایک پست")
print("6. مشاهده پروفایل")
print("7. ویرایش پروفایل")
print("8. ارسال پیام")
print("9. صندوق پیام‌ها")
print("10. ذخیره پست")
print("11. دیدن پست‌های ذخیره‌شده")
print("12. دیدن پست‌های من")
print("13. حذف پست")
print("14. ویرایش پست")

print("15. خروج")






if __name__ == "__main__":
    main()
