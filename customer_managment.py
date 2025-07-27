from pymongo import MongoClient
#version 12
class CustomerManagement:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['billing_system']
        
    def add_customer(self, customer_id, name, email, phone):
        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "phone": phone
        }
        self.db.customers.insert_one(customer)
        print(f"Customer {name} added successfully.")

    def view_customers(self):
        customers = self.db.customers.find()
        for customer in customers:
            print(customer)

# Example usage:
if __name__ == "__main__":
    cm = CustomerManagement()
    cm.add_customer("C001", "Alice", "alice@example.com", "1234567890")
    cm.view_customers()
