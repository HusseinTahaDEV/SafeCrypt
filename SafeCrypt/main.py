# safecrypt/main.py
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QTextEdit,
    QProgressBar,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from .encryption import EncryptionManager
import os
import logging

logging.basicConfig(filename="datalog.log", level=logging.INFO)


class EncryptionWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, file_path, encrypt, manager):
        super().__init__()
        self.file_path = file_path
        self.encrypt = encrypt
        self.manager = manager

    def run(self):
        try:
            if self.encrypt:
                output_path = self.manager.compress_file(self.file_path)
                output_path = self.manager.encrypt_file(output_path)
                os.remove(self.file_path)
                self.finished.emit(f"Encrypted file: {output_path}")
            else:
                zip_path = self.manager.decrypt_file(self.file_path)
                output_path = self.manager.decompress_file(zip_path)
                os.remove(self.file_path)
                self.finished.emit(f"Decrypted file: {output_path}")
        except Exception as e:
            self.finished.emit(f"Error processing file {self.file_path}: {str(e)}")


class DataLock(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SafeCrypt - Simple File Encryption")
        self.setGeometry(100, 100, 600, 400)

        self.encryption_manager = EncryptionManager()
        self.salt = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.infoLabel = QLabel(
            "Drag and drop files or folders here to encrypt/decrypt them."
        )
        self.infoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.infoLabel)

        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)
        layout.addWidget(self.resultText)

        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)

        buttonLayout = QHBoxLayout()

        self.keyButton = QPushButton("Generate Encryption Key")
        self.keyButton.clicked.connect(self.generate_key)
        buttonLayout.addWidget(self.keyButton)

        self.loadKeyButton = QPushButton("Load Encryption Key")
        self.loadKeyButton.clicked.connect(self.load_key)
        buttonLayout.addWidget(self.loadKeyButton)

        self.uploadButton = QPushButton("Select Files/Folders to Encrypt/Decrypt")
        self.uploadButton.clicked.connect(self.open_file_dialog)
        buttonLayout.addWidget(self.uploadButton)

        layout.addLayout(buttonLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.encrypt_decrypt_file(file_path)

    def generate_key(self):
        password, ok = QInputDialog.getText(
            self,
            "Password",
            "Enter a password for the encryption key:",
            QLineEdit.Password,
        )
        if ok:
            key, salt = self.encryption_manager.generate_key(password)
            self.salt = salt
            self.resultText.append(f"Generated Key: {key.decode()}")
            self.encryption_manager.save_key("secret.key", salt)
            logging.info("Encryption key generated and saved.")

    def load_key(self):
        options = QFileDialog.Options()
        key_file, _ = QFileDialog.getOpenFileName(
            self,
            "Load Encryption Key",
            "",
            "Key Files (*.key);;All Files (*)",
            options=options,
        )
        if key_file:
            password, ok = QInputDialog.getText(
                self,
                "Password",
                "Enter the password for the encryption key:",
                QLineEdit.Password,
            )
            if ok:
                try:
                    with open(key_file, "rb") as file:
                        salt = file.read()
                    self.encryption_manager.load_key(password, salt)
                    self.resultText.append(f"Loaded Key from {key_file}")
                    logging.info("Encryption key loaded successfully.")
                except Exception as e:
                    self.resultText.append(f"Error loading key: {str(e)}")
                    logging.error(f"Error loading key: {str(e)}")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files/Folders to Encrypt/Decrypt",
            "",
            "All Files (*)",
            options=options,
        )
        if files:
            self.resultText.append(f"Selected Files: {files}")
            for file in files:
                self.encrypt_decrypt_file(file)

    def encrypt_decrypt_file(self, file_path):
        if self.encryption_manager.key is None:
            self.resultText.append(
                "Error: No encryption key found. Generate or load a key first."
            )
            return

        encrypt = not file_path.endswith(".encrypted")
        self.resultText.append(
            f'{"Encrypting" if encrypt else "Decrypting"} file: {file_path}'
        )
        logging.info(f'{"Encrypting" if encrypt else "Decrypting"} file: {file_path}')

        self.worker = EncryptionWorker(file_path, encrypt, self.encryption_manager)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self, message):
        self.resultText.append(message)
        logging.info(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DataLock()
    ex.show()
    sys.exit(app.exec_())
