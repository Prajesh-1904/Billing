#version 2.0
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pymongo import MongoClient
class ProductManagement:
    def __init__(self, db):
        self.collection = db['items']

    def add_or_update_product(self, product_name, price, quantity, tax_percentage):
        existing_product = self.collection.find_one({"product_name": product_name})

        if existing_product:
            new_quantity = existing_product['quantity'] - quantity
            if new_quantity < 0:
                raise ValueError(f"Not enough stock for {product_name}")
            self.collection.update_one({"product_name": product_name}, {"$set": {"quantity": new_quantity}})
        else:
            product_data = {
                "product_name": product_name,
                "price": price,
                "quantity": quantity,
                "tax_percentage": tax_percentage
            }
            self.collection.insert_one(product_data)


class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['billing']
        self.collection = self.db['sessions']
        self.pm = ProductManagement(self.db)

        frame = tk.Frame(root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky='w')
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=0, column=1)

        tk.Label(frame, text="Phone Number:").grid(row=1, column=0, sticky='w')
        self.entry_phone = tk.Entry(frame)
        self.entry_phone.grid(row=1, column=1)

        tk.Label(frame, text="Date & Time:").grid(row=2, column=0, sticky='w')
        self.entry_datetime = tk.Entry(frame)
        self.entry_datetime.grid(row=2, column=1)
        self.entry_datetime.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.entry_datetime.config(state='readonly')  # Make it read-only

        tk.Label(frame, text="Product:").grid(row=3, column=0, sticky='w')
        self.entry_product = tk.Entry(frame)
        self.entry_product.grid(row=3, column=1)

        tk.Label(frame, text="Total Price (After Tax):").grid(row=4, column=0, sticky='w')
        self.entry_total_price = tk.Entry(frame)
        self.entry_total_price.grid(row=4, column=1)

        tk.Label(frame, text="Tax Percentage:").grid(row=5, column=0, sticky='w')
        self.entry_tax = tk.Entry(frame)
        self.entry_tax.grid(row=5, column=1)

        tk.Label(frame, text="Quantity:").grid(row=6, column=0, sticky='w')
        self.entry_quantity = tk.Entry(frame)
        self.entry_quantity.grid(row=6, column=1)

        self.button_add_product = tk.Button(frame, text="Add Product", command=self.add_product)
        self.button_add_product.grid(row=7, column=0, columnspan=2, pady=5)

        self.bill_text = tk.Text(frame, width=100, height=20, font=('Arial', 16))
        self.bill_text.grid(row=8, column=0, columnspan=2, pady=10)

        self.button_generate_bill = tk.Button(frame, text="Generate Bill", command=self.generate_bill)
        self.button_generate_bill.grid(row=9, column=0, columnspan=2, pady=5)

        self.total_price_label = tk.Label(frame, text="Total Price: ₹0.00", font=('Arial', 16))
        self.total_price_label.grid(row=10, column=0, columnspan=2)

        self.products = [] 

    def add_product(self):
        product = self.entry_product.get()
        total_price = self.entry_total_price.get()  
        tax_percentage = self.entry_tax.get()
        quantity = self.entry_quantity.get()

        try:
            total_price = float(total_price)
            tax_percentage = float(tax_percentage) / 100
            quantity = int(quantity)

            before_tax_price = total_price / (1 + tax_percentage)

            self.pm.add_or_update_product(product, before_tax_price, quantity, tax_percentage * 100)

            total_before_tax = before_tax_price * quantity
            total_after_tax = total_price * quantity

            self.products.append((product, before_tax_price, total_price, quantity, total_before_tax, total_after_tax))
            self.bill_text.insert(tk.END, f"{product:<20} ₹{before_tax_price:<10.2f} ₹{total_price:<10.2f} {quantity:<10} ₹{total_before_tax:<10.2f} ₹{total_after_tax:<10.2f}\n")

            self.entry_product.delete(0, tk.END)
            self.entry_total_price.delete(0, tk.END)
            self.entry_tax.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)

            self.update_total()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for price, tax, and quantity.")

    def update_total(self):
        total_price = sum(item[5] for item in self.products)  # Total after tax for all products
        self.total_price_label.config(text=f"Total Price: ₹{total_price:.2f}")

    def generate_bill(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        datetime_now = self.entry_datetime.get()

        # Save session to MongoDB
        session_data = {
            'name': name,
            'phone': phone,
            'datetime': datetime_now,
            'products': self.products,
            'total_price': sum(item[5] for item in self.products)  # Total after tax
        }
        self.collection.insert_one(session_data)

        bill_content = f"{'Name:':<20} {name}\n"
        bill_content += f"{'Phone Number:':<20} {phone}\n"
        bill_content += f"{'Date & Time:':<20} {datetime_now}\n\n"
        bill_content += "Products Purchased:\n"
        bill_content += f"{'Product':<20} {'Before Tax':<10} {'After Tax':<10} {'Quantity':<10} {'Total Before Tax':<10} {'Total After Tax':<10}\n"
        bill_content += "-" * 80 + "\n"
        for product, before_tax, after_tax, quantity, total_before_tax, total_after_tax in self.products:
            bill_content += f"{product:<20} ₹{before_tax:<10.2f} ₹{after_tax:<10.2f} {quantity:<10} ₹{total_before_tax:<10.2f} ₹{total_after_tax:<10.2f}\n"
        bill_content += "-" * 80 + "\n"
        bill_content += f"{'Total Amount:':<60} ₹{sum(item[5] for item in self.products):.2f}\n"

        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, bill_content)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
