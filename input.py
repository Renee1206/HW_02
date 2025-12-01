# input.py

def add_expense():
    """
    Input a single expense record.
    Returns True if a record was saved, or False if the user chose to quit.
    """
    print("\n--- New Expense ---")

    # 允許用 q 結束整個輸入流程
    date = input("Date (YYYY-MM-DD) (or q to quit): ").strip()
    if date.lower() == "q":
        return False

    # 金額：做錯誤檢查
    while True:
        amount = input("Amount: ").strip()
        try:
            amount_value = float(amount)
            break
        except ValueError:
            print("Amount must be a number. Please try again.")

    category = input("Category: ").strip()
    note = input("Note (optional): ").strip()

    # 寫入 CSV
    with open("expenses.csv", "a", encoding="utf-8") as f:
        f.write(f"{date},{amount_value},{category},{note}\n")

    print("Expense saved to expenses.csv!")
    return True


if __name__ == "__main__":
    add_expense()