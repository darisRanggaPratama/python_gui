import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QTableWidget, QTableWidgetItem, QPushButton, 
    QLineEdit, QComboBox, QLabel, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from controllers.customer_controller import CustomerController
from views.customer_form import CustomerForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = CustomerController()
        self.controller.data_changed.connect(self.load_data)
        
        self.current_page = 1
        self.per_page = 10
        self.total_records = 0
        self.total_pages = 0
        self.search_term = ""
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        self.setWindowTitle("Customer Management System")
        self.setGeometry(100, 100, 1200, 700)
        
        # Modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #e0e0e0;
                font-size: 12px;
                color: black;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QTableWidget QHeaderView::section {
                background-color: #2196f3;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QPushButton#addButton {
                background-color: #4caf50;
            }
            QPushButton#addButton:hover {
                background-color: #45a049;
            }
            QPushButton#deleteButton {
                background-color: #f44336;
            }
            QPushButton#deleteButton:hover {
                background-color: #da190b;
            }
            QPushButton#editButton {
                background-color: #ff9800;
            }
            QPushButton#editButton:hover {
                background-color: #f57c00;
            }
            QPushButton#uploadButton {
                background-color: #9c27b0;
            }
            QPushButton#uploadButton:hover {
                background-color: #7b1fa2;
            }
            QPushButton#downloadButton {
                background-color: #607d8b;
            }
            QPushButton#downloadButton:hover {
                background-color: #455a64;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #2196f3;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
                min-width: 80px;
            }
            QComboBox:focus {
                border-color: #2196f3;
            }
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 12px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Customer Management System")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Top controls layout
        top_layout = QHBoxLayout()
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Pencarian:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari berdasarkan NIK, Nama, Tanggal Lahir, Status, atau Gaji...")
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(self.search_input)
        
        top_layout.addLayout(search_layout)
        top_layout.addStretch()
        
        # Per page combo
        per_page_layout = QHBoxLayout()
        per_page_layout.addWidget(QLabel("Tampilkan:"))
        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["1", "5", "10", "25", "50", "100"])
        self.per_page_combo.setCurrentText("10")
        self.per_page_combo.currentTextChanged.connect(self.on_per_page_changed)
        per_page_layout.addWidget(self.per_page_combo)
        per_page_layout.addWidget(QLabel("baris"))
        
        top_layout.addLayout(per_page_layout)
        main_layout.addLayout(top_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Tambah Data")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_customer)
        button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edit Data")
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(self.edit_customer)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Hapus Data")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_customer)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.setObjectName("uploadButton")
        self.upload_button.clicked.connect(self.upload_csv)
        button_layout.addWidget(self.upload_button)
        
        self.download_button = QPushButton("Download CSV")
        self.download_button.setObjectName("downloadButton")
        self.download_button.clicked.connect(self.download_csv)
        button_layout.addWidget(self.download_button)
        
        main_layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "NIK", "Nama", "Tanggal Lahir", "Status", "Gaji"])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.edit_customer)
        
        main_layout.addWidget(self.table)
        
        # Pagination layout
        pagination_layout = QHBoxLayout()
        
        self.info_label = QLabel()
        pagination_layout.addWidget(self.info_label)
        
        pagination_layout.addStretch()
        
        self.prev_button = QPushButton("◀ Sebelumnya")
        self.prev_button.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_button)
        
        self.page_label = QLabel()
        pagination_layout.addWidget(self.page_label)
        
        self.next_button = QPushButton("Selanjutnya ▶")
        self.next_button.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_button)
        
        main_layout.addLayout(pagination_layout)
        
        # Search timer for delayed search
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
    
    def load_data(self):
        customers, total_records = self.controller.get_customers(
            page=self.current_page, 
            per_page=self.per_page, 
            search_term=self.search_term
        )
        
        self.total_records = total_records
        self.total_pages = max(1, (total_records + self.per_page - 1) // self.per_page)
        
        # Update table
        self.table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer['idx'])))
            self.table.setItem(row, 1, QTableWidgetItem(customer['nik']))
            self.table.setItem(row, 2, QTableWidgetItem(customer['name']))
            
            born_str = customer['born'].strftime('%d-%m-%Y') if customer['born'] else ''
            self.table.setItem(row, 3, QTableWidgetItem(born_str))
            
            status_str = "Aktif" if customer['active'] else "Tidak Aktif"
            self.table.setItem(row, 4, QTableWidgetItem(status_str))
            
            salary_str = f"Rp {customer['salary']:,}" if customer['salary'] else "Rp 0"
            self.table.setItem(row, 5, QTableWidgetItem(salary_str))
        
        # Update pagination info
        start_record = (self.current_page - 1) * self.per_page + 1
        end_record = min(self.current_page * self.per_page, total_records)
        
        if total_records > 0:
            self.info_label.setText(f"Menampilkan {start_record}-{end_record} dari {total_records} data")
        else:
            self.info_label.setText("Tidak ada data")
        
        self.page_label.setText(f"Halaman {self.current_page} dari {self.total_pages}")
        
        # Update button states
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)
        
        # Clear selection
        self.table.clearSelection()
        self.on_selection_changed()
    
    def on_selection_changed(self):
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def on_search_changed(self):
        self.search_timer.stop()
        self.search_timer.start(500)  # 500ms delay
    
    def perform_search(self):
        self.search_term = self.search_input.text().strip()
        self.current_page = 1
        self.load_data()
    
    def on_per_page_changed(self, value):
        self.per_page = int(value)
        self.current_page = 1
        self.load_data()
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()
    
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()
    
    def add_customer(self):
        form = CustomerForm(self.controller, parent=self)
        form.data_saved.connect(self.load_data)
        form.exec()
    
    def edit_customer(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            customer_id = int(self.table.item(current_row, 0).text())
            customer_data = self.controller.get_customer(customer_id)
            
            if customer_data:
                form = CustomerForm(self.controller, customer_data, parent=self)
                form.data_saved.connect(self.load_data)
                form.exec()
    
    def delete_customer(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            customer_id = int(self.table.item(current_row, 0).text())
            self.controller.delete_customer(customer_id)
    
    def upload_csv(self):
        self.controller.import_csv(self)
    
    def download_csv(self):
        self.controller.export_csv(self)

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Customer Management System")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PyQt6 CRUD")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
