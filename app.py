import streamlit as st
import pandas as pd

# Bu satır Streamlit komutlarından önce, sadece bir kere çağrılmalı
st.set_page_config(page_title="Veri Dashboard", layout="wide")

from components.preview import veri_on_izleme
from components.filter_clean import veri_filtrele_temizle
from components.charts import grafik_olustur
from components.download import veri_ve_grafik_indir

# Uygulama başlığı ve açıklama
st.title(" Interaktif Veri Dashboard")
st.markdown(
    "Hoş geldiniz. Bu platform, verilerinizi hızlı ve güvenli bir şekilde yükleyerek "
    "kapsamlı analizler gerçekleştirmenize ve etkili görselleştirmeler oluşturmanıza olanak tanır."
)

# CSV yükleme alanı
with st.sidebar:
    st.header(" CSV Dosyası Yükle")
    uploaded_file = st.file_uploader("CSV formatında bir dosya yükleyin", type="csv")

# Dosya yüklendiyse ana sekmeleri göster
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    tab1, tab2, tab3, tab4 = st.tabs([
        " Veri Önizleme",
        " Filtreleme",
        " Grafik Oluşturma",
        " İndirme"
    ])

    with tab1:
        veri_on_izleme(df)
    with tab2:
        df = veri_filtrele_temizle(df)
    with tab3:
        grafik_olustur(df)
    with tab4:
        veri_ve_grafik_indir(df)
else:
    st.info("Lütfen bir CSV dosyası yükleyin.")