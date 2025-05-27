import pandas as pd

def doldur_eksik_veri(df, method="mean"):
    if method == "mean":
        return df.fillna(df.mean(numeric_only=True))
    elif method == "median":
        return df.fillna(df.median(numeric_only=True))
    elif method == "mode":
        return df.fillna(df.mode().iloc[0])
    return df

def sil_eksik_satirlar(df):
    return df.dropna()

def aykirilari_iqr_ile_sil(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df_clean = df[(df[column] >= lower) & (df[column] <= upper)]
    return df_clean