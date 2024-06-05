from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64
import os
import zipfile


class EncryptionManager:
    def __init__(self):
        self.key = None

    def generate_key(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        return key, salt

    def load_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key

    def save_key(self, key_file, salt):
        with open(key_file, "wb") as file:
            file.write(salt)

    def encrypt_file(self, file_path, output_dir):
        try:
            fernet = Fernet(self.key)
            with open(file_path, "rb") as file:
                data = file.read()
            encrypted_data = fernet.encrypt(data)
            output_path = os.path.join(
                output_dir, os.path.basename(file_path) + ".encrypted"
            )
            with open(output_path, "wb") as file:
                file.write(encrypted_data)
            return output_path
        except Exception as e:
            raise Exception(f"Error encrypting file: {str(e)}")

    def decrypt_file(self, file_path, output_dir):
        try:
            fernet = Fernet(self.key)
            with open(file_path, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            output_path = os.path.join(
                output_dir, os.path.basename(file_path).replace(".encrypted", "")
            )
            with open(output_path, "wb") as file:
                file.write(decrypted_data)
            return output_path
        except Exception as e:
            raise Exception(f"Error decrypting file: {str(e)}")

    def compress_folder(self, folder_path):
        try:
            zip_path = folder_path + ".zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(
                            os.path.join(root, file),
                            os.path.relpath(
                                os.path.join(root, file),
                                os.path.join(folder_path, ".."),
                            ),
                        )
            return zip_path
        except Exception as e:
            raise Exception(f"Error compressing folder: {str(e)}")

    def decompress_file(self, zip_path, output_dir):
        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(output_dir)
            return zip_path.replace(".zip", "")
        except Exception as e:
            raise Exception(f"Error decompressing file: {str(e)}")
