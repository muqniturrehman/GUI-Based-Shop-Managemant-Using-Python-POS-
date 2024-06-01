import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sq
from calculator import calculator
import sys


class ProductManager:
    def __init__(self, root):
        self.root = root
        self.con = sq.connect("billing_system.db")
        self.cur = self.con.cursor()
        self.create_products_table()
        self.setup_ui()

    def create_products_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL
            )
        ''')
        self.con.commit()

    def setup_ui(self):
        self.products_window = tk.Toplevel(self.root)
        self.products_window.title("Manage Products")
        self.products_window.geometry("1520x900")
        self.products_window.configure(bg="lightblue")
        self.products_window.attributes("-fullscreen", True)

        self.label_frame = tk.Frame(self.products_window, bg="grey")
        self.label_frame.pack()

        tk.Label(self.label_frame, text="Mart Land", font=("Arial", 24, "bold"), bg="grey").pack()

        self.tabs_frame = tk.Frame(self.products_window, bg="lightblue", padx=10, pady=30)
        self.tabs_frame.pack()

        products_button = tk.Button(self.tabs_frame, text="Products", bg="black", fg="white", cursor="hand2", padx=50)
        products_button.grid(row=0, column=1, padx=20)

        # Replace with actual methods from the BillingApp class
        bills_button = tk.Button(self.tabs_frame, text="Bills", bg="grey", fg="white", cursor="hand2", padx=50,
                                 command=self.view_bills)
        bills_button.grid(row=0, column=2, padx=20)

        cashmemo_button = tk.Button(self.tabs_frame, text="Cash Memo", bg="grey", fg="white", cursor="hand2", padx=50, command = self.cashmemo_caller )
        cashmemo_button.grid(row=0, column=3, padx=20)

        calculator_button = tk.Button(self.tabs_frame, text="Calculator", bg="grey", fg="white", cursor="hand2", padx=50,
                                      command=self.calculator)
        calculator_button.grid(row=0, column=4, padx=20)

        # Replace with actual methods from the BillingApp class
        theme_button = tk.Button(self.tabs_frame, text="Theme", bg="grey", fg="white", cursor="hand2", padx=50,
                                 command=self.change_theme)
        theme_button.grid(row=0, column=0, padx=20, sticky="e")

        quit_button = tk.Button(self.tabs_frame, text="Quit", bg="grey", fg="white", cursor="hand2", padx=50,
                                command=self.Quit)
        quit_button.grid(row=0, column=5, padx=20, sticky="e")

        product_frame = ttk.LabelFrame(self.products_window, text="Product Details", padding=(10, 5))
        product_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.unit_price_var = tk.DoubleVar()
        self.search_var = tk.StringVar()

        ttk.Label(product_frame, text="Search:").grid(row=4, column=0, padx=5, pady=5)
        search_entry = ttk.Entry(product_frame, textvariable=self.search_var)
        search_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(product_frame, text="Product Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(product_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(product_frame, text="Quantity").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(product_frame, textvariable=self.quantity_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(product_frame, text="Unit Price").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(product_frame, textvariable=self.unit_price_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(product_frame, text="Add Product", command=self.add_product).grid(row=3, column=0, padx=2, pady=2)
        ttk.Button(product_frame, text="Edit Product", command=self.Edit_product).grid(row=3, column=1, padx=2, pady=5)
        ttk.Button(product_frame, text="Delete Product", command=self.delete_product).grid(row=3, column=2, padx=2, pady=2)
        ttk.Button(product_frame, text="Search", command=self.search_products).grid(row=4, column=2, padx=2, pady=2)

        # Create Treeview to display products
        self.products_tree = ttk.Treeview(product_frame, columns=("Name", "Quantity", "Unit Price"))
        self.products_tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.products_tree.heading("#0", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Quantity", text="Quantity")
        self.products_tree.heading("Unit Price", text="Unit Price")

        # Configure Treeview scrollbar
        scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=self.products_tree.yview)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.load_products()

    def clear_entries(self):
        self.name_var.set("")
        self.quantity_var.set(0)
        self.unit_price_var.set(0)

    def load_products(self):
        # Clear existing data in Treeview
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Retrieve products from the database
        self.cur.execute("SELECT * FROM Products")
        products = self.cur.fetchall()

        # Populate Treeview with products
        for product in products:
            self.products_tree.insert("", "end", text=product[0], values=(product[1], product[2], product[3]))

    def add_product(self):
        name = self.name_var.get()
        quantity = self.quantity_var.get()
        unit_price = self.unit_price_var.get()
        if name and quantity > 0 and unit_price > 0:
            self.cur.execute("INSERT INTO Products (name, quantity, unit_price) VALUES (?, ?, ?)",
                             (name, quantity, unit_price))
            self.con.commit()
            self.load_products()
            self.clear_entries()

        else:
            messagebox.showwarning("Invalid Input", "Please enter valid product details.")

    def Edit_product(self):
        selected_item = self.products_tree.selection()
        if selected_item:
            product_name = self.products_tree.item(selected_item[0], "values")[0]
            self.cur.execute("SELECT * FROM Products WHERE name = ?", (product_name,))
            product = self.cur.fetchone()
            if product:
                self.name_var.set(product[1])
                self.quantity_var.set(product[2])
                self.unit_price_var.set(product[3])
                self.cur.execute("DELETE FROM Products WHERE name = ?", (product_name,))
                self.con.commit()
                self.load_products()
            else:
                messagebox.showwarning("Invalid Input", "Please enter valid product details.")
        else:
            messagebox.showwarning("Selection Error", "Please select a product to update.")

    def delete_product(self):
        selected_item = self.products_tree.selection()
        if selected_item:
            product_name = self.products_tree.item(selected_item[0], "values")[0]
            self.cur.execute("DELETE FROM Products WHERE Name = ?", (product_name,))
            self.con.commit()
            self.load_products()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

    def get_products(self, search_query=""):
        if search_query:
            self.cur.execute("SELECT * FROM Products WHERE name LIKE ?", ("%" + search_query + "%",))
        else:
            self.cur.execute("SELECT * FROM Products")
        return self.cur.fetchall()

    def search_products(self):
        search_query = self.search_var.get()
        self.products_tree.delete(*self.products_tree.get_children())
        for product in self.get_products(search_query):
            self.products_tree.insert("", "end", values=(product[1], product[2], product[3]))

    def calculator(self):
        calculator()

    def Quit(self):
        sys.exit()

    # Placeholder methods to avoid errors, replace with actual implementations
    def view_bills(self):
        import bills
        self.root.destroy()  # Close the current window
        bills.Show_bills()

    def change_theme(self):
        if self.products_window.cget("bg") == "lightblue":
            self.products_window.configure(bg="grey")
        else:
            self.products_window.configure(bg="lightblue")

    def cashmemo_caller(self):
        import Cashmemo
        self.root.destroy()  # Close the current window
        Cashmemo.Cashmemo()


def manage_products():
    root = tk.Tk()
    root.withdraw()
    app = ProductManager(root)
    root.mainloop()


manage_products()
