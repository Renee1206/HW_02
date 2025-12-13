# input_expense.py

def add_expense():
    print("Add your expenses:")

    while True:
        print("\n--- New Expense ---")
        
        date = input("Date (YYYY-MM-DD): ")

        # 金額：只有這裡做錯誤檢查，其他欄位不檢查
        while True:
            amount = input("Amount: ")
            try:
                amount = float(amount)
                break
            except ValueError:
                print("Amount must be a number. Please try again.")

        category = input("Category: ")
        note = input("Note (optional): ")

        # 寫入 CSV
        with open("expenses.csv", "a", encoding="utf-8") as f:
            f.write(f"{date},{amount},{category},{note}\n")

        print("Expense saved!")

        # 問是否要再輸入一筆
        again = input("\nDo you want to add another expense? (y/n): ").lower()
        if again != "y":
            break

    print("\nAll expenses saved to expenses.csv!")


if __name__ == "__main__":
    add_expense()