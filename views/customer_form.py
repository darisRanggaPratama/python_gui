from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QDateEdit, QComboBox, QSpinBox, 
    QPushButton, QLabel
)
from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtGui import QFont

class CustomerForm(QDialog):
    data_saved = pyqtSignal()
    
    def __init__(self, controller, customer_data=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.customer_data = customer_data
        self.setup_ui()
        
        if customer_data:
            self.populate_form()
    
    def setup_ui(self):
        self.setWindowTitle("Form Customer")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QDateEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#cancelButton {
                background-color: #f44336;
            }
            QPushButton#cancelButton:hover {
                background-color: #da190b;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Tambah Customer" if not self.customer_data else "Edit Customer")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.nik_edit = QLineEdit()
        self.nik_edit.setMaxLength(6)
        form_layout.addRow("NIK:", self.nik_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(50)
        form_layout.addRow("Nama:", self.name_edit)
        
        self.born_edit = QDateEdit()
        self.born_edit.setDate(QDate.currentDate())
        self.born_edit.setCalendarPopup(True)
        form_layout.addRow("Tanggal Lahir:", self.born_edit)
        
        self.active_combo = QComboBox()
        self.active_combo.addItems(["Tidak Aktif", "Aktif"])
        form_layout.addRow("Status:", self.active_combo)
        
        self.salary_spin = QSpinBox()
        self.salary_spin.setRange(0, 999999999)
        self.salary_spin.setSuffix(" IDR")
        form_layout.addRow("Gaji:", self.salary_spin)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Simpan")
        self.save_button.clicked.connect(self.save_customer)
        
        self.cancel_button = QPushButton("Batal")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def populate_form(self):
        if self.customer_data:
            self.nik_edit.setText(self.customer_data['nik'])
            self.name_edit.setText(self.customer_data['name'])
            
            if self.customer_data['born']:
                self.born_edit.setDate(QDate.fromString(str(self.customer_data['born']), "yyyy-MM-dd"))
            
            self.active_combo.setCurrentIndex(self.customer_data['active'])
            self.salary_spin.setValue(self.customer_data['salary'] or 0)
    
    def save_customer(self):
        nik = self.nik_edit.text().strip()
        name = self.name_edit.text().strip()
        born = self.born_edit.date().toPyDate()
        active = self.active_combo.currentIndex()
        salary = self.salary_spin.value()
        
        if not nik or not name:
            self.controller.show_error_message("NIK dan Nama harus diisi!")
            return
        
        if self.customer_data:  # Edit mode
            success = self.controller.update_customer(
                self.customer_data['idx'], nik, name, born, active, salary
            )
        else:  # Add mode
            success = self.controller.create_customer(nik, name, born, active, salary)
        
        if success:
            self.data_saved.emit()
            self.accept()