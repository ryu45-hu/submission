import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data
@st.cache_data  # Menggunakan cache untuk menghindari pemuatan ulang yang tidak perlu
def load_data():
    df = pd.read_csv("dashboard/all_data.csv")
    # Pastikan kolom tanggal tidak menyebabkan error dalam analisis numerik
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

df = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Data Bike Sharing")

# Menampilkan informasi dasar
st.subheader("Informasi Dataset")
st.write(f"Jumlah Baris: {df.shape[0]}")
st.write(f"Jumlah Kolom: {df.shape[1]}")
st.write("Ringkasan Statistik:")
st.write(df.describe())

# Menampilkan beberapa data awal
st.subheader("Pratinjau Data")
st.write(df.head())

# Visualisasi Data
st.subheader("Visualisasi Data")

# Pilihan kolom untuk visualisasi
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
if numeric_columns:
    selected_column = st.selectbox("Pilih kolom untuk histogram:", numeric_columns)

    # Histogram
    fig, ax = plt.subplots()
    sns.histplot(df[selected_column], bins=20, kde=True, ax=ax)
    ax.set_title(f'Distribusi {selected_column}')
    st.pyplot(fig)

    # Scatter plot antara dua variabel
    st.subheader("Scatter Plot")
    x_axis = st.selectbox("Pilih variabel X:", numeric_columns, index=0)
    y_axis = st.selectbox("Pilih variabel Y:", numeric_columns, index=1)

    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
    ax.set_title(f'Scatter Plot {x_axis} vs {y_axis}')
    st.pyplot(fig)

    # Korelasi antar variabel numerik
    st.subheader("Heatmap Korelasi")
    fig, ax = plt.subplots(figsize=(10, 8))  # Ukuran heatmap
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    ax.set_title("Korelasi Antar Variabel Numerik")
    sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm", fmt='.2f', ax=ax)
    st.pyplot(fig)
else:
    st.write("Tidak ada kolom numerik yang tersedia untuk divisualisasikan.")

st.write("by: mustolih")
