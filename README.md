# SafeCrypt
![SafeCrypt Logo](https://raw.githubusercontent.com/HusseinTahaDEV/SafeCrypt/main/assets/logo.PNG).
SafeCrypt is a professional-grade file encryption and decryption tool designed to provide maximum security and ease of use. With SafeCrypt, you can securely encrypt your sensitive files using strong encryption algorithms and manage your encryption keys with confidence.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/HusseinTahaDEV/SafeCrypt/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/safecrypt.svg)](https://pypi.org/project/safecrypt/)
[![GitHub Issues](https://img.shields.io/github/issues/HusseinTahaDEV/SafeCrypt.svg)](https://github.com/HusseinTahaDEV/SafeCrypt/issues)
[![GitHub Stars](https://img.shields.io/github/stars/HusseinTahaDEV/SafeCrypt.svg)](https://github.com/HusseinTahaDEV/SafeCrypt/stargazers)

## Features

- **Strong Encryption**: Utilizes Fernet symmetric encryption (AES) for robust security.
- **Password Protection**: Password-based key derivation with PBKDF2 and salt for added security.
- **File Compression**: Compresses files before encryption to save space and speed up transfer.
- **Drag-and-Drop Interface**: Intuitive drag-and-drop interface for easy file encryption and decryption.
- **Multi-threading**: Utilizes multi-threading for efficient batch processing of files.
- **Cross-platform**: Works seamlessly on Windows, macOS, and Linux.

## Installation

To install SafeCrypt, clone the repository:

```bash
git clone https://github.com/HusseinTahaDEV/SafeCrypt.git
cd SafeCrypt
```

## Usage

### Terminal Version

1. **Generate Key**:
   ```bash
   python safecrypter.py --generate-key
   ```

2. **Encrypt File**:
   ```bash
   python safecrypter.py --encrypt <file_path>
   ```

3. **Decrypt File**:
   ```bash
   python safecrypter.py --decrypt <file_path>
   ```

### GUI Version

1. Run the GUI version:
   ```bash
   python main.py
   ```

## Updating

To update SafeCrypt to the latest version from GitHub:
```bash
cd SafeCrypt
git pull origin main
```

## Documentation

For detailed documentation and usage instructions, please refer to the [Wiki](https://github.com/HusseinTahaDEV/SafeCrypt/tree/main/wiki).

## Development

To set up the development environment:

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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact [Hussein Taha](mailto:ceo.husseintaha@gmail.com).

---

## Acknowledgements

- Created by Hussein Taha
- GitHub: [HusseinTahaDEV](https://github.com/HusseinTahaDEV)
```

This `README.md` includes all the main parts and follows a professional format. It provides a clear overview of the project, installation instructions, usage examples, updating instructions, and contribution guidelines, making it easy for others to use and contribute to the project.
