import tkinter as tk
from tkinter import ttk, messagebox
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

        self.container = tk.Frame(root)
        self.container.pack(fill='both', expand=True)

        self.show_import_page()

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ── Import page ────────────────────────────────────────────────────────────

    def show_import_page(self):
        self.clear_frame()

        # Title
        tk.Label(
            self.container,
            text="📁 Import Expense Data",
            font=('Arial', 28, 'bold'),
            pady=30
        ).pack()

        tk.Label(
            self.container,
            text="Paste/Browse for the file path to your CSV file below and click 'Process File'",
            font=('Arial', 12),
            fg='gray'
        ).pack(pady=10)

        # ── File input row ──────────────────────────────────────────────────────
        input_frame = tk.Frame(self.container)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="File Path:", font=('Arial', 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky='e'
        )

        self.file_path_entry = tk.Entry(input_frame, font=('Arial', 12), width=50)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(
            input_frame, text="Browse...", command=self.browse_file,
            font=('Arial', 9), bg='#9E9E9E', fg='white', cursor='hand2'
        ).grid(row=0, column=2, padx=15, pady=10)

        # ── Action buttons ──────────────────────────────────────────────────────
        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame, text="🔍 Process File", command=self.process_file,
            font=('Arial', 14), bg='#4CAF50', fg='white', cursor='hand2',
            width=20, height=2
        ).pack(side='left', padx=10)

        tk.Button(
            button_frame, text="Skip to Menu →", command=self.show_main_menu,
            font=('Arial', 14), bg='#2196F3', fg='white', cursor='hand2',
            width=20, height=2
        ).pack(side='left', padx=10)

        tk.Button(
            button_frame, text="🗑 Clear Database", command=self.confirm_clear_database,
            font=('Arial', 14), bg='#f44336', fg='white', cursor='hand2',
            width=20, height=2
        ).pack(side='left', padx=10)

        # Status label
        self.status_label = tk.Label(self.container, text="", font=('Arial', 11), fg='green')
        self.status_label.pack(pady=8)

        # ── Submitted files list ────────────────────────────────────────────────
        self._build_submitted_files_panel()

    def _build_submitted_files_panel(self):
        """Show every CSV that has been imported, pulled from the DB."""
        imported = self.db.get_imported_files()   # [(file_path, records_added, imported_at), ...]

        panel = tk.LabelFrame(
            self.container,
            text="  📂 Submitted Files  ",
            font=('Arial', 11, 'bold'),
            fg='#333',
            padx=10, pady=8
        )
        panel.pack(fill='x', padx=30, pady=(0, 15))

        if not imported:
            tk.Label(
                panel,
                text="No files submitted yet.",
                font=('Arial', 11),
                fg='gray'
            ).pack(anchor='w')
            return

        # Scrollable list for when there are many imports
        canvas = tk.Canvas(panel, height=min(len(imported) * 26, 130), highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient='vertical', command=canvas.yview)
        inner = tk.Frame(canvas)

        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        for file_path, records_added, imported_at in imported:
            # Trim the timestamp to just the date + time (drop microseconds if present)
            when = imported_at[:16]  # "YYYY-MM-DD HH:MM"
            short_path = file_path if len(file_path) <= 55 else '…' + file_path[-54:]

            row = tk.Frame(inner)
            row.pack(fill='x', pady=1)

            tk.Label(
                row,
                text=f"✔  {short_path}",
                font=('Arial', 10),
                fg='#2e7d32',
                anchor='w'
            ).pack(side='left')

            tk.Label(
                row,
                text=f"  {records_added} records  |  {when}",
                font=('Arial', 10),
                fg='gray',
                anchor='e'
            ).pack(side='right')

    # ── Clear database ─────────────────────────────────────────────────────────

    def confirm_clear_database(self):
        """Show a confirmation dialog before wiping the DB."""
        confirmed = messagebox.askyesno(
            title="Clear Database",
            message="This will permanently delete ALL expense records and the import history.\n\nAre you sure?",
            icon='warning'
        )
        if confirmed:
            self.db.delete_database()
            # Rebuild the import page so the submitted-files panel refreshes
            self.show_import_page()
            self.status_label.config(text="🗑 Database cleared successfully.", fg='gray')

    # ── File handling ──────────────────────────────────────────────────────────

    def browse_file(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)

    def process_file(self):
        file_path = self.file_path_entry.get().strip()

        if not file_path:
            self.status_label.config(text="⚠️ Please enter a file path", fg='red')
            return

        try:
            from FileScrape import process_csv

            self.status_label.config(text="⏳ Processing file...", fg='orange')
            self.root.update()

            records_added = process_csv(file_path, self.db)

            # Rebuild the page so the submitted-files panel reflects the new import
            self.show_import_page()
            self.status_label.config(
                text=f"✅ Success! Added {records_added} records to database",
                fg='green'
            )

            self.root.after(1500, self.show_main_menu)

        except FileNotFoundError:
            self.status_label.config(text="❌ File not found. Check the path and try again.", fg='red')
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg='red')

    # ── Main menu ──────────────────────────────────────────────────────────────

    def show_main_menu(self):
        self.clear_frame()

        tk.Label(
            self.container,
            text="💰 EXPENSE ANALYZER 3000 💰",
            font=('Arial', 32, 'bold'),
            pady=20
        ).pack()

        tk.Label(self.container, text="By: Evan Travis", font=('Arial', 10), fg='gray').pack(pady=0)

        tk.Label(
            self.container,
            text="Select a query to view your expenses",
            font=('Arial', 14),
            fg='gray'
        ).pack(pady=10)

        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=30)

        queries = [
            ("📝 Queries", self.show_queries_page),
            ("📅 Monthly Summary", self.show_monthly_summary),
            ("💲 All Expenses", self.show_all_expenses),
            ("📋 Summary", self.show_summary)
        ]

        for text, command in queries:
            tk.Button(
                button_frame, text=text, command=command,
                font=('Arial', 14), width=35, height=2,
                bg='#4CAF50', fg='white', cursor='hand2'
            ).pack(pady=8)

        tk.Button(
            button_frame, text="← Back to Import",
            command=self.show_import_page,
            font=('Arial', 12), width=35, height=1,
            bg='#9E9E9E', fg='white', cursor='hand2'
        ).pack(pady=(16, 0))

    # ── Generic results page ───────────────────────────────────────────────────

    def create_result_page(self, title, columns, data, back_command=None):
        self.clear_frame()

        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(header, text=title, font=('Arial', 24, 'bold')).pack(side='left')

        if back_command is None:
            back_command = self.show_queries_page

        tk.Button(
            header,
            text="← Back to Menu" if back_command == self.show_main_menu else "← Back to Queries",
            command=back_command,
            font=('Arial', 12), bg='#2196F3', fg='white', cursor='hand2'
        ).pack(side='right')

        results_frame = tk.Frame(self.container)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side='right', fill='y')

        tree = ttk.Treeview(
            results_frame, columns=columns, show='headings',
            yscrollcommand=scrollbar.set, height=20
        )
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=150)

        tree.pack(fill='both', expand=True)

        for row in data:
            tree.insert('', 'end', values=row)

        tk.Label(
            self.container,
            text=f"Total Results: {len(data)}",
            font=('Arial', 12), fg='gray'
        ).pack(pady=10)

    # ── Query pages ────────────────────────────────────────────────────────────

    def show_top_10(self):
        expenses = self.db.largest_10_purchases()
        data = [(e[1], f"${e[2]:.2f}", e[4], e[5]) for e in expenses]
        self.create_result_page(
            "Top 10 Largest Purchases",
            ('Date', 'Cost', 'Transaction Type', 'Vendor'),
            data, back_command=self.show_queries_page
        )

    def show_total_debit_credit(self):
        expenses = self.db.total_debits_credits()
        data = [(e[0], f"${e[1]:.2f}") for e in expenses]
        self.create_result_page(
            "Total Debits and Credits",
            ('Transaction type', 'Cost'),
            data, back_command=self.show_queries_page
        )

    def show_total_purchase_categories(self):
        expenses = self.db.total_purchase_categories()
        data = [(e[0], f"${e[1]:.2f}", e[2]) for e in expenses]
        self.create_result_page(
            "Total Purchase Categories",
            ('Price Category', 'Cost', 'Transaction Count'),
            data, back_command=self.show_queries_page
        )

    def show_total_purchases_by_vendor(self):
        expenses = self.db.total_purchase_vendor()
        data = [(e[0], f"${e[1]:.2f}", e[2]) for e in expenses]
        self.create_result_page(
            "Total Purchase By Vendor",
            ('Vendor', 'Cost', 'Transaction Count'),
            data, back_command=self.show_queries_page
        )

    def show_year_over_year_totals(self):
        expenses = self.db.total_year_over_year()
        data = [(e[0], f"${e[1]:.2f}", e[2]) for e in expenses]
        self.create_result_page(
            "Year over Year Total Spending",
            ('Year', 'Cost', 'Transaction Count'),
            data, back_command=self.show_queries_page
        )

    def show_average_spending_by_vendor(self):
        expenses = self.db.average_spending_by_vendor()
        data = [(e[0], f"${e[1]:.2f}", e[2], f"${e[3]:.2f}") for e in expenses]
        self.create_result_page(
            "Average Spending by Vendor",
            ('Vendor', 'Average', 'Transaction Count', 'Total Spent'),
            data, back_command=self.show_queries_page
        )

    # ── Monthly summary ────────────────────────────────────────────────────────

    def show_monthly_summary(self):
        self.clear_frame()

        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(header, text="📅 Monthly Summary - Select Year", font=('Arial', 24, 'bold')).pack(side='left')

        tk.Button(
            header, text="← Back to Menu", command=self.show_main_menu,
            font=('Arial', 12), bg='#2196F3', fg='white', cursor='hand2'
        ).pack(side='right')

        try:
            years = self.db.get_available_years()

            if not years:
                tk.Label(
                    self.container,
                    text="No expense data available. Please import a CSV file first.",
                    font=('Arial', 14), fg='gray'
                ).pack(pady=100)
                return

            tk.Label(
                self.container,
                text="Select a year to view monthly spending:",
                font=('Arial', 14), fg='gray'
            ).pack(pady=40)

            dropdown_frame = tk.Frame(self.container)
            dropdown_frame.pack(pady=20)

            tk.Label(dropdown_frame, text="Year:", font=('Arial', 14)).pack(side='left', padx=10)

            self.selected_year = tk.StringVar(value=str(years[0]))

            ttk.Combobox(
                dropdown_frame, textvariable=self.selected_year,
                values=[str(y) for y in years],
                state='readonly', font=('Arial', 14), width=15
            ).pack(side='left', padx=10)

            tk.Button(
                self.container, text="📊 View Chart",
                command=lambda: self.show_monthly_chart(int(self.selected_year.get())),
                font=('Arial', 14), width=20, height=2,
                bg='#4CAF50', fg='white', cursor='hand2'
            ).pack(pady=30)

        except AttributeError:
            tk.Label(
                self.container,
                text="Database method 'get_available_years()' not yet implemented.",
                font=('Arial', 14), fg='red', justify='center'
            ).pack(pady=100)

    def show_monthly_chart(self, year):
        expenses = self.db.monthly_debit_credit_given_year(year)

        debit_totals  = {f"{i:02d}": 0 for i in range(1, 13)}
        credit_totals = {f"{i:02d}": 0 for i in range(1, 13)}

        for month, trans_type, cost in expenses:
            if 'Debit' in trans_type:
                debit_totals[month] = cost
            if 'Credit' in trans_type:
                credit_totals[month] = cost

        x_array = np.array(['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'])
        y_debit  = [debit_totals[f"{i:02d}"]  for i in range(1, 13)]
        y_credit = [credit_totals[f"{i:02d}"] for i in range(1, 13)]

        plt.plot(x_array, y_debit,  'o--r', label='Debit')
        plt.plot(x_array, y_credit, 'o--g', label='Credit')
        plt.title(f"Total Debit/Credit Spending Per Month - {year}")
        plt.xlabel("Month")
        plt.ylabel("Total ($)")
        plt.legend()
        plt.grid(axis='x')
        plt.show()

    # ── All expenses ───────────────────────────────────────────────────────────

    def show_all_expenses(self):
        try:
            expenses = self.db.all_expenses()
            data = [(e[1], f"${e[2]:.2f}", e[3], e[4], e[5]) for e in expenses]
            self.create_result_page(
                "All Expenses",
                ('Date', 'Cost', 'Category', 'Type', 'Vendor'),
                data, back_command=self.show_main_menu
            )
        except AttributeError:
            self.show_placeholder("All Expenses")

    def show_placeholder(self, query_name):
        self.clear_frame()
        tk.Label(
            self.container,
            text=f"'{query_name}' query not yet implemented in Database.py",
            font=('Arial', 16)
        ).pack(pady=100)
        tk.Button(
            self.container, text="← Back to Menu", command=self.show_main_menu,
            font=('Arial', 12), bg='#2196F3', fg='white'
        ).pack()

    # ── Queries page ───────────────────────────────────────────────────────────

    def show_queries_page(self):
        self.clear_frame()

        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(header, text="📝 Queries", font=('Arial', 28, 'bold')).pack(side='left')

        tk.Button(
            header, text="← Back to Menu", command=self.show_main_menu,
            font=('Arial', 12), bg='#2196F3', fg='white', cursor='hand2'
        ).pack(side='right')

        button_frame = tk.Frame(self.container)
        button_frame.pack(pady=20)

        queries = [
            ("🏅 Top 10 Largest Purchases",       self.show_top_10),
            ("📊 Total Debits & Credits",          self.show_total_debit_credit),
            ("📦 Total Purchase Categories",       self.show_total_purchase_categories),
            ("🛍 Total Purchases By Vendor",       self.show_total_purchases_by_vendor),
            ("📅 Year-over-Year Total Spending",   self.show_year_over_year_totals),
            ("📑 Average Spending by Vendor",      self.show_average_spending_by_vendor),
        ]

        columns = 2
        for i, (text, command) in enumerate(queries):
            tk.Button(
                button_frame, text=text, command=command,
                font=('Arial', 14), width=35, height=2,
                bg='#4CAF50', fg='white', cursor='hand2'
            ).grid(row=i // columns, column=i % columns, padx=10, pady=8)


    def show_summary(self):
        self.clear_frame()

        # ── Header ──────────────────────────────────────────────────────────────
        header = tk.Frame(self.container)
        header.pack(fill='x', padx=20, pady=(20, 10))

        tk.Label(header, text="📋 Summary", font=('Arial', 24, 'bold')).pack(side='left')

        tk.Button(
            header, text="← Back to Menu", command=self.show_main_menu,
            font=('Arial', 12), bg='#2196F3', fg='white', cursor='hand2'
        ).pack(side='right')

        # ── Scrollable body ──────────────────────────────────────────────────────
        body_frame = tk.Frame(self.container)
        body_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        canvas = tk.Canvas(body_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_frame, orient='vertical', command=canvas.yview)
        self._summary_grid = tk.Frame(canvas)

        self._summary_grid.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        canvas.create_window((0, 0), window=self._summary_grid, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Mouse-wheel scrolling
        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>',
            lambda ev: canvas.yview_scroll(-1 * (ev.delta // 120), 'units')))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

        # ── Sections ─────────────────────────────────────────────────────────────
        self._summary_add_avg_debit_credit()

    # ── Summary helpers ────────────────────────────────────────────────────────

    def _summary_section(self, title):
        """Add a full-width section header to the summary grid."""
        tk.Label(
            self._summary_grid,
            text=title,
            font=('Arial', 13, 'bold'),
            fg='#555',
            anchor='w'
        ).grid(row=self._summary_next_row(), column=0, columnspan=4,
               sticky='w', padx=10, pady=(20, 4))

        ttk.Separator(self._summary_grid, orient='horizontal').grid(
            row=self._summary_next_row(), column=0, columnspan=4,
            sticky='ew', padx=10, pady=(0, 10)
        )

    def _summary_card(self, label, value, col, row, bg='#E3F2FD', fg='#0D47A1'):
        """Render a single stat card at the given grid position."""
        card = tk.Frame(
            self._summary_grid,
            bg=bg,
            relief='flat',
            bd=0,
            highlightbackground='#BBDEFB',
            highlightthickness=1
        )
        card.grid(row=row, column=col, padx=10, pady=6, sticky='nsew')
        self._summary_grid.columnconfigure(col, weight=1)

        tk.Label(card, text=value, font=('Arial', 20, 'bold'),
                 bg=bg, fg=fg).pack(pady=(14, 2))
        tk.Label(card, text=label, font=('Arial', 10),
                 bg=bg, fg='#555').pack(pady=(0, 14))

    def _summary_next_row(self):
        """Return the next unused grid row index."""
        if not hasattr(self, '_sum_row'):
            self._sum_row = 0
        else:
            self._sum_row += 1
        return self._sum_row

    def _summary_add_avg_debit_credit(self):
        """Outlier-trimmed average debit vs credit card pair."""
        self._sum_row = 0  # reset row counter each time summary is built

        results = self.db.average_debit_credit_overall()

        # Parse whichever rows came back (order not guaranteed)
        avgs = {'Debit': None, 'Credit': None}
        for trans_type, cleaned_avg in results:
            if trans_type in avgs:
                avgs[trans_type] = cleaned_avg

        self._summary_section("💳  Average Transaction")

        card_row = self._summary_next_row()
        debit_val  = f"${avgs['Debit']:.2f}"  if avgs['Debit']  is not None else "N/A"
        credit_val = f"${avgs['Credit']:.2f}" if avgs['Credit'] is not None else "N/A"

        self._summary_card("Avg Debit",  debit_val,  col=0, row=card_row,
                           bg='#FFEBEE', fg='#B71C1C')
        self._summary_card("Avg Credit", credit_val, col=1, row=card_row,
                           bg='#E8F5E9', fg='#1B5E20')


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
