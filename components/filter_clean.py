import streamlit as st
import pandas as pd
import plotly.express as px

def veri_filtrele_temizle(df):
    st.subheader(" Veri Filtreleme")
    columns = df.columns.tolist()
    selected_col = st.selectbox("Filtrelemek için bir kolon seçin", columns)
    value = st.text_input("Filtre değeri girin")

    if selected_col and value:
        filtered_df = df[df[selected_col].astype(str) == value]
        st.write(filtered_df)

    st.markdown("---")
    st.subheader(" Otomatik Veri Temizleme")

    # Eksik değer analizi ve temizleme
    with st.expander(" Eksik Değer Analizi ve Temizleme"):
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]

        if not missing_cols.empty:
            st.write("Eksik değer içeren sütunlar:")
            st.dataframe(missing_cols)

            fill_option = st.selectbox("Doldurma yöntemi:", ["Ortalama (mean)", "Medyan", "Mod (en sık)"], key="fill_option")

            if st.button("Eksik Değerleri Doldur", key="fill_button"):
                if fill_option == "Ortalama (mean)":
                    df = df.fillna(df.mean(numeric_only=True))
                elif fill_option == "Medyan":
                    df = df.fillna(df.median(numeric_only=True))
                elif fill_option == "Mod (en sık)":
                    df = df.fillna(df.mode().iloc[0])
                st.success("✅ Eksik veriler başarıyla dolduruldu.")

            if st.button("Eksik Satırları Sil", key="drop_button"):
                df = df.dropna()
                st.success("✅ Eksik veriler içeren satırlar silindi.")
        else:
            st.success("✅ Eksik veri bulunmamaktadır.")

    # Aykırı değer analizi ve temizleme
    with st.expander(" Aykırı Değer Analizi ve Temizleme (Boxplot + IQR)"):
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Aykırı kontrol için sayısal kolon seç", numeric_cols, key="iqr_col")
            fig = px.box(df, y=selected_col, points="all")
            st.plotly_chart(fig, use_container_width=True)

            if st.button("Aykırı Değerleri Kaldır (IQR)", key="iqr_button"):
                Q1 = df[selected_col].quantile(0.25)
                Q3 = df[selected_col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                initial = df.shape[0]
                df = df[(df[selected_col] >= lower) & (df[selected_col] <= upper)]
                final = df.shape[0]
                st.success(f"✅ {initial - final} aykırı satır kaldırıldı.")
        else:
            st.warning("Sayısal veri içeren kolon bulunamadı.")

    return df