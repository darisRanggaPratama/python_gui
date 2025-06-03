from config.database import DatabaseConfig
from mysql.connector import Error
import csv
from datetime import datetime

class Customer:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def get_all_customers(self, page=1, per_page=10, search_term=""):
        connection = self.db_config.get_connection()
        if not connection:
            return [], 0
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Build search condition
            search_condition = ""
            search_params = []
            
            if search_term:
                search_condition = """
                WHERE nik LIKE %s OR name LIKE %s OR 
                      DATE_FORMAT(born, '%Y-%m-%d') LIKE %s OR 
                      active LIKE %s OR salary LIKE %s
                """
                search_value = f"%{search_term}%"
                search_params = [search_value] * 5
            
            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM customer {search_condition}"
            cursor.execute(count_query, search_params)
            total_records = cursor.fetchone()['total']
            
            # Get paginated data
            offset = (page - 1) * per_page
            data_query = f"""
                SELECT idx, nik, name, born, active, salary 
                FROM customer {search_condition}
                ORDER BY idx 
                LIMIT %s OFFSET %s
            """
            
            params = search_params + [per_page, offset]
            cursor.execute(data_query, params)
            customers = cursor.fetchall()
            
            return customers, total_records
            
        except Error as e:
            print(f"Error fetching customers: {e}")
            return [], 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_customer_by_id(self, idx):
        connection = self.db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM customer WHERE idx = %s"
            cursor.execute(query, (idx,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching customer: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def create_customer(self, nik, name, born, active, salary):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO customer (nik, name, born, active, salary) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nik, name, born, active, salary))
            connection.commit()
            return True
        except Error as e:
            print(f"Error creating customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def update_customer(self, idx, nik, name, born, active, salary):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
                UPDATE customer 
                SET nik = %s, name = %s, born = %s, active = %s, salary = %s 
                WHERE idx = %s
            """
            cursor.execute(query, (nik, name, born, active, salary, idx))
            connection.commit()
            return True
        except Error as e:
            print(f"Error updating customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def delete_customer(self, idx):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM customer WHERE idx = %s"
            cursor.execute(query, (idx,))
            connection.commit()
            return True
        except Error as e:
            print(f"Error deleting customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def import_from_csv(self, file_path):
        success_count = 0
        error_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=';')
                next(csv_reader)  # Skip header row
                
                for row in csv_reader:
                    if len(row) >= 5:
                        try:
                            nik = row[0]
                            name = row[1]
                            born = datetime.strptime(row[2], '%Y-%m-%d').date() if row[3] else None
                            active = int(row[3]) if row[3] else 0
                            salary = int(row[4]) if row[4] else 0
                            
                            if self.create_customer(nik, name, born, active, salary):
                                success_count += 1
                            else:
                                error_count += 1
                        except Exception as e:
                            print(f"Error processing row {row}: {e}")
                            error_count += 1
                    else:
                        error_count += 1
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return 0, 1
        
        return success_count, error_count
    
    def export_to_csv(self, file_path):
        customers, _ = self.get_all_customers(page=1, per_page=999999)  # Get all records
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file, delimiter=';')
                
                # Write header
                csv_writer.writerow(['idx', 'nik', 'name', 'born', 'active', 'salary'])
                
                # Write data
                for customer in customers:
                    born_str = customer['born'].strftime('%Y-%m-%d') if customer['born'] else ''
                    csv_writer.writerow([
                        customer['idx'],
                        customer['nik'],
                        customer['name'],
                        born_str,
                        customer['active'],
                        customer['salary']
                    ])
            
            return len(customers), 0
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return 0, 1