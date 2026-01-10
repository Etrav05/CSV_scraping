import os
import re
from database import ExpensesDB

monthlyCosts = {
    "month": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06",
               "2024-07", "2024-08", "2024-09", "2024-010", "2024-11", "2024-12",],
    "Credit": [0.0] * 12,  # Initialize with 12 months of 0.0
    "Debit": [0.0] * 12,
}
'''
categories = {
    "food": ["subway", "popeyes", "sunset", "dairy queen", "tim hortons", "wendy's", "famous wok",
             "cafe", "boston", "roxbury", "chicken", "swiss", "bulk barn", "mcdonald's", "coke", "bitter end",
             "starbucks", "domino's", "harveys", "valens", "wayback", "hasty", "panera", "settlers", "twice",
             "montana's", "keg", "collins", "ada*vending", "willie's", "a1", "big bear", "parkside", "ichiki",
             "rockton berry", "foodland", "jax sweet", "mr gao", "arby's", "sports bar", "kfc", "beaner munky",
             "chungchun rice", "brant county", "dominos", "yogurtys froyo", "dyments farm", "sobeys",
             "willie dog", "mcmaster hospit", "m m bar", "thirsty cactus", "marcy's berries", "metro", "zehrs",
             "sh vending", "cafe domestiiqu", "lagershed", "jesses tap gr", "bitter end", "cabin coffee",
             "rockton lions"],

    "living": ["shoppers drug", "staples", "urban", "archies", "sport chek", "boathouse " ],

    "transport": ["metrolinx"],

    "tuition": ["conestoga", "mcmaster university"],

    "entertainment": ["galaxy cinemas", "indigo", "flying", "ibowl" "rockton", "crunchyroll", "k1 speed"],

    "gas": ["petro canada"],

    "other": ["dollarama", "fuald'd motel", "dollar planet", "swiss plus", "amazon", "electronic funds transfer debit",
              "e-transfer", "amazon.ca", "lcbo/rao", "lcbo", "walmart", "electronic funds transfer preauthorized debit",
              "amzn mktp", "canadian tire", "sail outdoors", "mcmaster campus", "body shop"],

    "income": ["internet deposit", "electronic funds transfer credit"],
}
'''

def price_categorization(cost):
    if cost < 10.00:
        return "Small"
    elif cost < 100.00:
        return "Medium"
    elif cost < 1000.00:
        return "Large"
    elif cost < 10000.00:
        return "Extreme"
    else:   # > 10000.0
        return "Massive"

def debit_finder(line):
    debit_term = "INTERNET DEPOSIT"

    if debit_term in line:
        return "Debit"

    else:
        return "Credit"

def vendor_finder(description):
    # Special Cases
    if "PREAUTHORIZED DEBIT" in description:
        description = description.split("PREAUTHORIZED DEBIT", 1)[1].strip()  # Removes preauthorized debit as it is all
                                                                              # Caps making it hard to tell from vendors
    if "ATM WITHDRAWAL" in description:
        return "ATM WITHDRAWAL"

    if "Branch Transaction" in description:
        return "BANK"

    parts = description.split()  # Split up words by spaces
    description_parts = []
    skipped = False  # A long banking number can appear before and/or after the vendor name, so I track
                                 # if it is gone yet

    for part in reversed(parts):  # Start from the end of line (Vendor names were typically at the end)
        if re.match(r'^[A-Z0-9]{8,}$', part) and re.search(r'[A-Z]', part) and re.search(r'\d', part):
            if not skipped:
                skipped = True
                continue
            else:
                break

        if re.match(r'^\d{8,}$', part):  # Skip the first 8+ digit number we encounter using 're'
            if not skipped:
                skipped = True
                continue
            else:
                break  # Stop at second long number

        # Also stop at common banking keywords
        if part.upper() in ['PURCHASE', 'RETAIL', 'INTERAC', 'SALE', 'POINT', 'OF', 'TRANSFER', 'FUNDS', 'ELECTRONIC',
                            'BANKING', 'INTERNET']:
            break

        description_parts.insert(0, part)  # Collecting the parts

    vendor = ' '.join(description_parts)

    # Keep words that start with uppercase (allows "Garrison Brewin")
    vendor = ' '.join([word for word in vendor.split() if word and word[0].isupper()])

    vendor = re.sub(r'\s*[#C]\d*$', '', vendor)  # Find common patterns with trailing symbols and numbers
    vendor = vendor.strip()

    return vendor if vendor else "UNKNOWN"

db = ExpensesDB()  # Set up the database
# path = 'C:\\Users\\User\\Downloads\\CSV_Financial_Reader.txt'

def process_csv(path, database):
    records_added = 0  # Track how many records added

    with open(path, "r") as file:
        for line in file:
            line = line.strip().rstrip(',')  # Remove trailing spaces and commas
            parts = line.split(',')  # split the line up into parts

            date = parts[0]  # Get the first part (date)
            year_month = '-'.join(date.split('-')[:2])  # Extract year-month

            description = parts[1] if len(parts) > 1 else ""  # Get the description of the transaction for later

            # BIG CHANGE, credits and debits seem to have their own columns, therefore we can parse & classify them here
            debit_amount = parts[2] if len(parts) > 2 and parts[2] else None
            credit_amount = parts[3] if len(parts) > 3 and parts[3] else None

            if debit_amount:
                cost = float(debit_amount)
                transaction_type = "Debit"
            elif credit_amount:
                cost = float(credit_amount)
                transaction_type = "Credit"
            else:
                continue  # Skip if no amount

            price_cat = price_categorization(cost)
            vendor = vendor_finder(description)

            print(f"{year_month} - ${cost:.2f} - {price_cat} - {transaction_type} - {vendor}")
            db.add_expense(year_month, cost, price_cat, transaction_type, vendor)
            records_added += 1

        return records_added
