from models.customer import Customer
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import QObject, pyqtSignal

class CustomerController(QObject):
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.model = Customer()
    
    def get_customers(self, page=1, per_page=10, search_term=""):
        return self.model.get_all_customers(page, per_page, search_term)
    
    def get_customer(self, idx):
        return self.model.get_customer_by_id(idx)
    
    def create_customer(self, nik, name, born, active, salary):
        if self.model.create_customer(nik, name, born, active, salary):
            self.data_changed.emit()
            self.show_success_message("Data berhasil disimpan!")
            return True
        else:
            self.show_error_message("Gagal menyimpan data!")
            return False
    
    def update_customer(self, idx, nik, name, born, active, salary):
        reply = self.show_confirmation_message("Konfirmasi", "Apakah Anda yakin ingin mengubah data ini?")
        if reply == QMessageBox.StandardButton.Yes:
            if self.model.update_customer(idx, nik, name, born, active, salary):
                self.data_changed.emit()
                self.show_success_message("Data berhasil diubah!")
                return True
            else:
                self.show_error_message("Gagal mengubah data!")
                return False
        return False
    
    def delete_customer(self, idx):
        reply = self.show_confirmation_message("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if reply == QMessageBox.StandardButton.Yes:
            if self.model.delete_customer(idx):
                self.data_changed.emit()
                self.show_success_message("Data berhasil dihapus!")
                return True
            else:
                self.show_error_message("Gagal menghapus data!")
                return False
        return False
    
    def import_csv(self, parent_widget):
        file_path, _ = QFileDialog.getOpenFileName(
            parent_widget, 
            "Pilih File CSV", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            reply = self.show_confirmation_message("Konfirmasi", "Apakah Anda yakin ingin mengimpor data dari CSV?")
            if reply == QMessageBox.StandardButton.Yes:
                success_count, error_count = self.model.import_from_csv(file_path)
                self.data_changed.emit()
                message = f"Import selesai!\nBerhasil: {success_count} data\nGagal: {error_count} data"
                self.show_success_message(message)
                return True
        return False
    
    def export_csv(self, parent_widget):
        file_path, _ = QFileDialog.getSaveFileName(
            parent_widget, 
            "Simpan File CSV", 
            "customers.csv", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            reply = self.show_confirmation_message("Konfirmasi", "Apakah Anda yakin ingin mengekspor data ke CSV?")
            if reply == QMessageBox.StandardButton.Yes:
                success_count, error_count = self.model.export_to_csv(file_path)
                message = f"Export selesai!\nBerhasil: {success_count} data\nGagal: {error_count} data"
                self.show_success_message(message)
                return True
        return False
    
    def show_success_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Sukses")
        msg_box.setText(message)
        msg_box.exec()
    
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()
    
    def show_confirmation_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        return msg_box.exec()