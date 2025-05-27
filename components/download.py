import streamlit as st
import io
import matplotlib.pyplot as plt
import pandas as pd

def veri_ve_grafik_indir(df):
    st.subheader(" Veriyi ve Grafiği İndirme Sayfası")

    # --- VERİYİ İNDİR ---
    st.markdown("###  Temizlenmiş Veriyi İndir")

    download_format = st.selectbox("Veri indirme formatını seçin", ["CSV", "Excel (.xlsx)", "JSON"], key="data_format")

    if download_format == "CSV":
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=" CSV olarak indir",
            data=csv_data,
            file_name="temizlenmis_veri.csv",
            mime="text/csv"
        )

    elif download_format == "Excel (.xlsx)":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Veri")
            writer.close()
        st.download_button(
            label=" Excel (.xlsx) olarak indir",
            data=output.getvalue(),
            file_name="temizlenmis_veri.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif download_format == "JSON":
        json_data = df.to_json(orient="records", indent=2)
        st.download_button(
            label="📥 JSON olarak indir",
            data=json_data,
            file_name="temizlenmis_veri.json",
            mime="application/json"
        )

    # --- GRAFİĞİ İNDİR ---
    st.markdown("###  Seçilen Grafiği İndir")

    if "son_grafik" in st.session_state and "x_col" in st.session_state:
        fig = st.session_state["son_grafik"]
        st.plotly_chart(fig, use_container_width=True, key="indir_grafik")

        # Matplotlib ile PNG çıktısı
        chart_type = st.session_state.get("chart_type", "")
        x_col = st.session_state.get("x_col")
        y_col = st.session_state.get("y_col", None)

        buf = io.BytesIO()
        plt.figure(figsize=(10, 5))

        try:
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

            st.download_button(
                label=" PNG olarak indir (matplotlib)",
                data=buf.getvalue(),
                file_name="grafik.png",
                mime="image/png"
            )
        except Exception as e:
            st.warning(f"Grafik oluşturulurken hata oluştu: {e}")
    else:
        st.info("Henüz grafik oluşturulmadı. Lütfen önce 'Grafik Oluşturma' sekmesinden bir grafik üretin.")