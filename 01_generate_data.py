

import random
import csv
from datetime import datetime, timedelta

random.seed(42)  

CATEGORY_MERCHANTS = {
    "Food": [
        ("SWIGGY*ORDER{n}", (150, 600)),
        ("ZOMATO ONLINE", (120, 550)),
        ("DOMINOS PIZZA", (300, 800)),
        ("STARBUCKS COFFEE", (150, 400)),
        ("LOCAL RESTAURANT {n}", (200, 900)),
        ("PAYTM*FOODCOURT", (100, 400)),          
        ("UPI-9876543210-FOOD", (100, 500)),      
        ("BIGBASKET GROCERY", (500, 2000)),       
    ],
    "Travel": [
        ("UBER TRIP {n}", (80, 400)),
        ("OLA CABS", (100, 450)),
        ("IRCTC TICKET", (400, 1500)),
        ("INDIGO AIRLINES", (2500, 6000)),
        ("PETROL PUMP {n}", (500, 2000)),
        ("UPI-8765432109-CAB", (100, 400)),
        ("RAPIDO BIKE", (40, 150)),
    ],
    "Shopping": [
        ("AMAZON PAY", (300, 3000)),
        ("FLIPKART INTERNET", (500, 4000)),
        ("MYNTRA DESIGNS", (600, 2500)),
        ("RELIANCE RETAIL", (400, 3500)),
        ("PAYTM*MALL{n}", (300, 2500)),            
        ("UPI-7654321098-SHOP", (200, 3000)),
    ],
    "Bills": [
        ("AIRTEL POSTPAID", (300, 700)),
        ("ELECTRICITY BOARD BILL", (800, 2500)),
        ("JIO RECHARGE", (200, 500)),
        ("NETFLIX SUBSCRIPTION", (200, 700)),
        ("APARTMENT MAINTENANCE", (1500, 3000)),
        ("UPI-6543210987-BILL", (200, 1000)),
    ],
    "Entertainment": [
        ("BOOKMYSHOW TICKET", (200, 800)),
        ("PVR CINEMAS", (250, 900)),
        ("SPOTIFY PREMIUM", (120, 200)),
        ("NETFLIX SUBSCRIPTION", (200, 700)),      
    ],
    "Income": [
        ("SALARY CREDIT XYZCORP", (30000, 60000)),
        ("FREELANCE PAYMENT", (2000, 15000)),
        ("REFUND CREDIT", (200, 3000)),
        ("UPI-1234567890-CREDIT", (500, 5000)),
    ],
}


NOISE_DESCRIPTIONS = [
    ("POS PURCHASE {n}", (100, 3000)),
    ("UPI-{n}-TXN", (50, 3000)),
    ("NEFT TRANSFER", (500, 5000)),
    ("CARD PAYMENT {n}", (100, 2000)),
]


def add_typo_noise(description, chance=0.15):
    
    if random.random() > chance:
        return description

    if random.random() < 0.5 and len(description) > 3:
        pos = random.randint(0, len(description) - 1)
        description = description[:pos] + description[pos + 1:]
    else:
        description = description + str(random.randint(100, 999))

    return description


def generate_transactions(num_rows=200, noise_fraction=0.12):
    rows = []
    start_date = datetime(2026, 1, 1)

    num_noise = int(num_rows * noise_fraction)
    num_clean = num_rows - num_noise

    for i in range(num_clean):
        category = random.choice(list(CATEGORY_MERCHANTS.keys()))
        template, (low, high) = random.choice(CATEGORY_MERCHANTS[category])

        description = template.format(n=random.randint(1, 999))
        description = add_typo_noise(description)
        amount = round(random.uniform(low, high), 2)

        if category != "Income":
            amount = -amount

        date = start_date + timedelta(days=random.randint(0, 210))

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "description": description,
            "amount": amount,
            "category": category,
        })

    
    for i in range(num_noise):
        category = random.choice(list(CATEGORY_MERCHANTS.keys()))
        template, (low, high) = random.choice(NOISE_DESCRIPTIONS)
        description = template.format(n=random.randint(1000, 9999))
        amount = round(random.uniform(low, high), 2)

        if category != "Income":
            amount = -amount

        date = start_date + timedelta(days=random.randint(0, 210))

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "description": description,
            "amount": amount,
            "category": category,
        })

    rows.sort(key=lambda r: r["date"])
    return rows


def save_csv(rows, filename="transactions.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "description", "amount", "category"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} transactions to {filename}")


if __name__ == "__main__":
    transactions = generate_transactions(300)
    save_csv(transactions)

    print("\nSample rows:")
    for row in transactions[:5]:
        print(row)
