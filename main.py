from customer_managment import CustomerManagement
from product_managment import ProductManagement
from invoice_managment import InvoiceManagement

def main():
    cm = CustomerManagement()
    pm = ProductManagement()
    im = InvoiceManagement()

    # Example usage
    cm.add_customer("C002", "Bob", "bob@example.com", "0987654321")
    pm.add_product("P002", "Smartphone", 600, 15)
    im.generate_invoice("C002", "P002", 1)

if __name__ == "__main__":
    main()
