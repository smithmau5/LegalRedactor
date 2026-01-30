import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QListWidget, 
                             QProgressBar, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from redactor_engine import RedactorEngine

class RedactionWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, files):
        super().__init__()
        self.files = files
        self.engine = RedactorEngine()

    def run(self):
        total = len(self.files)
        for i, file_path in enumerate(self.files):
            self.log.emit(f"Processing {os.path.basename(file_path)}...")
            try:
                base, ext = os.path.splitext(file_path)
                output_path = f"{base}_redacted{ext}"
                
                if ext.lower() == '.pdf':
                    self.engine.redact_pdf(file_path, output_path)
                elif ext.lower() == '.docx':
                    self.engine.redact_docx(file_path, output_path)
                
                self.log.emit(f"Saved to {os.path.basename(output_path)}")
            except Exception as e:
                self.log.emit(f"Error processing {os.path.basename(file_path)}: {str(e)}")
            
            self.progress.emit(int((i + 1) / total * 100))
        
        self.finished.emit()

class DragDropWidget(QWidget):
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.label = QLabel("Drag & Drop PDF or DOCX files here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; padding: 20px; font-size: 16px; color: #555;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.pdf', '.docx')):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Legal Doc Redactor")
        self.resize(600, 500)
        self.files = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Dropzone
        self.dropzone = DragDropWidget()
        self.dropzone.files_dropped.connect(self.add_files)
        layout.addWidget(self.dropzone)

        # List of files
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear List")
        self.clear_btn.clicked.connect(self.clear_list)
        btn_layout.addWidget(self.clear_btn)

        self.start_btn = QPushButton("Start Redaction")
        self.start_btn.clicked.connect(self.start_redaction)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_layout.addWidget(self.start_btn)
        layout.addLayout(btn_layout)

        # Progress and Log
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def add_files(self, new_files):
        for f in new_files:
            if f not in self.files:
                self.files.append(f)
                self.file_list.addItem(f)
        self.status_label.setText(f"{len(self.files)} files queued.")

    def clear_list(self):
        self.files = []
        self.file_list.clear()
        self.status_label.setText("List cleared.")

    def start_redaction(self):
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please add files first.")
            return

        self.start_btn.setEnabled(False)
        self.dropzone.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.worker = RedactionWorker(self.files)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.log.connect(self.status_label.setText)
        self.worker.finished.connect(self.redaction_finished)
        self.worker.start()

    def redaction_finished(self):
        self.start_btn.setEnabled(True)
        self.dropzone.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.status_label.setText("Redaction complete!")
        QMessageBox.information(self, "Done", "All files processed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
