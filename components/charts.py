import streamlit as st
import plotly.express as px
import pandas as pd

def grafik_olustur(df):
    st.subheader("Grafik Oluştur")

    chart_type = st.selectbox("Grafik Tipi Seçin", ["Bar", "Line", "Scatter", "Pie", "Histogram"])
    st.session_state["chart_type"] = chart_type

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    # Seçime göre kolonlar
    if chart_type == "Pie":
        x_col = st.selectbox("Kategorik Alan (Adlar)", categorical_cols)
        y_col = st.selectbox("Sayısal Alan (Değerler)", numeric_cols)
    elif chart_type == "Histogram":
        x_col = st.selectbox("Histogram için Sayısal Kolon Seçin", numeric_cols)
        y_col = None
    else:
        x_col = st.selectbox("X Ekseni", categorical_cols + numeric_cols)
        y_col = st.selectbox("Y Ekseni", numeric_cols)

    fig = None

    try:
        if chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col, color=x_col)
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col)
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=x_col)
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_col, values=y_col)
        elif chart_type == "Histogram":
            if pd.api.types.is_numeric_dtype(df[x_col]):
                fig = px.histogram(df, x=x_col)
            else:
                st.warning(f"'{x_col}' sütunu sayısal değil. Histogram sadece sayısal verilerle çizilebilir.")

        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.session_state["son_grafik"] = fig
            st.session_state["x_col"] = x_col
            if y_col:
                st.session_state["y_col"] = y_col

    except Exception as e:
        st.warning(f"Grafik oluşturulurken hata oluştu: {e}")