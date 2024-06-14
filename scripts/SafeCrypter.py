import sys
import os
import argparse
import logging
import subprocess
from encryption import EncryptionManager
import colorama
from colorama import Fore, Style
import pyfiglet

colorama.init(autoreset=True)


def welcome_message():
    print(Fore.CYAN + pyfiglet.figlet_format("SafeCrypt"))
    print(Fore.CYAN + "Welcome to SafeCrypt - Simple File Encryption\n")
    print(Fore.GREEN + "Secure your files with ease using SafeCrypt.")
    print(Fore.GREEN + "Choose an option to continue:\n")
    print(Fore.RED + "((WARNING))")
    print(Fore.YELLOW + "")
    print(Fore.YELLOW + "this CLI version is experimental")
    print(Fore.YELLOW + "some features may not work as expected ")
    print(Fore.YELLOW + "")


def clear_screen():
    if os.name == "posix":  # Linux/Unix/MacOS
        _ = subprocess.call("clear", shell=True)
    elif os.name == "nt":  # Windows
        _ = subprocess.call("cls", shell=True)


def generate_key(args):
    manager = EncryptionManager()
    key, salt = manager.generate_key(args.password)
    manager.save_key("secret.key", salt)
    logging.info("Encryption key generated and saved.")
    print(Fore.GREEN + f"Generated Key: {key.decode()}")


def load_key(args):
    manager = EncryptionManager()
    if args.key_file and args.salt_file:
        with open(args.salt_file, "rb") as file:
            salt = file.read()
    else:
        raise ValueError("Key file and salt file must be provided.")

    manager.load_key(args.password, salt)
    logging.info("Encryption key loaded successfully.")
    print(Fore.GREEN + f"Loaded Key from {args.key_file}")
    return manager


def encrypt_file(args, manager):
    try:
        if os.path.isdir(args.input):
            output_path = manager.compress_folder(args.input)
            encrypted_path = manager.encrypt_file(output_path, args.output)
            os.remove(output_path)
        else:
            encrypted_path = manager.encrypt_file(args.input, args.output)
        print(Fore.GREEN + f"Encrypted file saved at: {encrypted_path}")
        logging.info(f"Encrypted file saved at: {encrypted_path}")
    except Exception as e:
        print(Fore.RED + f"Error encrypting file: {str(e)}")
        logging.error(f"Error encrypting file: {str(e)}")


def decrypt_file(args, manager):
    try:
        decrypted_path = manager.decrypt_file(args.input, args.output)
        if decrypted_path.endswith(".zip"):
            output_path = manager.decompress_file(decrypted_path, args.output)
            os.remove(decrypted_path)
        else:
            output_path = decrypted_path
        print(Fore.GREEN + f"Decrypted file saved at: {output_path}")
        logging.info(f"Decrypted file saved at: {output_path}")
    except Exception as e:
        print(Fore.RED + f"Error decrypting file: {str(e)}")
        logging.error(f"Error decrypting file: {str(e)}")


def main():
    clear_screen()

    welcome_message()

    parser = argparse.ArgumentParser(
        description=Fore.CYAN + "SafeCrypt - Simple File Encryption",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate key command
    parser_generate_key = subparsers.add_parser(
        "generate-key", help=Fore.YELLOW + "Generate a new encryption key"
    )
    parser_generate_key.add_argument(
        "-p",
        "--password",
        required=True,
        help=Fore.YELLOW + "Password for the encryption key",
    )
    parser_generate_key.set_defaults(func=generate_key)

    # Load key command
    parser_load_key = subparsers.add_parser(
        "load-key", help=Fore.YELLOW + "Load an existing encryption key"
    )
    parser_load_key.add_argument(
        "-p",
        "--password",
        required=True,
        help=Fore.YELLOW + "Password for the encryption key",
    )
    parser_load_key.add_argument(
        "-k", "--key-file", required=True, help=Fore.YELLOW + "Path to the key file"
    )
    parser_load_key.add_argument(
        "-s", "--salt-file", required=True, help=Fore.YELLOW + "Path to the salt file"
    )
    parser_load_key.set_defaults(func=load_key)

    # Encrypt command
    parser_encrypt = subparsers.add_parser(
        "encrypt", help=Fore.YELLOW + "Encrypt a file or folder"
    )
    parser_encrypt.add_argument(
        "-p",
        "--password",
        required=True,
        help=Fore.YELLOW + "Password for the encryption key",
    )
    parser_encrypt.add_argument(
        "-k", "--key-file", required=True, help=Fore.YELLOW + "Path to the key file"
    )
    parser_encrypt.add_argument(
        "-s", "--salt-file", required=True, help=Fore.YELLOW + "Path to the salt file"
    )
    parser_encrypt.add_argument(
        "-i",
        "--input",
        required=True,
        help=Fore.YELLOW + "Path to the input file or folder",
    )
    parser_encrypt.add_argument(
        "-o",
        "--output",
        required=True,
        help=Fore.YELLOW + "Path to the output directory",
    )
    parser_encrypt.set_defaults(func=encrypt_file)

    # Decrypt command
    parser_decrypt = subparsers.add_parser(
        "decrypt", help=Fore.YELLOW + "Decrypt a file or folder"
    )
    parser_decrypt.add_argument(
        "-p",
        "--password",
        required=True,
        help=Fore.YELLOW + "Password for the encryption key",
    )
    parser_decrypt.add_argument(
        "-k", "--key-file", required=True, help=Fore.YELLOW + "Path to the key file"
    )
    parser_decrypt.add_argument(
        "-s", "--salt-file", required=True, help=Fore.YELLOW + "Path to the salt file"
    )
    parser_decrypt.add_argument(
        "-i",
        "--input",
        required=True,
        help=Fore.YELLOW + "Path to the input file or folder",
    )
    parser_decrypt.add_argument(
        "-o",
        "--output",
        required=True,
        help=Fore.YELLOW + "Path to the output directory",
    )
    parser_decrypt.set_defaults(func=decrypt_file)

    # If no command is provided, display help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "generate-key":
        args.func(args)
    elif args.command == "load-key":
        manager = args.func(args)
    elif args.command == "encrypt":
        manager = load_key(args)
        encrypt_file(args, manager)
    elif args.command == "decrypt":
        manager = load_key(args)
        decrypt_file(args, manager)


if __name__ == "__main__":
    main()
