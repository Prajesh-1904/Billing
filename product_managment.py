from pymongo import MongoClient

class ProductManagement:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['billing_system']
        
    def add_product(self, product_id, name, price, stock):
        product = {
            "product_id": product_id,
            "name": name,
            "price": price,
            "stock": stock
        }
        self.db.products.insert_one(product)
        print(f"Product {name} added successfully.")

    def view_products(self):
        products = self.db.products.find()
        for product in products:
            print(product)

# Example usage:
if __name__ == "__main__":
    pm = ProductManagement()
    pm.add_product("P001", "Laptop", 1000, 10)
    pm.view_products()
