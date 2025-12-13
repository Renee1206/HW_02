import csv
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties


def get_cjk_font() -> Optional[FontProperties]:
    """
    找一個支援中文的字型，用於「圖上文字」(labels/legend/autopct)。
    不改變文字內容語言，只是讓中文字不變方塊。
    """
    candidates = [
        "Microsoft JhengHei",   # Windows 繁中
        "Microsoft YaHei",      # Windows
        "SimHei",               # Windows
        "PingFang TC",          # macOS
        "Heiti TC",             # macOS
        "Noto Sans CJK TC",     # 跨平台
        "Noto Sans CJK SC",
        "WenQuanYi Zen Hei",    # Linux
        "Arial Unicode MS",
    ]

    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return FontProperties(family=name)

    return None


_CJK_FP = get_cjk_font()


def read_expenses(csv_file: str = "expenses.csv") -> Dict[str, float]:
    category_totals = defaultdict(float)

    try:
        with open(csv_file, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header if present

            for row in reader:
                if len(row) < 3:
                    continue

                amount_str = row[1]
                category = row[2].strip() if row[2] else "Uncategorized"

                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                if amount > 0:
                    category_totals[category] += amount

    except FileNotFoundError:
        return {}

    return dict(category_totals)


def _prepare_data(
    category_totals: Dict[str, float],
    min_pct_for_label: float = 3.0,
    other_threshold_pct: float = 2.0
) -> Tuple[List[str], List[float], float, float]:
    if not category_totals:
        return [], [], 0.0, min_pct_for_label

    items = [(k, v) for k, v in category_totals.items() if v > 0]
    if not items:
        return [], [], 0.0, min_pct_for_label

    items.sort(key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in items)

    labels, sizes = [], []
    other_sum = 0.0

    for k, v in items:
        pct = (v / total) * 100 if total > 0 else 0
        if pct < other_threshold_pct:
            other_sum += v
        else:
            labels.append(k)
            sizes.append(v)

    if other_sum > 0:
        labels.append("Other")
        sizes.append(other_sum)

    return labels, sizes, total, min_pct_for_label


def plot_pie_chart_on_ax(
    category_totals: Dict[str, float],
    ax,
    title: str = "Expenses by Category",
    min_pct_for_label: float = 3.0,
    other_threshold_pct: float = 2.0
):
    ax.clear()
    ax.set_aspect("equal")
    ax.set_facecolor("white")

    labels, sizes, total, min_pct_for_label = _prepare_data(
        category_totals,
        min_pct_for_label=min_pct_for_label,
        other_threshold_pct=other_threshold_pct
    )

    if not labels:
        ax.text(
            0.5, 0.5,
            "No expenses yet.\nAdd a record to see the chart.",
            ha="center", va="center",
            fontsize=12
        )
        ax.set_title(title, pad=14, fontsize=14, fontweight="bold")
        ax.axis("off")
        return

    cmap = plt.get_cmap("tab20")
    colors = [cmap(i % cmap.N) for i in range(len(labels))]

    def autopct_func(pct: float) -> str:
        if pct < min_pct_for_label:
            return ""
        value = (pct / 100.0) * total
        return f"{pct:.1f}%\n${value:,.0f}"

    # 只讓「圖上文字」使用中文字型（如果找得到）
    textprops = {"fontsize": 9}
    if _CJK_FP is not None:
        textprops["fontproperties"] = _CJK_FP

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,                 # labels 可能含中文
        startangle=90,
        counterclock=False,
        colors=colors,
        autopct=autopct_func,          # 百分比/金額
        pctdistance=0.78,
        labeldistance=1.05,
        textprops=textprops,
        wedgeprops={"linewidth": 1.0, "edgecolor": "white"}
    )

    # 甜甜圈中心
    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre_circle)

    ax.text(0, 0.05, "Total", ha="center", va="center", fontsize=10, color="gray")
    ax.text(0, -0.10, f"${total:,.0f}", ha="center", va="center", fontsize=14, fontweight="bold")

    ax.set_title(title, pad=14, fontsize=14, fontweight="bold")

    # legend 也可能出現中文類別 -> 指定 fontproperties
    legend_labels = [f"{lab}  (${val:,.0f})" for lab, val in zip(labels, sizes)]
    legend_kwargs = dict(
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
        fontsize=9,
        title_fontsize=10,
    )
    if _CJK_FP is not None:
        legend_kwargs["prop"] = _CJK_FP

    ax.legend(wedges, legend_labels, **legend_kwargs)

    ax.axis("off")
