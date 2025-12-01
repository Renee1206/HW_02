# visualize_expense.py

import csv
from collections import defaultdict

import matplotlib.pyplot as plt


def read_expenses(csv_file="expenses.csv"):
    """
    讀取 expenses.csv，回傳 {category: total_amount} 的 dict
    CSV 欄位順序：date,amount,category,note
    """
    category_totals = defaultdict(float)

    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # 保護性檢查：跳過欄位數不對的列
                if len(row) < 4:
                    continue

                date, amount_str, category, note = row

                # 金額轉 float，轉換失敗就跳過
                try:
                    amount = float(amount_str)
                except ValueError:
                    print(f"警告：無法解析金額「{amount_str}」，此筆紀錄已略過。")
                    continue

                category_totals[category] += amount

    except FileNotFoundError:
        print(f"找不到檔案：{csv_file}，請先用 input_expense.py 建立一些支出紀錄。")
        return {}

    return category_totals


def plot_pie_chart(category_totals):
    """
    根據 {category: total_amount} 畫圓餅圖
    """
    if not category_totals:
        print("沒有資料可以繪圖。")
        return

    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    # 繪製圓餅圖
    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",  # 顯示百分比
        startangle=90        # 從正上方開始
    )
    plt.title("Expenses by Category")
    plt.axis("equal")  # 讓圓餅圖看起來是正圓

    # 顯示圖表
    plt.tight_layout()
    plt.show()
    # 若想存成圖片，可取消下面註解：
    # plt.savefig("expenses_pie_chart.png")


def main():
    category_totals = read_expenses("expenses.csv")
    plot_pie_chart(category_totals)


if __name__ == "__main__":
    main()
