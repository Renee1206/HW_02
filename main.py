import matplotlib.pyplot as plt
from input import add_expense
from output import read_expenses, plot_pie_chart_on_ax

if __name__ == "__main__":
    with open("expenses.csv", "w", encoding="utf-8") as f:
        f.write("date,amount,category,note\n")

    print("Start entering your expenses. Type 'q' as the date to quit.\n")

    plt.ion()
    fig, ax = plt.subplots()
    plot_pie_chart_on_ax({}, ax)
    plt.show(block=False)

    while True:
        saved = add_expense()
        if not saved:
            print("\nExit input. Final pie chart has been shown (if any).")
            break

        category_totals = read_expenses("expenses.csv")
        plot_pie_chart_on_ax(category_totals, ax)
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    plt.show()