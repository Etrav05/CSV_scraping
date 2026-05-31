# Expense Tracker
A simple desktop application to analyze your expenses from CSV files.

<img width="897" height="627" alt="image" src="https://github.com/user-attachments/assets/ce835fc0-0120-4f48-be22-abe529f87a9a" />

## Features
- Process banking CSV files
    - View Top 10 Largest Purchases
    - Total Debits & Credits
    - Total Purchase Categories
    - Total Purchases By Vendor
    - Year-over-Year Total Spending
    - Average Spending by Vendor
- Yearly spending summaries
    - Broken down into monthly Credit and Debit totals
    - Uses Matplotlib to visualize this data
- Summary dashboard with at-a-glance stats
    - Total spent, received, and transaction count
    - Outlier-trimmed average debit and credit transaction value
    - Average debit and credit transactions per month
    - Biggest single purchase, most visited vendor, highest average spend vendor
- Import history — tracks every CSV file you've submitted with record count and timestamp
- Clear database button with confirmation prompt
- SQLite database storage

**NOTE: Test data was produced by AI**
<img width="897" height="627" alt="image" src="https://github.com/user-attachments/assets/c163dd17-2cdb-448b-9c25-f23a5dd2ed6d" />

<img width="900" height="630" alt="image" src="https://github.com/user-attachments/assets/fd713936-7253-4d5e-bda2-7d107a88b81a" />

<img width="900" height="630" alt="image" src="https://github.com/user-attachments/assets/add240de-a62d-433f-956c-ef8e25498a48" />

<img width="1251" height="596" alt="image" src="https://github.com/user-attachments/assets/240a50a9-17e0-4137-80fb-c71c627b98e3" />

## Installation
1. Clone this repository
2. Install Python 3.8 or higher
3. Install dependencies:
```
pip install matplotlib numpy
```

## Usage
1. Run the application:
```
python main.py
```
2. Import your CSV file or skip to view existing data
3. Browse different expense reports from the main menu
4. View the Summary page for a quick overview of your spending

## Project Structure
- `main.py` - Main application interface
- `database.py` - Database operations
- `FileScrape.py` - CSV file processing
- `expenses.db` - SQLite database (created automatically)

## CSV Format
Your CSV should have the following format (Based on CIBC's formatting):
```
2025-01-20,Description of transaction,DebitAmount,CreditAmount,
```

## Requirements
- Python 3.8+
- tkinter (usually comes with Python)
- sqlite3 (built-in)
- matplotlib
- numpy

## Author
Evan Travis

## License
MIT
