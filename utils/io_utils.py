import io
import pandas as pd

def veriyi_csv_olarak_indir(df):
    return df.to_csv(index=False).encode("utf-8")

def veriyi_excel_olarak_indir(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Veri")
        writer.close()
    return output.getvalue()

def veriyi_json_olarak_indir(df):
    return df.to_json(orient="records", indent=2)