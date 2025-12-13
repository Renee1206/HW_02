# input.py

import os
import csv


def save_expense(date: str, amount: str, category: str, note: str, csv_file: str = "expenses.csv"):
    if not date:
        raise ValueError("Date is required.")
    if not category:
        raise ValueError("Category is required.")
    if not amount:
        raise ValueError("Amount is required.")

    try:
        amount_value = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

    if amount_value < 0:
        raise ValueError("Amount cannot be negative.")

    file_exists = os.path.exists(csv_file)
    needs_header = (not file_exists) or os.path.getsize(csv_file) == 0

    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(["date", "amount", "category", "note"])
        writer.writerow([date, amount_value, category, note])
main
