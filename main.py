import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QTextEdit, QComboBox, QLabel, 
                               QLineEdit, QHBoxLayout)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from config import API_KEY, EDUCATION_SITES, ECOMMERCE_SITES, DANGEROUS_SITES
from safe_browsing import SafeBrowsingChecker
import os
import sys


class CheckerThread(QThread):
    result_ready = Signal(list)
    
    def __init__(self, checker, urls):
        super().__init__()
        self.checker = checker
        self.urls = urls
    
    def run(self):
        results = self.checker.check_urls(self.urls)
        self.result_ready.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.checker = SafeBrowsingChecker(API_KEY)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Audit Website")
        self.setMinimumSize(700, 600)

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        
        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Dropdown Section
        label = QLabel("Pilih Kategori Website:")
        layout.addWidget(label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Website Pendidikan", "Website E-Commerce", "Website Berbahaya"])
        layout.addWidget(self.category_combo)
        
        self.check_button = QPushButton("Scan Kategori")
        self.check_button.clicked.connect(self.start_check_category)
        layout.addWidget(self.check_button)
        
        # Manual Input Section
        manual_label = QLabel("Atau Input URL Manual:")
        layout.addWidget(manual_label)
        
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        input_layout.addWidget(self.url_input)
        
        self.manual_button = QPushButton("Scan URL")
        self.manual_button.clicked.connect(self.start_check_manual)
        input_layout.addWidget(self.manual_button)
        
        layout.addLayout(input_layout)
        
        # Result area
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        central_widget.setLayout(layout)
    
    def start_check_category(self):
        self.check_button.setEnabled(False)
        self.manual_button.setEnabled(False)
        self.result_text.clear()
        self.result_text.append("Memulai scanning...\n")
        
        if self.category_combo.currentText() == "Website Pendidikan":
            urls = EDUCATION_SITES
            category = "Pendidikan"
        elif self.category_combo.currentText() == "Website E-Commerce":
            urls = ECOMMERCE_SITES
            category = "E-Commerce"
        elif self.category_combo.currentText() == "Website Berbahaya":
            urls = DANGEROUS_SITES
            category = "Berbahaya"
        
        self.result_text.append(f"Kategori: {category}\n")
        self.result_text.append("=" * 50 + "\n")
        
        self.thread = CheckerThread(self.checker, urls)
        self.thread.result_ready.connect(self.display_results)
        self.thread.start()
    
    def start_check_manual(self):
        url = self.url_input.text().strip()
        
        if not url:
            self.result_text.clear()
            self.result_text.append("⚠️ Error: URL tidak boleh kosong!")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.check_button.setEnabled(False)
        self.manual_button.setEnabled(False)
        self.result_text.clear()
        self.result_text.append("Memulai scanning...\n")
        self.result_text.append(f"URL: {url}\n")
        self.result_text.append("=" * 50 + "\n")
        
        self.thread = CheckerThread(self.checker, [url])
        self.thread.result_ready.connect(self.display_results)
        self.thread.start()
    
    def display_results(self, results):
        for url, is_safe, threats in results:
            if is_safe is None:
                self.result_text.append(f"⚠️ {url}")
                self.result_text.append(f"   Status: Error - {threats[0]}\n")
            elif is_safe:
                self.result_text.append(f"✅ {url}")
                self.result_text.append(f"   Status: Aman\n")
            else:
                self.result_text.append(f"⚠️ {url}")
                self.result_text.append(f"   Status: Terdeteksi Ancaman")
                self.result_text.append(f"   Jenis: {', '.join(threats)}\n")
        
        self.result_text.append("=" * 50)
        self.result_text.append("\nScan selesai!")
        self.check_button.setEnabled(True)
        self.manual_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()