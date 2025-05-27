import streamlit as st

def veri_on_izleme(df):
    st.subheader("Veri Önizlemesi")
    st.dataframe(df.head())

    with st.expander(" Temel İstatistikler"):
        st.write(df.describe())