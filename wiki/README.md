Got it! I've updated the placeholders with your name and username. Here's the revised wiki:

### Welcome to the SafeCrypt Wiki!

SafeCrypt is a professional-grade file encryption and decryption tool designed to provide maximum security and ease of use. This wiki serves as a comprehensive guide to understanding and using SafeCrypt effectively.

#### Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Generating Encryption Keys](#generating-encryption-keys)
   - [Loading Encryption Keys](#loading-encryption-keys)
   - [Encrypting Files](#encrypting-files)
   - [Decrypting Files](#decrypting-files)
4. [Development](#development)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

---

### Introduction

SafeCrypt is a powerful tool that allows users to encrypt and decrypt their files with ease. It provides strong encryption using the Fernet symmetric encryption algorithm, along with password protection for added security. With SafeCrypt, users can securely store and transfer their sensitive files without worrying about unauthorized access.

### Installation

You can install SafeCrypt via pip:

```bash
pip install safecrypt
```

### Usage

#### Generating Encryption Keys

To generate a new encryption key, follow these steps:

1. Launch SafeCrypt by running the main application script.
2. Click on the "Generate Encryption Key" button.
3. Enter a password for the encryption key when prompted.
4. The generated key will be displayed in the application window, and a corresponding key file (`secret.key`) will be saved in the current directory.

#### Loading Encryption Keys

If you have an existing encryption key saved in a key file, you can load it into SafeCrypt:

1. Launch SafeCrypt by running the main application script.
2. Click on the "Load Encryption Key" button.
3. Select the key file (`*.key`) containing your encryption key.
4. Enter the password for the encryption key when prompted.
5. The loaded key will be used for subsequent encryption and decryption operations.

#### Encrypting Files

To encrypt a file or folder, follow these steps:

1. Launch SafeCrypt by running the main application script.
2. Drag and drop the file or folder you want to encrypt onto the application window.
3. SafeCrypt will compress the file/folder, encrypt it using the loaded encryption key, and save the encrypted file with a `.encrypted` extension.
4. The progress of the encryption process will be displayed in the application window.

#### Decrypting Files

To decrypt an encrypted file, follow these steps:

1. Launch SafeCrypt by running the main application script.
2. Drag and drop the encrypted file onto the application window.
3. SafeCrypt will decrypt the file using the loaded encryption key, decompress it, and save the decrypted file.
4. The progress of the decryption process will be displayed in the application window.

### Development

If you're interested in contributing to SafeCrypt or want to customize it for your specific needs, you can set up the development environment as follows:

1. Clone the repository:
```bash
git clone https://github.com/HusseinTahaDEV/SafeCrypt.git
```

2. Navigate to the project directory and install the requirements:
```bash
cd SafeCrypt
pip install -r requirements.txt
```

3. Run tests to ensure everything is set up correctly:
```bash
python -m unittest discover
```

### Contributing

Contributions to SafeCrypt are welcome! If you have ideas for new features, improvements, or bug fixes, please fork the repository and submit a pull request with your changes.

### License

SafeCrypt is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it according to your needs.

### Contact

For any inquiries, support, or feedback, please contact [Hussein Taha](mailto:ceo.husseintaha@gmail.com).

---

