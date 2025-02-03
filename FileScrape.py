import os

# def yearmonth(Year, month, foodValues):

foodValues = {}  # list of values spent on food

categories = {
    "food_list": ["subway", "popeyes", "sunset", "dairy queen", "tim hortons", "wendy's", "famous wok", "lcbo/rao",
                  "cafe", "boston", "roxbury", "chicken", "swiss", "bulk", "mcdonald's", "coke", "sh", "bitter end",
                  "starbucks", "domino's", "harveys", "valens", "wayback", "hasty", "panera", "settlers", "twice",
                  "montana's", "keg", "collins", "ada*vending", "willie's", "a1", "big bear", "parkside", "ichiki",
                  "rockton berry", "foodland", "jax sweet", "mr gao", "arby's", "sports bar", "kfc", "beaner munky",
                  "chungchun rice", "brant county", "dominos", "yogurtys froyo", "dyments farm", "sobeys",
                  "willie dog", "mcmaster hospit", "m m bar", "thirsty cactus", "marcy's berries"],

    "store_list": ["dollarama", "shoppers", "staples", "galaxy", "indigo", "flying", "urban", "rockton", "ibowl",
                   "archies"],

    "petrol_list": []
}

path = 'C:\\Users\\User\\Downloads\\CSV_Financial_Reader.txt'

if os.path.exists(path):
    print('-- Exists --')

if os.path.isfile(path):
    print('== This is a file ==')

with open("C:\\Users\\User\\Downloads\\CSV_Financial_Reader.txt", "r") as file:
    for line in file:
        line = line.strip().rstrip(',')  # Remove trailing spaces and commas
        date = line.split(',')[0]  # Get the first part (date)
        year_month = '-'.join(date.split('-')[:2])  # Extract year-month

        if any(word.lower() in line.lower() for word in categories["food_list"]):  # Isolating all food purchases
            foodMatch = next(word for word in categories["food_list"] if word.lower() in line.lower())
            foodCost = float(line.split(',')[-1])  # Extract the last part (cost)

            if year_month not in foodValues:
                foodValues[year_month] = []
            foodValues[year_month].append(foodCost)

            #  print(f"{date}, {foodMatch}, {foodCost}")

for year_month, cost in foodValues.items():
    print(f"{year_month} - {sum(cost):.2f}")
