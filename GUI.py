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
    QDialog,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from encryption import EncryptionManager
import os
import logging

logging.basicConfig(filename="datalog.log", level=logging.INFO)


class EncryptionWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, file_path, encrypt, manager, output_dir):
        super().__init__()
        self.file_path = file_path
        self.encrypt = encrypt
        self.manager = manager
        self.output_dir = output_dir

    def run(self):
        try:
            if self.encrypt:
                if os.path.isdir(self.file_path):
                    output_path = self.manager.compress_folder(self.file_path)
                    encrypted_path = self.manager.encrypt_file(
                        output_path, self.output_dir
                    )
                    os.remove(output_path)
                else:
                    encrypted_path = self.manager.encrypt_file(
                        self.file_path, self.output_dir
                    )
                self.finished.emit(f"Encrypted file saved at: {encrypted_path}")
            else:
                decrypted_path = self.manager.decrypt_file(
                    self.file_path, self.output_dir
                )
                if decrypted_path.endswith(".zip"):
                    output_path = self.manager.decompress_file(
                        decrypted_path, self.output_dir
                    )
                    os.remove(decrypted_path)
                else:
                    output_path = decrypted_path
                self.finished.emit(f"Decrypted file saved at: {output_path}")
        except Exception as e:
            self.finished.emit(f"Error processing file {self.file_path}: {str(e)}")
            logging.error(f"Error processing file {self.file_path}: {str(e)}")


class DataLock(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataLock - Simple File Encryption")
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

        self.uploadButton = QPushButton("Import Files/Folders")
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
            self.encrypt_decrypt_prompt(file_path)

    def generate_key(self):
        password, ok = QInputDialog.getText(
            self,
            "Password",
            "Enter a password for the encryption key:",
            QLineEdit.Password,
        )
        if ok:
            try:
                key, salt = self.encryption_manager.generate_key(password)
                self.salt = salt
                self.resultText.append(f"Generated Key: {key.decode()}")
                self.encryption_manager.save_key("secret.key", salt)
                logging.info("Encryption key generated and saved.")
            except Exception as e:
                self.resultText.append(f"Error generating key: {str(e)}")
                logging.error(f"Error generating key: {str(e)}")

    def load_key(self):
        layout = QVBoxLayout()
        self.manualKeyInput = QLineEdit()
        self.manualKeyInput.setPlaceholderText("Enter key manually")
        layout.addWidget(self.manualKeyInput)

        browseKeyButton = QPushButton("Browse for Key File")
        browseKeyButton.clicked.connect(self.browse_for_key)
        layout.addWidget(browseKeyButton)

        dialog = QDialog(self)
        dialog.setWindowTitle("Load Encryption Key")
        dialog.setLayout(layout)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Close the dialog if the user successfully loaded the key
            dialog.accept()

    def browse_for_key(self):
        options = QFileDialog.Options()
        key_file, _ = QFileDialog.getOpenFileName(
            self, "Load Encryption Key", "", "All Files (*)", options=options
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
        else:
            key = self.manualKeyInput.text().encode()
            if key:
                password, ok = QInputDialog.getText(
                    self,
                    "Password",
                    "Enter the password for the encryption key:",
                    QLineEdit.Password,
                )
                if ok:
                    try:
                        self.encryption_manager.load_key(password, key)
                        self.resultText.append("Key loaded successfully.")
                        logging.info("Encryption key loaded successfully.")
                    except Exception as e:
                        self.resultText.append(f"Error loading key: {str(e)}")
                        logging.error(f"Error loading key: {str(e)}")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files/Folders to Import", "", "All Files (*)", options=options
        )
        if files:
            self.resultText.append(f"Selected Files: {files}")
            for file in files:
                self.encrypt_decrypt_prompt(file)

    def encrypt_decrypt_prompt(self, file_path):
        if self.encryption_manager.key is None:
            self.resultText.append(
                "Error: No encryption key found. Generate or load a key first."
            )
            return

        response, ok = QInputDialog.getItem(
            self,
            "Encrypt or Decrypt",
            "Choose action:",
            ["Encrypt", "Decrypt"],
            0,
            False,
        )
        if ok:
            encrypt = response == "Encrypt"
            self.resultText.append(f"{response}ing file: {file_path}")
            logging.info(f"{response}ing file: {file_path}")

            options = QFileDialog.Options()
            output_dir = QFileDialog.getExistingDirectory(
                self, "Select Directory to Save File", options=options
            )
            if output_dir:
                self.worker = EncryptionWorker(
                    file_path, encrypt, self.encryption_manager, output_dir
                )
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
