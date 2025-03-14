import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class CompressThread(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal(str)

    def run(self):
        for i in range(1, 101):
            time.sleep(0.05)
            self.progress.emit(i)
        self.done.emit("File_compressed")


class CompressingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Compressing Tool")
        self.setStyleSheet("background-color: #222; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        self.label = QLabel("Compressing Tool")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.file_type = QComboBox()
        self.file_type.addItems(["PDF", "PIC", "TXT", "CSV"])
        self.file_type.setStyleSheet("background: white; color: black;")
        layout.addWidget(self.file_type)

        self.choose_file_btn = QPushButton("Choose files or drop files here")
        self.choose_file_btn.setStyleSheet("background: blue; color: white; padding: 10px; border-radius: 5px;")
        self.choose_file_btn.clicked.connect(self.chon_file)
        layout.addWidget(self.choose_file_btn)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.download_btn = QPushButton("Download")
        self.download_btn.setStyleSheet("background: green; color: white; padding: 10px; border-radius: 5px;")
        self.download_btn.clicked.connect(self.start_compression)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    def chon_file(self):
        file_filter = {
            "PDF": "*.pdf",
            "PIC": "*.png *.jpg *.jpeg",
            "TXT": "*.txt",
            "CSV": "*.csv"
        }

        file_type = self.file_type.currentText()
        filters = file_filter[file_type]
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose File", "", filters)

        if file_name:
            self.choose_file_btn.setText(file_name)
            self.selected_file = file_name

    def start_compression(self):
        self.thread = CompressThread()
        self.thread.progress.connect(self.cap_nhat_progress)
        self.thread.done.connect(self.show_done)
        self.thread.start()

    def cap_nhat_progress(self, value):
        self.progress.setValue(value)

    def show_done(self, file_name):
        file_type = self.file_type.currentText().lower()
        msg = QMessageBox()
        msg.setWindowTitle("Done")
        msg.setText(f"✅ Done\n{file_name}.{file_type}")
        msg.setStyleSheet("background: white; color: black; font-size: 14px;")
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompressingTool()
    window.show()
    sys.exit(app.exec())
