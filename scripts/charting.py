import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_ranked_bar(df, group_cols, value_col, flag_outliers=True):
    # Aggregate to group level
    grp = df.groupby(group_cols)[value_col].sum().reset_index()

    # IQR flag on the grouped totals
    q1, q3 = grp[value_col].quantile([0.25, 0.75])
    iqr = q3 - q1
    grp["is_outlier"] = (grp[value_col] < q1 - 1.5 * iqr) | (grp[value_col] > q3 + 1.5 * iqr)

    # Label: join the group columns with " | "
    grp["label"] = grp[group_cols].astype(str).agg(" | ".join, axis=1)
    grp = grp.sort_values(value_col)

    if flag_outliers:
        colors = grp["is_outlier"].map({True: "crimson", False: "lightgrey"})
    else:
        colors = "lightgrey"

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(grp["label"], grp[value_col], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"{value_col} by {' × '.join(group_cols)}")
    ax.set_xlabel(f"Total {value_col}")
    plt.tight_layout()
    return fig, ax

def plot_scatter(df, x_col, y_col, flag_col=None):
    if flag_col:
        colors = df[flag_col].map({True: "crimson", False: "lightgrey"})
    else:
        colors = "lightgrey"

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df[x_col], df[y_col], c=colors, alpha=0.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{y_col} vs {x_col}")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.tight_layout()
    return fig, ax

def plot_box(df, value_col, by_col):
    fig, ax = plt.subplots(figsize=(8, 5))
    df.boxplot(column=value_col, by=by_col, ax=ax)
    ax.set_title(f"{value_col} distribution by {by_col}")
    ax.set_xlabel(by_col)
    ax.set_ylabel(value_col)
    fig.suptitle("")   # removes the automatic "grouped by" title
    plt.tight_layout()
    return fig, ax

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Load the file
    df = pd.read_csv("../data/Sample - Superstore.csv", encoding = "latin-1")
    # print("Number of rows: ", len(df))
    # print("Number of columns: ", len(df.columns))
    # print("Columns:", df.columns.to_list())
    # print("The columns are:", df.columns.to_list())
    # print("The shape of the dataset")
    # print(df.shape)

    # Horizontal Bar Plot
    fig_bar, ax_bar = plot_ranked_bar(df, ["Region", "Category"], "Profit")

    # Row-level flag: discount above the upper IQR fence within its own Category
    q1 = df.groupby("Category")["Discount"].transform(lambda s: s.quantile(0.25))
    q3 = df.groupby("Category")["Discount"].transform(lambda s: s.quantile(0.75))
    df["high_discount"] = df["Discount"] > q3 + 1.5 * (q3 - q1)

    # Scatterplot
    fig_sc, ax_sc = plot_scatter(df, "Discount", "Profit", "high_discount")

    # Box
    fig_box, ax_box = plot_box(df, "Discount", "Category")

    fig_bar.savefig("../charts/profit_by_region_category.png", dpi=150)
    fig_sc.savefig("../charts/discount_vs_profit.png", dpi=150)
    fig_box.savefig("../charts/discount_by_category.png", dpi=150)
    # Checks
    # print(df.groupby("Discount")["Profit"].agg(["count", "sum", lambda s: (s < 0).mean()]))

    # print(df[(df["Discount"] >= 0.7) & (~df["high_discount"])].groupby("Category").size())
    # print(df[df["Discount"] >= 0.3]["Profit"].sum())

    # q1 = df.groupby("Category")["Discount"].quantile(0.25)
    # q3 = df.groupby("Category")["Discount"].quantile(0.75)
    # print(q3 + 1.5 * (q3 - q1))

    # print(df[df["high_discount"]].groupby("Category")["Discount"].unique())

    plt.show()