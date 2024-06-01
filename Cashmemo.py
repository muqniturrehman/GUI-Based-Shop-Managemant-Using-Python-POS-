import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import sqlite3 as sq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import calculator
# Connect to database (will create the database if it doesn't exist)
con = sq.connect("billing_system.db")
cur = con.cursor()

# Create tables if they don't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS BIlls (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        date TEXT NOT NULL,
        total REAL NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS BillItems (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER NOT NULL,
        particular TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (bill_id) REFERENCES Bills (bill_id)
    )
''')

con.commit()

class BillItem:
    def __init__(self, particular, quantity, unit_price):
        self.particular = particular
        self.quantity = quantity
        self.unit_price = unit_price

    def __str__(self):
        return f"{self.particular} - Quantity: {self.quantity}, Unit Price: {self.unit_price}"

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.root.configure(bg="lightblue")

        self.particular = tk.StringVar()
        self.unit_price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.customer_name = tk.StringVar()
        self.items = []

        self.setup_ui()

    def setup_ui(self):
        label_frame = tk.Frame(self.root, bg="lightblue")
        label_frame.pack()
        tk.Label(label_frame, text="Mart Land", font=("Arial", 24, "bold"), bg="grey").pack()
        label_frame.configure(bg="grey")

        tabs_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=30)
        tabs_frame.pack()

        products_button = tk.Button(tabs_frame, text="Products", bg="grey", fg="white", cursor="hand2", padx=50,
                                    command=self.manage_products)
        products_button.grid(row=0, column=1, padx=20)

        bills_button = tk.Button(tabs_frame, text="Bills", bg="grey", fg="white", cursor="hand2", padx=50,
                                 command=self.view_bills)
        bills_button.grid(row=0, column=2, padx=20)

        cashmemo_button = tk.Button(tabs_frame, text="Cash Memo", bg="black", fg="white", cursor="hand2", padx=50)
        cashmemo_button.grid(row=0, column=3, padx=20)

        calculator_button = tk.Button(tabs_frame, text="Calculator", bg="grey", fg="white", cursor="hand2", padx=50,
                                      command=self.calculatorr)
        calculator_button.grid(row=0, column=4, padx=20)

        theme_button = tk.Button(tabs_frame, text="Theme", bg="grey", fg="white", cursor="hand2", padx=50,
                                 command=self.change_theme)
        theme_button.grid(row=0, column=0, padx=20, sticky="e")

        quit_button = tk.Button(tabs_frame, text="Quit", bg="grey", fg="white", cursor="hand2", padx=50,
                                command=self.Quit)
        quit_button.grid(row=0, column=5, padx=20, sticky="e")

        bill_frame = ttk.LabelFrame(self.root, text="Bill Details", padding=(10, 5))
        bill_frame.pack(padx=20, pady=20, fill="both")

        cur.execute("SELECT MAX(bill_id) AS bill_no FROM Bills")
        bill_no = cur.fetchone()
        con.commit

        Bill_label = ttk.Label(bill_frame, text = f"Bill No: {bill_no}", font=("Arial", 10))
        Bill_label.grid(row=0, column=0, sticky="w")

        date_label = ttk.Label(bill_frame, text="Date:")
        date_label.grid(row=1, column=0, sticky="w", pady=10)

        date = ttk.Label(bill_frame, text=datetime.now().strftime("%Y-%m-%d"), font=("Arial", 10))
        date.grid(row=1, column=1, sticky="w", pady=10)

        time_label = ttk.Label(bill_frame, text="Time:")
        time_label.grid(row=1, column=2, sticky="w", padx=(50, 5), pady=10)
        time = ttk.Label(bill_frame, text=datetime.now().strftime("%H:%M:%S"), font=("Arial", 10))
        time.grid(row=1, column=3, sticky="w", pady=10)

        name_label = ttk.Label(bill_frame, text="Customer Name:", font=("Arial", 10))
        name_label.grid(row=2, column=0, padx=(0, 5), pady=10, sticky="w")
        name_field = ttk.Entry(bill_frame, font=("Arial", 10), textvariable=self.customer_name)
        name_field.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        ph_label = ttk.Label(bill_frame, text="Customer Phone:", font=("Arial", 10))
        ph_label.grid(row=2, column=2, padx=(50, 5), pady=10, sticky="w")
        ph_field = ttk.Entry(bill_frame, font=("Arial", 10))
        ph_field.grid(row=2, column=3, padx=(0, 5), pady=10, sticky="ew")

        frame = ttk.LabelFrame(self.root, text="Customer Details", padding=(10, 5))
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(frame, text="Customer Name", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.customer_name, font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5,
                                                                                   sticky="ew")
        self.customer_name.set("Anonymous")

        ttk.Label(frame, text="Particular", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        particular_entry = ttk.Entry(frame, textvariable=self.particular, font=("Arial", 12))
        particular_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        particular_entry.bind("<Return>", self.populate_product_details_by_name)

        ttk.Label(frame, text="Code", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.code_entry = ttk.Entry(frame, font=("Arial", 12))

        self.code_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.code_entry.bind("<Return>", self.populate_product_details_by_code)

        ttk.Label(frame, text="Unit Price", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        unit_price_entry = ttk.Entry(frame, textvariable=self.unit_price, font=("Arial", 12))
        unit_price_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame, text="Quantity", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.quantity, font=("Arial", 12)).grid(row=4, column=1, padx=5, pady=5,
                                                                              sticky="ew")

        ttk.Button(frame, text="Add Item", command=self.add_item).grid(row=5, column=0, columnspan=2, padx=5, pady=5,
                                                                       sticky="ew")
        ttk.Button(frame, text="Delete Item", command=self.delete_item).grid(row=6, column=0, columnspan=2, padx=5,
                                                                             pady=5, sticky="ew")
        ttk.Button(frame, text="Edit Item", command=self.edit_item).grid(row=7, column=0, columnspan=2, padx=5, pady=5,
                                                                         sticky="ew")
        ttk.Button(frame, text="Generate Bill", command=self.generate_bill).grid(row=9, column=0, columnspan=2, padx=5,
                                                                                 pady=5, sticky="ew")

        ttk.Button(frame, text="Clear Entries", command=self.clear_entries).grid(row=8, column=0, columnspan=2, padx=5,
                                                                                 pady=5, sticky="ew")

        self.products_tree = ttk.Treeview(frame, columns=("Particular", "Quantity", "Unit Price"), show="headings")
        self.products_tree.grid(row=0, column=2, columnspan=3, rowspan=10, padx=10, pady=5, sticky="nsew")

        self.products_tree.heading("Particular", text="Particular")
        self.products_tree.heading("Quantity", text="Quantity")
        self.products_tree.heading("Unit Price", text="Unit Price")

        self.products_tree.column("Particular", width=150)
        self.products_tree.column("Quantity", width=80)
        self.products_tree.column("Unit Price", width=100)

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        ttk.Button(frame, text="Print Bill", command=self.generate_pdf_bill).grid(row=10, column=4, columnspan=2, padx=5, pady=5,
                                                                      sticky="ew")



    def generate_pdf_bill(self):
        customer_name = self.customer_name.get()
        total = sum(item.unit_price * item.quantity for item in self.items)

        filename = f"{customer_name}_bill.pdf"
        c = canvas.Canvas(filename, pagesize=letter)

        # Add bill details
        c.drawString(100, 750, "Customer Name: " + customer_name)
        c.drawString(100, 730, "Items")
        c.drawString(300, 730, "Qty")
        c.drawString(400, 730, "Unit Price")
        c.drawString(500, 730, "Total")

        # Add items to the bill
        y = 710
        for item in self.items:
            c.drawString(100, y, item.particular)
            c.drawString(300, y, str(item.quantity))
            c.drawString(400, y, str(item.unit_price))
            c.drawString(500, y, str(item.quantity * item.unit_price))
            y -= 20

        # Add total
        c.drawString(400, y - 20, "Total:")
        c.drawString(500, y - 20, str(total))

        c.save()
        messagebox.showinfo("PDF Generated", f"PDF bill '{filename}' generated successfully.")

    def generate_bill(self):
        name = self.customer_name.get()

        if not name:
            messagebox.showwarning("Invalid Input", "Please enter valid customer details.")
            return

        total = sum(item.unit_price * item.quantity for item in self.items)

        bill_str = (
            f"\n{'_' * 52}\n"
            f"{' ' * 22}MART LAND\n"
            f"{' ' * 18}Your Trusted Store\n"
            f"\n* Deals in all kinds of daily necessities *\n"
            f"{'_' * 52}\n"
            f"Customer Name: {name}\n"
            f"{'_' * 52}\n"
            f"{' ' * 2}Items{' ' * 24}Qty{' ' * 8}Unit Price{' ' * 8}Total\n"
            f"{'-' * 52}\n"
        )

        for item in self.items:
            total_price = item.quantity * item.unit_price
            bill_str += f"{item.particular:<30}{item.quantity:<10}{item.unit_price:<15}{total_price:<10}\n"

        bill_str += f"{'-' * 52}\n"
        bill_str += f"{' ' * 38}Total: {total}\n"
        bill_str += f"{'_' * 52}\n"
        bill_str += f"{' ' * 20}Thank you for shopping with us!\n"
        bill_str += f"{' ' * 23}Visit Again!\n"
        bill_str += f"{'_' * 52}"

        cur.execute("INSERT INTO Bills (customer_name, date, total) VALUES (?, ?, ?)",
                    (name, datetime.now().strftime("%Y-%m-%d"), total))
        bill_id = cur.lastrowid
        for item in self.items:
            cur.execute("INSERT INTO BillItems (bill_id, particular, quantity, unit_price) VALUES (?, ?, ?, ?)",
                        (bill_id, item.particular, item.quantity, item.unit_price))
        con.commit()

        messagebox.showinfo("Bill Generated", bill_str)

    def populate_product_details_by_name(self, event):
        particular = self.particular.get()
        if particular:
            cur.execute("SELECT id, unit_price FROM Products WHERE name = ?", (particular,))
            result = cur.fetchone()
            if result:
                product_id, unit_price = result
                self.code_entry.delete(0, tk.END)
                self.code_entry.insert(0, product_id)
                self.unit_price.set(unit_price)
            else:
                messagebox.showwarning("Product Not Found", f"The product '{particular}' is not available in the database.")

    def populate_product_details_by_code(self, event):
        product_code = self.code_entry.get()
        if product_code:
            cur.execute("SELECT name, unit_price FROM Products WHERE id = ?", (product_code,))
            result = cur.fetchone()
            if result:
                name, unit_price = result

                self.particular.set(name)
                self.unit_price.set(unit_price)
            else:
                messagebox.showwarning("Product Not Found", f"The product with code '{product_code}' is not available in the database.")

    def add_item(self):
        particular = self.particular.get()
        unit_price = self.unit_price.get()
        quantity = self.quantity.get()

        if particular and unit_price > 0 and quantity > 0:
            cur.execute("SELECT quantity FROM Products WHERE name = ?", (particular,))
            result = cur.fetchone()
            if result:
                stock_quantity = result[0]
                if quantity <= stock_quantity:
                    cur.execute("UPDATE Products SET quantity = quantity - ? WHERE name = ?", (quantity, particular))
                    con.commit()
                    item = BillItem(particular, quantity, unit_price)
                    self.items.append(item)

                    self.products_tree.insert("", "end", values=(item.particular, item.quantity, item.unit_price))
                    self.clear_entries()
                else:
                    messagebox.showwarning("Out of Stock",
                                           f"Requested quantity for '{particular}' is not available. Only {stock_quantity} in stock.")
            else:
                messagebox.showwarning("Out of Stock", f"The product '{particular}' is not available in stock.")
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid item details.")

    def delete_item(self):
        selected_item = self.products_tree.selection()
        if selected_item:
            item_index = self.products_tree.index(selected_item)
            item = self.items.pop(item_index)
            self.products_tree.delete(selected_item)
            cur.execute("UPDATE Products SET quantity = quantity + ? WHERE name = ?", (item.quantity, item.particular))
            con.commit()
            #messagebox.showinfo("Item Deleted", f"Item '{item.particular}' deleted successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select an item to delete.")

    def edit_item(self):
        selected_item = self.products_tree.selection()
        if selected_item:
            item_index = self.products_tree.index(selected_item)
            item = self.items[item_index]
            self.particular.set(item.particular)
            self.unit_price.set(item.unit_price)
            self.quantity.set(item.quantity)
            self.delete_item()
        else:
            messagebox.showwarning("Selection Error", "Please select an item to edit.")

    def clear_entries(self):
        self.particular.set("")
        self.unit_price.set(0)
        self.quantity.set(0)
        self.customer_name.set("Anonymous")
        self.code_entry.delete(0, tk.END)

    def calculatorr(self):
        calculator.calculator()

    def change_theme(self):
        current_bg = self.root.cget("bg")
        new_bg = "lightblue" if current_bg == "grey" else "grey"
        self.root.configure(bg=new_bg)

    def Quit(self):
        sys.exit()

    def manage_products(self):
        import products
        self.root.destroy()  # Close the current window
        products.manage_products()

    def view_bills(self):
        import bills
        self.root.destroy()  # Close the current window
        bills.Show_bills()

def Cashmemo():
    root = tk.Tk()
    app = BillingApp(root)
    root.attributes("-fullscreen", True)  # Open in full screen
    root.mainloop()
#Cashmemo()
