from modules.auth import AuthManager
from modules.feed import FeedManager


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
                        feed.show_feed()
                    elif choice2 == "2":
                        feed.create_post(user.id)
                    elif choice2 == "3":
                        feed.add_comment(user.id)
                    else:
                        print("گزینه نامعتبر")

        elif choice == "2":
            auth.register()
        elif choice == "3":
            print("خروج از برنامه")
            break
        else:
            print("گزینه نامعتبر")
        




if __name__ == "__main__":
    main()
