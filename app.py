import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Belediye Bilgi İşlem - Depo Stok Takip",
    page_icon="📦",
    layout="wide",
)

# Depodaki güncel toner ve cihaz listesi (Model ve Renk bazlı)
if "stok" not in st.session_state:
  st.session_state.stok = pd.DataFrame([
      {
          "Malzeme Adı": "UTAX 2507 Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 4,
          "Kritik Sınır": 2,
      },
      {
          "Malzeme Adı": "UTAX 2508 Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 3,
          "Kritik Sınır": 2,
      },
      {
          "Malzeme Adı": "UTAX 3062i Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 2,
          "Kritik Sınır": 2,
      },
      {
          "Malzeme Adı": "UTAX 4035 Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 5,
          "Kritik Sınır": 2,
      },
      {
          "Malzeme Adı": "UTAX 4531 Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 2,
          "Kritik Sınır": 1,
      },
      {
          "Malzeme Adı": "UTAX 4532 Siyah Toner",
          "Kategori": "Toner",
          "Renk": "Siyah",
          "Adet": 3,
          "Kritik Sınır": 1,
      },
      {
          "Malzeme Adı": "UTAX 4532 Mavi (Cyan) Toner",
          "Kategori": "Toner",
          "Renk": "Mavi",
          "Adet": 1,
          "Kritik Sınır": 1,
      },
      {
          "Malzeme Adı": "UTAX 4532 Kırmızı (Magenta) Toner",
          "Kategori": "Toner",
          "Renk": "Kırmızı",
          "Adet": 2,
          "Kritik Sınır": 1,
      },
      {
          "Malzeme Adı": "UTAX 4532 Sarı (Yellow) Toner",
          "Kategori": "Toner",
          "Renk": "Sarı",
          "Adet": 1,
          "Kritik Sınır": 1,
      },
      {
          "Malzeme Adı": "UTAX 2507 Yedek Cihaz",
          "Kategori": "Yedek Cihaz",
          "Renk": "Yok",
          "Adet": 1,
          "Kritik Sınır": 1,
      },
  ])

st.title("📦 Belediye Bilgi İşlem - Depo Toner ve Cihaz Stok Takip Paneli")
st.markdown(
    "Depodaki tüm UTAX toner modellerinin ve renklerinin anlık stok takibi."
)

# Kritik Seviyedeki Ürünleri Kontrol Et ve Uyarı Ver
kritik_urunler = st.session_state.stok[
    st.session_state.stok["Adet"] <= st.session_state.stok["Kritik Sınır"]
]
if not kritik_urunler.empty:
  st.error(
      "🚨 **Kritik Stok Uyarısı!** Aşağıdaki ürünler kritik sınırda veya"
      " tükenmek üzere:"
  )
  for idx, row in kritik_urunler.iterrows():
    st.warning(
        f"⚠️ **{row['Malzeme Adı']}**: Depoda yalnızca **{row['Adet']} adet**"
        f" kaldı!"
    )

st.divider()

# Mevcut Depo Tablosu
st.subheader("📋 Güncel Envanter Listesi")
st.dataframe(st.session_state.stok, use_container_width=True)

st.divider()

# İşlem Alanları (Stok Ekle / Stoktan Düş)
col1, col2 = st.columns(2)

with col1:
  st.subheader("➕ Depoya Ürün Ekle (Giriş)")
  secilen_urun_ekle = st.selectbox(
      "Eklenecek Ürünü Seçin",
      st.session_state.stok["Malzeme Adı"].tolist(),
      key="ekle_select",
  )
  eklenen_adet = st.number_input(
      "Eklenecek Adet", min_value=1, value=1, key="ekle_adet"
  )
  if st.button("Stok Ekle"):
    st.session_state.stok.loc[
        st.session_state.stok["Malzeme Adı"] == secilen_urun_ekle, "Adet"
    ] += eklenen_adet
    st.success("Başarıyla eklendi!")
    st.rerun()

with col2:
  st.subheader("➖ Depodan Ürün Ver (Çıkış / Kullanım)")
  secilen_urun_dus = st.selectbox(
      "Verilecek Ürünü Seçin",
      st.session_state.stok["Malzeme Adı"].tolist(),
      key="dus_select",
  )
  dusulen_adet = st.number_input(
      "Çıkılacak Adet", min_value=1, value=1, key="dus_adet"
  )
  if st.button("Stoktan Düş"):
    mevcut = st.session_state.stok.loc[
        st.session_state.stok["Malzeme Adı"] == secilen_urun_dus, "Adet"
    ].values[0]
    if mevcut >= dusulen_adet:
      st.session_state.stok.loc[
          st.session_state.stok["Malzeme Adı"] == secilen_urun_dus, "Adet"
      ] -= dusulen_adet
      st.success("Stoktan düşüldü!")
      st.rerun()
    else:
      st.error("Hata: Depoda bu kadar ürün yok!")