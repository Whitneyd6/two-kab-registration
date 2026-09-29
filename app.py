import roster


def main():
    while True:
        print("\n=== KAB Attendance Registry ===")
        # MENU OPTIONS GO HERE
        print("1. Add student")
        print("2. Check in student")
        print("3. View today's check-ins")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            roster.add_student_prompt()
        elif choice == "2":
            roster.check_in_prompt()
        elif choice == "3":
            roster.list_today()

if __name__ == "__main__":
    main()