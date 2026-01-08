import os
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
path = 'C:\\Users\\User\\Downloads\\CSV_Financial_Reader.txt'

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


db = ExpensesDB()  # Set up the database

def main():
    if os.path.exists(path):
        print('-- Exists --')

    if os.path.isfile(path):
        print('== This is a file ==')

    with open("C:\\Users\\User\\Downloads\\CSV_Financial_Reader.txt", "r") as file:
        for line in file:
            line = line.strip().rstrip(',')  # Remove trailing spaces and commas
            date = line.split(',')[0]  # Get the first part (date)
            year_month = '-'.join(date.split('-')[:2])  # Extract year-month

            cost = float(line.split(',')[-1])  # Extract the value (cost)

            price_cat = price_categorization(cost)
            debit_test = debit_finder(line)

            print(f"{year_month} - ${cost:.2f} - {price_cat} - {debit_test}")
            db.add_expense(year_month, cost, price_cat, debit_test, vendor="")

    for category, costs in monthlyCosts.items():  # Rounding monthly costs
        if category != "month":  # Skip the "month" key
            monthlyCosts[category] = [round(cost, 2) for cost in costs]

    print("\nMonthly Costs:")
    for category, costs in monthlyCosts.items():
        if category != "month":  # Skip the "month" key
            print(f"{category}: {costs}")

if __name__ == "__main__":
    main()
