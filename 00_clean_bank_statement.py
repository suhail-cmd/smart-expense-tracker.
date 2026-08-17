"""
BONUS STEP: Convert a real bank statement export into the clean format
our model expects (date, description, amount).

WHY THIS EXISTS:
Real bank statements usually have SEPARATE Debit and Credit columns,
plus a running Balance column we don't need. Our model just wants one
'amount' column where spending is negative and income is positive.

This script also strips the UPI reference numbers out of descriptions
(e.g. 'UPI/SWIGGY/406812345678/Payment' -> 'UPI SWIGGY Payment') since
those long numbers are just noise that can confuse the TF-IDF vectorizer.

Run: python 00_clean_bank_statement.py sample_bank_statement.csv
"""

import sys
import re
import pandas as pd


def clean_description(desc):
    """Remove long reference numbers, keep the meaningful words."""
    # remove sequences of 6+ digits (typical reference/UPI numbers)
    desc = re.sub(r"\d{6,}", "", desc)
    # replace separators with spaces
    desc = re.sub(r"[/\-]", " ", desc)
    # collapse multiple spaces
    desc = re.sub(r"\s+", " ", desc).strip()
    return desc


def convert_statement(input_path, output_path="transactions_cleaned.csv"):
    df = pd.read_csv(input_path)

    # Real exports vary in column names - adjust here if yours differ
    date_col = "Date"
    desc_col = "Description"
    debit_col = "Debit"
    credit_col = "Credit"

    df[debit_col] = pd.to_numeric(df[debit_col], errors="coerce").fillna(0)
    df[credit_col] = pd.to_numeric(df[credit_col], errors="coerce").fillna(0)

    # amount: negative for spending (debit), positive for income (credit)
    df["amount"] = df[credit_col] - df[debit_col]

    df["description"] = df[desc_col].apply(clean_description)
    df["date"] = pd.to_datetime(df[date_col], format="%d-%m-%Y", errors="coerce").dt.strftime("%Y-%m-%d")

    cleaned = df[["date", "description", "amount"]]
    cleaned.to_csv(output_path, index=False)

    print(f"Cleaned {len(cleaned)} transactions -> {output_path}")
    print("\nPreview:")
    print(cleaned.head(10).to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 00_clean_bank_statement.py <your_statement.csv>")
        sys.exit(1)

    convert_statement(sys.argv[1])
