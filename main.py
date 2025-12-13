import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from input import save_expense
from output import read_expenses, plot_pie_chart_on_ax

CSV_FILE = "expenses.csv"


def on_add():
    date = date_var.get().strip()
    category = category_var.get().strip()
    amount = amount_var.get().strip()
    note = note_var.get().strip()

    try:
        save_expense(date, amount, category, note, CSV_FILE)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return

    update_chart()
    clear_inputs()


def update_chart():
    totals = read_expenses(CSV_FILE)
    plot_pie_chart_on_ax(totals, ax, title="Expenses by Category")
    canvas.draw()


def clear_inputs():
    date_var.set("")
    category_var.set("")
    amount_var.set("")
    note_var.set("")


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("980x560")

container = ttk.Frame(root, padding=10)
container.pack(fill="both", expand=True)

left = ttk.Frame(container)
left.pack(side="left", fill="y", padx=(0, 12))

right = ttk.Frame(container)
right.pack(side="right", fill="both", expand=True)

# Left form
ttk.Label(left, text="Add Expense", font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(0, 10))

ttk.Label(left, text="Date (YYYY-MM-DD)").pack(anchor="w")
date_var = tk.StringVar()
ttk.Entry(left, textvariable=date_var, width=28).pack(anchor="w", pady=(0, 8))

ttk.Label(left, text="Category").pack(anchor="w")
category_var = tk.StringVar()
ttk.Entry(left, textvariable=category_var, width=28).pack(anchor="w", pady=(0, 8))

ttk.Label(left, text="Amount").pack(anchor="w")
amount_var = tk.StringVar()
ttk.Entry(left, textvariable=amount_var, width=28).pack(anchor="w", pady=(0, 8))

ttk.Label(left, text="Note (optional)").pack(anchor="w")
note_var = tk.StringVar()
ttk.Entry(left, textvariable=note_var, width=28).pack(anchor="w", pady=(0, 14))

btn_row = ttk.Frame(left)
btn_row.pack(anchor="w", fill="x")
ttk.Button(btn_row, text="Add", command=on_add).pack(side="left", fill="x", expand=True)
ttk.Button(btn_row, text="Clear", command=clear_inputs).pack(side="left", fill="x", expand=True, padx=(8, 0))

ttk.Label(left, text="Tip: Category can be Chinese (e.g., 衣服 / 遊戲).", foreground="gray").pack(anchor="w", pady=(18, 0))

# Right chart
fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=120)
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

plot_pie_chart_on_ax({}, ax, title="Expenses by Category")
canvas.draw()

root.mainloop()
