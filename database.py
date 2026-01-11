import sqlite3
from contextlib import contextmanager

class ExpensesDB:
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect('expenses.db')
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year_month TEXT NOT NULL,
                    cost REAL,
                    price_category TEXT,
                    transaction_type TEXT,
                    vendor TEXT
                )
            ''')
            conn.commit()

    def add_expense(self, year_month, cost, price_cat, transaction_type, vendor=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses(year_month, cost, price_category, transaction_type, vendor)
                VALUES (?, ?, ?, ?, ?)
            ''', (year_month, cost, price_cat, transaction_type, vendor)
            )
            conn.commit()
            return cursor.lastrowid

    def get_available_years(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT year_month
                FROM expenses
            ''')

            years = set()  # Parse for the years here rather than in the GUI
            for row in cursor.fetchall():
                year_month = row[0]
                year = int(year_month[:4])  # Get first 4 characters
                years.add(year)

            return sorted(years, reverse=True)

    def monthly_debit_credit_given_year(self, year):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT 
                        SUBSTR(year_month, -2, 2) as month,
                        transaction_type,
                        SUM(cost) as total
                    FROM expenses
                    WHERE SUBSTR(year_month, 1, 4) = ?
                    GROUP BY month, transaction_type
                    ORDER BY month
                ''', (str(year),))
            return cursor.fetchall()

    def all_expenses(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                     SELECT *
                     FROM expenses
                 ''')
            return cursor.fetchall()

    def largest_10_purchases(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * 
                FROM expenses
                WHERE transaction_type NOT LIKE ?
                ORDER BY cost DESC
                LIMIT 10
            ''', ('%Credit%',))
            return cursor.fetchall()

    def total_debits_credits(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT transaction_type, SUM(cost) 
                FROM expenses
                GROUP BY transaction_type
                ORDER BY SUM(cost) DESC
            ''')
            return cursor.fetchall()

    def total_purchase_categories(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT price_category, SUM(cost), COUNT(*)
                FROM expenses
                WHERE transaction_type NOT LIKE ?
                GROUP BY price_category
                ORDER BY SUM(Cost) DESC
            ''', ('%Credit%',))
            return cursor.fetchall()

    def total_purchase_vendor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                  SELECT vendor, SUM(cost), COUNT(*)
                  FROM expenses
                  WHERE transaction_type NOT LIKE ?
                  GROUP BY vendor
                  ORDER BY COUNT(*) DESC
              ''', ('%Credit%',))
            return cursor.fetchall()

    def total_year_over_year(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    SUBSTR(year_month, 1, 4) AS year, 
                    SUM(cost), 
                    COUNT(*)
                FROM expenses
                WHERE transaction_type NOT LIKE ?
                GROUP BY year
                ORDER BY year DESC
              ''', ('%Credit%',))
            return cursor.fetchall()

    def average_spending_by_vendor(self, min_transactions=5):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT vendor, AVG(cost), COUNT(*), SUM(cost)
                FROM expenses
                WHERE transaction_type NOT LIKE ?
                GROUP BY vendor
                HAVING COUNT(*) >= ?
                ORDER BY AVG(cost) DESC
            ''', ('%Credit%', min_transactions))
            return cursor.fetchall()
