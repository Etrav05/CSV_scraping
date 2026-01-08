# Expense Tracker
A simple desktop application to analyze your expenses from CSV files.

<img width="801" height="630" alt="image" src="https://github.com/user-attachments/assets/e4658647-d037-4270-aeda-9641cab7506a" />


## Features
- Import expenses from CSV files
- View top 10 largest purchases
- (Future) Various other queries
- (Future) Monthly spending summaries
- (Future) Breakdown by vendor and transaction type
- SQLite database storage

## Installation
1. Clone this repository
2. Install Python 3.8 or higher
3. No additional dependencies needed (uses built-in libraries)

## Usage
1. Run the application:
```
   python gui.py
```

2. Import your CSV file or skip to view existing data

3. Browse different expense reports from the main menu

## Project Structure
- `gui.py` - Main application interface
- `database.py` - Database operations
- `FileScrape.py` - CSV file processing
- `expenses.db` - SQLite database (created automatically)

## CSV Format
Your CSV should have the following format (Based on CIBC's formatting):
```
2025-01-20,Description of transaction,Amount,
```

## Requirements
- Python 3.8+
- tkinter (usually comes with Python)
- sqlite3 (built-in)

## Author
Evan Travis

## License
MIT
