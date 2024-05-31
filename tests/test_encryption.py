# tests/test_encryption.py
import unittest
from safecrypt.encryption import EncryptionManager
import os


class TestEncryptionManager(unittest.TestCase):
    def setUp(self):
        self.manager = EncryptionManager()
        self.password = "testpassword"
        self.file_content = b"This is a test file."

        with open("testfile.txt", "wb") as f:
            f.write(self.file_content)

    def tearDown(self):
        if os.path.exists("testfile.txt"):
            os.remove("testfile.txt")
        if os.path.exists("testfile.txt.encrypted"):
            os.remove("testfile.txt.encrypted")
        if os.path.exists("testfile.txt.zip"):
            os.remove("testfile.txt.zip")
        if os.path.exists("secret.key"):
            os.remove("secret.key")

    def test_generate_and_load_key(self):
        key, salt = self.manager.generate_key(self.password)
        self.manager.save_key("secret.key", salt)

        self.manager.load_key(self.password, salt)
        self.assertEqual(self.manager.key, key)

    def test_encrypt_and_decrypt_file(self):
        key, salt = self.manager.generate_key(self.password)
        self.manager.save_key("secret.key", salt)

        self.manager.load_key(self.password, salt)
        zip_path = self.manager.compress_file("testfile.txt")
        enc_path = self.manager.encrypt_file(zip_path)
        dec_path = self.manager.decrypt_file(enc_path)
        self.manager.decompress_file(dec_path)

        with open("testfile.txt", "rb") as f:
            content = f.read()

        self.assertEqual(content, self.file_content)


if __name__ == "__main__":
    unittest.main()
