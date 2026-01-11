import tkinter as tk
from tkinter import ttk
from database import ExpensesDB
import matplotlib.pyplot as plt
import numpy as np

class ExpenseApp:
    def __init__(self, root):
        self.back_command = None
        self.file_path_entry = None
        self.db = ExpensesDB()
        self.root = root
        self.root.title("Expense Analyzer 3000")
        self.root.geometry("900x600")

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
            text="Paste/Browse for the file path to your CSV file below and click 'Process File'",
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

        # Browse button (Uses file dialog)
        browse_btn = tk.Button(
            input_frame,
            text="Browse...",
            command=self.browse_file,
            font=('Arial', 9),
            bg='#9E9E9E',
            fg='white',
            cursor='hand2'
        )
        browse_btn.grid(row=0, column=2, padx=15, pady=10)

        # Button frame
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=20)

        # Process button
        process_btn = tk.Button(
            button_frame,
            text="🔍 Process File",
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
        """Open file dialog to browse for CSV files"""
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
            text="💰 EXPENSE ANALYZER 3000 💰",
            font=('Arial', 32, 'bold'),
            pady=20
        )
        title.pack()

        # Subtitle 1
        subtitle_name = tk.Label(
            self.container,
            text="By: Evan Travis",
            font=('Arial', 10),
            fg='gray'
        )
        subtitle_name.pack(pady=0)

        # Subtitle 2
        subtitle_instruction = tk.Label(
            self.container,
            text="Select a query to view your expenses",
            font=('Arial', 14),
            fg='gray'
        )
        subtitle_instruction.pack(pady=10)

        # Menu buttons frame
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        # Query buttons
        queries = [
            ("📝 Queries", self.show_queries_page),
            ("📅 Monthly Summary", self.show_monthly_summary),
            ("💲 All Expenses", self.show_all_expenses)
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

    def create_result_page(self, title, columns, data, back_command=None):
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

        if back_command is None:
            back_command = self.show_queries_page

        # Back button
        back_btn = tk.Button(
            header,
            text="← Back to Menu" if back_command == self.show_main_menu else "← Back to Queries",
            command=back_command,
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
            data,
            back_command=self.show_queries_page
        )

    def show_total_debit_credit(self):
        """Show total value of both debits and credits"""
        expenses = self.db.total_debits_credits()
        data = []
        for expense in expenses:
            trans_type, cost = expense
            data.append((trans_type, f"${cost:.2f}"))

        self.create_result_page(
            "Total Debits and Credits",
            ('Transaction type', 'Cost'),
            data,
            back_command=self.show_queries_page
        )

    def show_total_purchase_categories(self):
        """Show total values of each price categories (Small - Massive)"""
        expenses = self.db.total_purchase_categories()
        data = []
        for expense in expenses:
            price_cat, cost, count = expense
            data.append((price_cat, f"${cost:.2f}", count))

        self.create_result_page(
            "Total Purchase Categories",
            ('Price Category', 'Cost', 'Transaction Count'),
            data,
            back_command=self.show_queries_page
        )

    def show_total_purchases_by_vendor(self):
        """Show total value of purchases by vendor name"""
        expenses = self.db.total_purchase_vendor()
        data = []
        for expense in expenses:
            vendor, cost, count = expense
            data.append((vendor, f"${cost:.2f}", count))

        self.create_result_page(
            "Total Purchase By Vendor",
            ('Vendor', 'Cost', 'Transaction Count'),
            data,
            back_command=self.show_queries_page
        )

    def show_year_over_year_totals(self):
        """Show total value of purchases by year"""
        expenses = self.db.total_year_over_year()
        data = []
        for expense in expenses:
            year, cost, count = expense
            data.append((year, f"${cost:.2f}", count))

        self.create_result_page(
            "Year over Year Total Spending",
            ('Year', 'Cost', 'Transaction Count'),
            data,
            back_command=self.show_queries_page
        )

    def show_average_spending_by_vendor(self):
        """Show average value of purchases by vendor"""
        expenses = self.db.average_spending_by_vendor()
        data = []
        for expense in expenses:
            vendor, average, count, total = expense
            data.append((vendor, f"${average:.2f}", count, f"${total:.2f}"))

        self.create_result_page(
            "Average Spending by Vendor",
            ('Vendor', 'Average', 'Transaction Count', 'Total Spent'),
            data,
            back_command=self.show_queries_page
        )

    ####### MONTHLY SUMMARY #######
    def show_monthly_summary(self):
        """Show year selection page for monthly summary"""
        self.clear_frame()

        # Header frame
        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        # Title
        title_label = tk.Label(
            header,
            text="📅 Monthly Summary - Select Year",
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

        # Get available years from database
        try:
            years = self.db.get_available_years()

            if not years:
                # No data available
                msg = tk.Label(
                    self.container,
                    text="No expense data available. Please import a CSV file first.",
                    font=('Arial', 14),
                    fg='gray'
                )
                msg.pack(pady=100)
                return

            # Instructions
            instruction = tk.Label(
                self.container,
                text="Select a year to view monthly spending:",
                font=('Arial', 14),
                fg='gray'
            )
            instruction.pack(pady=40)

            # Dropdown frame
            dropdown_frame = tk.Frame(self.container)
            dropdown_frame.pack(pady=20)

            # Year label
            year_label = tk.Label(
                dropdown_frame,
                text="Year:",
                font=('Arial', 14)
            )
            year_label.pack(side='left', padx=10)

            # Dropdown variable
            self.selected_year = tk.StringVar()
            self.selected_year.set(str(years[0]))  # Set default to first year

            # Dropdown menu
            year_dropdown = ttk.Combobox(
                dropdown_frame,
                textvariable=self.selected_year,
                values=[str(year) for year in years],
                state='readonly',
                font=('Arial', 14),
                width=15
            )
            year_dropdown.pack(side='left', padx=10)

            # View chart button
            view_btn = tk.Button(
                self.container,
                text="📊 View Chart",
                command=lambda: self.show_monthly_chart(int(self.selected_year.get())),
                font=('Arial', 14),
                width=20,
                height=2,
                bg='#4CAF50',
                fg='white',
                cursor='hand2'
            )
            view_btn.pack(pady=30)

        except AttributeError:
            # Database method doesn't exist yet
            msg = tk.Label(
                self.container,
                text="Database method 'get_available_years()' not yet implemented.",
                font=('Arial', 14),
                fg='red',
                justify='center'
            )
            msg.pack(pady=100)

    def show_monthly_chart(self, year):
        """Show spending chart grouped by month"""
        expenses = self.db.monthly_debit_credit_given_year(year)

        debit_totals = {f"{i:02d}": 0 for i in range(1, 13)}  # {'01': 0, '02': 0, ...}
        credit_totals = {f"{i:02d}": 0 for i in range(1, 13)}

        for expense in expenses:
            month, trans_type, cost = expense
            if 'Debit' in trans_type:
                debit_totals[month] = cost
            if 'Credit' in trans_type:
                credit_totals[month] = cost

        x_array = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'])

        y_debit_points = [debit_totals[f"{i:02d}"] for i in range(1, 13)]
        y_credit_points = [credit_totals[f"{i:02d}"] for i in range(1, 13)]

        plt.plot(x_array, y_debit_points, 'o--r', label='Debit')
        plt.plot(x_array, y_credit_points, 'o--g', label='Credit')

        plt.title(f"Total Debit/Credit Spending Per Month - {year}")
        plt.xlabel("Month")
        plt.ylabel("Total ($)")

        plt.legend()
        plt.grid(axis='x')

        plt.show()
    ####### MONTHLY SUMMARY END #######

    def show_all_expenses(self):
        """Show all expenses"""
        try:
            expenses = self.db.all_expenses()
            data = []
            for expense in expenses:
                id, year_month, cost, price_cat, trans_type, vendor = expense
                data.append((year_month, f"${cost:.2f}", price_cat, trans_type, vendor))

            self.create_result_page(
                "All Expenses",
                ('Date', 'Cost', 'Category', 'Type', 'Vendor'),
                data,
                back_command=self.show_main_menu
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
            font=('Arial', 12),
            bg='#2196F3',
            fg='white'
        )
        back_btn.pack()

    def show_queries_page(self):
        """Display the queries page"""
        self.clear_frame()

        # Header frame
        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        # Title
        title_label = tk.Label(
            header,
            text="📝 Queries",
            font=('Arial', 28, 'bold')
        )
        title_label.pack(side='left')

        # Button frame
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=20)

        # Query buttons
        queries = [
            ("🏅 Top 10 Largest Purchases", self.show_top_10),
            ("📊 Total Debits & Credits", self.show_total_debit_credit),
            ("📦 Total Purchase Categories", self.show_total_purchase_categories),
            ("🛍 Total Purchases By Vendor", self.show_total_purchases_by_vendor),
            ("📅 Year-over-Year Total Spending", self.show_year_over_year_totals),
            ("📑 Average Spending by Vendor", self.show_average_spending_by_vendor)
        ]

        columns = 2
        for i, (text, command) in enumerate(queries):
            row = i // columns
            col = i % columns

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
            btn.grid(row=row, column=col, padx=10, pady=8)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()