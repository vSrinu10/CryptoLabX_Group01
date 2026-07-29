import os
from utils.file_analysis import analyze_file
from utils.logger import write_log

def menu():
    while True:
        print("\n===== CryptoLabX =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze File")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Coming Soon")
            write_log("Encrypt")

        elif choice == "2":
            print("Coming Soon")
            write_log("Decrypt")

        elif choice == "3":
            print("Coming Soon")
            write_log("Attack")

        elif choice == "4":
            filename = input("Enter filename: ")
            path = os.path.join("datasets", filename)

            if os.path.exists(path):
                analyze_file(path)
                write_log("Analyze")
            else:
                print("File not found.")

        elif choice == "5":
            write_log("Exit")
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()

