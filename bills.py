# Importing necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3 as sq
from datetime import datetime
from calculator import calculator
import sys

class BillViewer:
    def __init__(self):
        # Database initialization
        self.con = sq.connect("billing_system.db")
        self.cur = self.con.cursor()
        self.create_tables()

        # Main window setup
        self.root = tk.Tk()
        self.root.title("View Bills")
        self.root.geometry("1520x900")
        self.root.configure(background="lightblue")
        self.root.attributes("-fullscreen", True)

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", foreground="black", background="blue", font=("Helvetica", 10, "bold"))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("Treeview", font=("Helvetica", 10))

        label_frame = tk.Frame(self.root, bg="lightblue")
        label_frame.pack()

        tk.Label(label_frame, text="Mart Land", font=("Arial", 24, "bold"), bg="Grey").pack()
        label_frame.configure(bg="grey")

        tabs_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=30)
        tabs_frame.pack()

        products_button = tk.Button(tabs_frame, text="Products", bg="grey", fg="white", cursor="hand2", padx=50,
                                    command=self.manage_products)
        products_button.grid(row=0, column=1, padx=20)

        bills_button = tk.Button(tabs_frame, text="Bills", bg="black", fg="white", cursor="hand2", padx=50)
        bills_button.grid(row=0, column=2, padx=20)

        cashmemo_button = tk.Button(tabs_frame, text="Cash Memo", bg="grey", fg="white", cursor="hand2", padx=50, command = self.cashmemo_caller)
        cashmemo_button.grid(row=0, column=3, padx=20)

        calculator_button = tk.Button(tabs_frame, text="Calculator", bg="grey", fg="white", cursor="hand2", padx=50,
                                      command=self.calculator)
        calculator_button.grid(row=0, column=4, padx=20)

        theme_button = tk.Button(tabs_frame, text="Theme", bg="grey", fg="white", cursor="hand2", padx=50,
                                 command=self.change_theme)
        theme_button.grid(row=0, column=0, padx=20, sticky="e")

        quit_button = tk.Button(tabs_frame, text="Quit", bg="grey", fg="white", cursor="hand2", padx=50,
                                command=self.Quit)
        quit_button.grid(row=0, column=5, padx=20, sticky="e")
        # Search frame
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=10)

        # Search buttons
        self.bill_no_button = ttk.Button(self.search_frame, text="Search by Bill No.", command=self.search_by_bill_no)
        self.bill_no_button.grid(row=0, column=0, padx=10, pady=5)

        self.customer_name_button = ttk.Button(self.search_frame, text="Search by Customer Name", command=self.search_by_customer_name)
        self.customer_name_button.grid(row=0, column=1, padx=10, pady=5)

        self.date_range_button = ttk.Button(self.search_frame, text="Search by Date Range", command=self.search_by_date_range)
        self.date_range_button.grid(row=0, column=2, padx=10, pady=5)

        self.today_button = ttk.Button(self.search_frame, text="Search Today", command=self.search_today)
        self.today_button.grid(row=0, column=3, padx=10, pady=5)

        self.list_all_button = ttk.Button(self.search_frame, text="List All", command=self.list_all)
        self.list_all_button.grid(row=0, column=4, padx=10, pady=5)

        # Treeview for displaying bills
        self.bills_tree = ttk.Treeview(self.root, columns=("ID", "Customer", "Date", "Total"), show="headings")
        self.bills_tree.pack(side="left", fill="both", expand=True)

        self.bills_tree.heading("ID", text="Bill ID")
        self.bills_tree.heading("Customer", text="Customer")
        self.bills_tree.heading("Date", text="Date")
        self.bills_tree.heading("Total", text="Total")

        self.bills_tree.column("ID", width=50)
        self.bills_tree.column("Customer", width=150)
        self.bills_tree.column("Date", width=120)
        self.bills_tree.column("Total", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.bills_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.bills_tree.configure(yscrollcommand=scrollbar.set)

        # Load bills initially
        self.load_bills()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date TEXT NOT NULL,
                total REAL NOT NULL
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS BillItems (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id INTEGER NOT NULL,
                particular TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (bill_id) REFERENCES Bills (bill_id)
            )
        ''')

        self.con.commit()

    def load_bills(self):
        self.bills_tree.delete(*self.bills_tree.get_children())
        self.cur.execute("SELECT * FROM Bills")
        bills = self.cur.fetchall()
        for bill in bills:
            self.bills_tree.insert("", "end", values=bill)

    def search_by_bill_no(self):
        bill_no = tk.simpledialog.askinteger("Search by Bill No.", "Enter Bill No.:")
        if bill_no is not None:
            self.cur.execute("SELECT * FROM Bills WHERE bill_id = ?", (bill_no,))
            bill = self.cur.fetchone()
            if bill:
                self.bills_tree.delete(*self.bills_tree.get_children())
                self.bills_tree.insert("", "end", values=bill)
            else:
                messagebox.showinfo("Search Result", f"No bill found with Bill No. {bill_no}")

    def search_by_customer_name(self):
        customer_name = tk.simpledialog.askstring("Search by Customer Name", "Enter Customer Name:")
        if customer_name:
            self.cur.execute("SELECT * FROM Bills WHERE customer_name = ?", (customer_name,))
            bills = self.cur.fetchall()
            if bills:
                self.bills_tree.delete(*self.bills_tree.get_children())
                for bill in bills:
                    self.bills_tree.insert("", "end", values=bill)
            else:
                messagebox.showinfo("Search Result", f"No bills found for customer '{customer_name}'")

    def search_by_date_range(self):
        start_date = tk.simpledialog.askstring("Search by Date Range", "Enter Start Date (YYYY-MM-DD):")
        end_date = tk.simpledialog.askstring("Search by Date Range", "Enter End Date (YYYY-MM-DD):")
        if start_date and end_date:
            self.cur.execute("SELECT * FROM Bills WHERE date BETWEEN ? AND ?", (start_date, end_date))
            bills = self.cur.fetchall()
            if bills:
                self.bills_tree.delete(*self.bills_tree.get_children())
                for bill in bills:
                    self.bills_tree.insert("", "end", values=bill)
            else:
                messagebox.showinfo("Search Result", "No bills found in the specified date range")

    def search_today(self):
    # Get the current date
        now = datetime.now()
        today_date = now.date().strftime("%Y-%m-%d")

    # Execute the SQL query to find bills for today
        self.cur.execute("SELECT * FROM Bills WHERE date = ?", (today_date,))
        bills_today = self.cur.fetchall()

    # Clear the current treeview
        self.bills_tree.delete(*self.bills_tree.get_children())

    # Insert bills into the treeview or show a message if none are found
        if bills_today:
            for bill in bills_today:
                self.bills_tree.insert("", "end", values=bill)
        else:
            messagebox.showinfo("Bill result", "No bill generated today...")
    def list_all(self):
        self.bills_tree.delete(*self.bills_tree.get_children())
        self.cur.execute("SELECT * FROM Bills")
        bills = self.cur.fetchall()
        if bills:
            for bill in bills:
                self.bills_tree.insert("", "end", values=bill)
        else:
            messagebox.showinfo("Bill result","No bill generated today...")


    def manage_products(self):
        import products
        self.root.destroy()  # Close the current window
        products.manage_products()

    def calculator(self):
        calculator()

    def change_theme(self):
        current_bg = self.root.cget("bg")
        new_bg = "lightblue" if current_bg == "Grey" else "Grey"
        self.root.configure(bg=new_bg)

    def Quit(self):
        sys.exit()

    def cashmemo_caller(self):
        import Cashmemo
        self.root.destroy()  # Close the current window
        Cashmemo.Cashmemo()

def Show_bills():
    bill_viewer = BillViewer()
    bill_viewer.root.mainloop()

Show_bills()
