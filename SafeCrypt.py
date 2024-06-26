import sys
import os
import shutil
import subprocess
import colorama
from colorama import Fore, Style
import pyfiglet
import requests

colorama.init(autoreset=True)
REPO_URL = "https://github.com/HusseinTahaDEV/SafeCrypt.git"
# Determine the current working directory where the script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = CURRENT_DIR  # Set the target directory to the current working directory
VERSION_FILE = os.path.join(TARGET_DIR, "version.txt")


def welcome_message():
    print(Fore.CYAN + pyfiglet.figlet_format("SafeCrypt"))
    print(Fore.CYAN + "Welcome to SafeCrypt - Simple File Encryption\n")
    print(Fore.GREEN + "Secure your files with ease using SafeCrypt.")
    print(Fore.YELLOW + "Created by: Hussein Taha")
    print(Fore.YELLOW + "GitHub: https://github.com/HusseinTahaDEV\n")
    print(Fore.GREEN + "Choose an option to continue:\n")
    print(Fore.YELLOW + "1. Use GUI version")
    print(Fore.YELLOW + "2. Use Terminal version")
    print(Fore.YELLOW + "3. Check for updates")
    print(Fore.RED + "4. Exit\n")


def clear_screen():
    if os.name == "posix":  # Linux/Unix/MacOS
        _ = subprocess.call("clear", shell=True)
    elif os.name == "nt":  # Windows
        _ = subprocess.call("cls", shell=True)


def fetch_latest_version():
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/HusseinTahaDEV/SafeCrypt/main/version.txt"
        )
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(
                Fore.RED
                + f"Failed to fetch latest version information. Status code: {response.status_code}"
            )
    except Exception as e:
        print(
            Fore.RED + f"An error occurred while fetching version information: {str(e)}"
        )


def read_local_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as file:
            return file.read().strip()
    return None


def clear_directory(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, onerror=remove_readonly)
            except Exception as e:
                print(Fore.RED + f"Failed to delete {file_path}. Reason: {e}")
                return False
    except Exception as e:
        print(Fore.RED + f"Failed to clear directory {directory}: {e}")
        return False
    return True


def remove_readonly(func, path, exc_info):
    os.chmod(path, 0o777)
    func(path)


def update_safe_crypt():
    try:
        print(Fore.GREEN + f"Updating SafeCrypt in {TARGET_DIR}...")
        if not clear_directory(TARGET_DIR):
            print(Fore.RED + f"Failed to clear directory {TARGET_DIR}.")
            return False
        subprocess.run(["git", "clone", REPO_URL, TARGET_DIR], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to update SafeCrypt: {e}")
        return False
    return True


def check_updates():
    try:
        print(Fore.GREEN + "Checking for updates...")
        latest_version = fetch_latest_version()
        if latest_version:
            current_version = read_local_version()
            if not current_version or current_version != latest_version:
                print(Fore.YELLOW + f"New version {latest_version} is available.")
                update_choice = (
                    input(Fore.YELLOW + "Do you want to update? (yes/no): ")
                    .strip()
                    .lower()
                )
                if update_choice == "yes":
                    if not update_safe_crypt():
                        print(Fore.RED + "Failed to update SafeCrypt.")
                else:
                    print(
                        Fore.GREEN
                        + "Skipping update. SafeCrypt will remain at the current version."
                    )
            else:
                print(Fore.GREEN + "SafeCrypt is up to date.")
    except KeyboardInterrupt:
        print(Fore.RED + "\nUpdate process interrupted.")
    input(Fore.YELLOW + "Press Enter to continue...")


def main():
    try:
        clear_screen()
        welcome_message()
        choice = input(Fore.CYAN + "Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            print(Fore.GREEN + "Launching GUI version...")
            subprocess.run(["python", "Scripts/GUI.py"])
        elif choice == "2":
            print(Fore.GREEN + "Launching Terminal version...")
            subprocess.run(["python", "Scripts/safecrypter.py"])
        elif choice == "3":
            check_updates()
        elif choice == "4":
            print(Fore.GREEN + "Exiting SafeCrypt. Have a great day!")
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice. Please select 1, 2, 3, or 4.")
            main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
