import matplotlib.pyplot as plt
import io

def grafik_png_kaydet(df, chart_type, x_col, y_col=None):
    buf = io.BytesIO()
    plt.figure(figsize=(10, 5))

    if chart_type == "Bar":
        df.groupby(x_col)[y_col].sum().plot(kind="bar")
    elif chart_type == "Line":
        df.sort_values(x_col).plot(x=x_col, y=y_col, kind="line")
    elif chart_type == "Scatter":
        plt.scatter(df[x_col], df[y_col])
    elif chart_type == "Histogram":
        df[x_col].plot(kind="hist", bins=20)
    elif chart_type == "Pie":
        df_grouped = df.groupby(x_col)[y_col].sum()
        df_grouped.plot(kind="pie", autopct='%1.1f%%', ylabel='', legend=False)

    plt.title(f"{x_col} - {y_col if y_col else ''} ({chart_type})")
    plt.xlabel(x_col)
    if y_col:
        plt.ylabel(y_col)
    plt.tight_layout()
    plt.savefig(buf, format="png")
    return buf