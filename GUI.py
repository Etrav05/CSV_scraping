import tkinter as tk
from tkinter import ttk
from database import ExpensesDB

class ExpenseApp:
    def __init__(self, root):
        self.db = ExpensesDB()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")

        # Container for all frames
        self.container = tk.Frame(root)
        self.container.pack(fill='both', expand=True)

        # Show file import page first
        self.show_import_page()

    def clear_frame(self):
        """Clear all widgets from container"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_import_page(self):
        """Display the file import page"""
        self.clear_frame()

        # Title
        title = tk.Label(
            self.container,
            text="📁 Import Expense Data",
            font=('Arial', 28, 'bold'),
            pady=30
        )
        title.pack()

        # Instructions
        instructions = tk.Label(
            self.container,
            text="Paste the file path to your CSV file below and click 'Process File'",
            font=('Arial', 12),
            fg='gray'
        )
        instructions.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.container)
        input_frame.pack(pady=30)

        # File path label
        path_label = tk.Label(
            input_frame,
            text="File Path:",
            font=('Arial', 12)
        )
        path_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # File path entry
        self.file_path_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=50
        )
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse button (optional - uses file dialog)
        browse_btn = tk.Button(
            input_frame,
            text="Browse...",
            command=self.browse_file,
            font=('Arial', 10),
            bg='#9E9E9E',
            fg='white',
            cursor='hand2'
        )
        browse_btn.grid(row=0, column=2, padx=10, pady=10)

        # Button frame
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=20)

        # Process button
        process_btn = tk.Button(
            button_frame,
            text="📊 Process File",
            command=self.process_file,
            font=('Arial', 14),
            bg='#4CAF50',
            fg='white',
            cursor='hand2',
            width=20,
            height=2
        )
        process_btn.pack(side='left', padx=10)

        # Skip to menu button
        skip_btn = tk.Button(
            button_frame,
            text="Skip to Menu →",
            command=self.show_main_menu,
            font=('Arial', 14),
            bg='#2196F3',
            fg='white',
            cursor='hand2',
            width=20,
            height=2
        )
        skip_btn.pack(side='left', padx=10)

        # Status label
        self.status_label = tk.Label(
            self.container,
            text="",
            font=('Arial', 11),
            fg='green'
        )
        self.status_label.pack(pady=20)

    def browse_file(self):
        """Open file dialog to browse for CSV file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)

    def process_file(self):
        """Process the CSV file at the given path"""
        file_path = self.file_path_entry.get().strip()

        if not file_path:
            self.status_label.config(text="⚠️ Please enter a file path", fg='red')
            return

        try:
            # Import your processing function from FileScraper.py
            # Assuming you have a function like: process_csv(file_path, db)
            from FileScrape import process_csv

            self.status_label.config(text="⏳ Processing file...", fg='orange')
            self.root.update()

            # Process the file (you'll need to implement this in FileScraper.py)
            records_added = process_csv(file_path, self.db)

            self.status_label.config(
                text=f"✅ Success! Added {records_added} records to database",
                fg='green'
            )

            # Enable the "Go to Menu" button after success
            self.root.after(1500, self.show_main_menu)

        except FileNotFoundError:
            self.status_label.config(text="❌ File not found. Check the path and try again.", fg='red')
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg='red')

    def show_main_menu(self):
        """Display the main menu"""
        self.clear_frame()

        # Title
        title = tk.Label(
            self.container,
            text="💰 EXPENSE TRACKER 💰",
            font=('Arial', 32, 'bold'),
            pady=30
        )
        title.pack()

        # Subtitle
        subtitle = tk.Label(
            self.container,
            text="Select a query to view your expenses",
            font=('Arial', 14),
            fg='gray'
        )
        subtitle.pack(pady=10)

        # Menu buttons frame
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        # Query buttons
        queries = [
            ("📊 Top 10 Largest Purchases", self.show_top_10),
            ("📅 Monthly Summary", self.show_monthly_summary),
            ("🏪 Spending by Vendor", self.show_by_vendor),
            ("💳 Spending by Transaction Type", self.show_by_transaction_type),
            ("📈 All Expenses", self.show_all_expenses)
        ]

        for text, command in queries:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Arial', 14),
                width=35,
                height=2,
                bg='#4CAF50',
                fg='white',
                cursor='hand2'
            )
            btn.pack(pady=8)

    def create_result_page(self, title, columns, data):
        """Generic function to create a results page"""
        self.clear_frame()

        # Header frame
        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        # Title
        title_label = tk.Label(
            header,
            text=title,
            font=('Arial', 24, 'bold')
        )
        title_label.pack(side='left')

        # Back button
        back_btn = tk.Button(
            header,
            text="← Back to Menu",
            command=self.show_main_menu,
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            cursor='hand2'
        )
        back_btn.pack(side='right')

        # Results frame with scrollbar
        results_frame = tk.Frame(self.container)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side='right', fill='y')

        # Treeview table
        tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            height=20
        )

        # Configure scrollbar
        scrollbar.config(command=tree.yview)

        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=150)

        tree.pack(fill='both', expand=True)

        # Insert data
        for row in data:
            tree.insert('', 'end', values=row)

        # Count label
        count_label = tk.Label(
            self.container,
            text=f"Total Results: {len(data)}",
            font=('Arial', 12),
            fg='gray'
        )
        count_label.pack(pady=10)

    def show_top_10(self):
        """Show top 10 largest purchases"""
        expenses = self.db.largest_10_purchases()
        data = []
        for expense in expenses:
            id, year_month, cost, price_cat, trans_type, vendor = expense
            data.append((year_month, f"${cost:.2f}", trans_type, vendor))

        self.create_result_page(
            "Top 10 Largest Purchases",
            ('Date', 'Cost', 'Transaction Type', 'Vendor'),
            data
        )

    def show_monthly_summary(self):
        """Show spending grouped by month"""
        # You'll need to add this method to your Database.py
        try:
            expenses = self.db.get_monthly_summary()
            data = []
            for expense in expenses:
                month, count, total = expense
                data.append((month, count, f"${total:.2f}"))

            self.create_result_page(
                "Monthly Summary",
                ('Month', 'Transaction Count', 'Total Spent'),
                data
            )
        except AttributeError:
            self.show_placeholder("Monthly Summary")

    def show_by_vendor(self):
        """Show spending grouped by vendor"""
        try:
            expenses = self.db.get_by_vendor()
            data = []
            for expense in expenses:
                vendor, count, total = expense
                data.append((vendor, count, f"${total:.2f}"))

            self.create_result_page(
                "Spending by Vendor",
                ('Vendor', 'Transaction Count', 'Total Spent'),
                data
            )
        except AttributeError:
            self.show_placeholder("Spending by Vendor")

    def show_by_transaction_type(self):
        """Show spending grouped by transaction type"""
        try:
            expenses = self.db.get_by_transaction_type()
            data = []
            for expense in expenses:
                trans_type, count, total = expense
                data.append((trans_type, count, f"${total:.2f}"))

            self.create_result_page(
                "Spending by Transaction Type",
                ('Transaction Type', 'Count', 'Total Spent'),
                data
            )
        except AttributeError:
            self.show_placeholder("Spending by Transaction Type")

    def show_all_expenses(self):
        """Show all expenses"""
        try:
            expenses = self.db.get_all_expenses()
            data = []
            for expense in expenses:
                id, year_month, cost, price_cat, trans_type, vendor = expense
                data.append((year_month, f"${cost:.2f}", price_cat, trans_type, vendor))

            self.create_result_page(
                "All Expenses",
                ('Date', 'Cost', 'Category', 'Type', 'Vendor'),
                data
            )
        except AttributeError:
            self.show_placeholder("All Expenses")

    def show_placeholder(self, query_name):
        """Show placeholder for queries not yet implemented"""
        self.clear_frame()

        msg = tk.Label(
            self.container,
            text=f"'{query_name}' query not yet implemented in Database.py",
            font=('Arial', 16)
        )
        msg.pack(pady=100)

        back_btn = tk.Button(
            self.container,
            text="← Back to Menu",
            command=self.show_main_menu,
            font=('Arial', 12)
        )
        back_btn.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()