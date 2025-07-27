from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class InvoiceManagement:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['billing_system']

    def generate_invoice(self, customer_id, product_id, quantity):
        customer = self.db.customers.find_one({"customer_id": customer_id})
        product = self.db.products.find_one({"product_id": product_id})

        if not customer or not product:
            print("Customer or product not found.")
            return

        invoice_id = f"INV-{customer_id}-{product_id}"
        total_amount = product['price'] * quantity

        # Create PDF invoice
        c = canvas.Canvas(f"{invoice_id}.pdf", pagesize=letter)
        c.drawString(100, 750, f"Invoice ID: {invoice_id}")
        c.drawString(100, 730, f"Customer: {customer['name']}")
        c.drawString(100, 710, f"Product: {product['name']}")
        c.drawString(100, 690, f"Quantity: {quantity}")
        c.drawString(100, 670, f"Total Amount: ${total_amount}")
        c.save()
        
        print(f"Invoice {invoice_id} generated successfully.")

# Example usage:
if __name__ == "__main__":
    im = InvoiceManagement()
    im.generate_invoice("C001", "P001", 2)
