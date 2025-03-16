import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Data Bike Sharing")

file_path = "dashboard/main_data.csv"
main_data = pd.read_csv(file_path)

main_data["dteday"] = pd.to_datetime(main_data["dteday"], errors='coerce')
main_data = main_data.dropna(subset=["dteday"])

start_date = st.sidebar.date_input("Pilih Tanggal Mulai", main_data["dteday"].min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", main_data["dteday"].max().date())

if start_date > end_date:
    st.error("Tanggal mulai harus sebelum tanggal akhir")
else:
    filtered_data = main_data[(main_data["dteday"] >= pd.to_datetime(start_date)) & 
                              (main_data["dteday"] <= pd.to_datetime(end_date))]

    if filtered_data.empty:
        st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")
    else:
        monthly_average_count = filtered_data.groupby(filtered_data["dteday"].dt.to_period("M"))["cnt"].mean().reset_index()
        monthly_average_count["dteday"] = pd.to_datetime(monthly_average_count["dteday"].dt.to_timestamp())

        monthly_average_temp = filtered_data.groupby(filtered_data["dteday"].dt.to_period("M"))["temp"].mean().reset_index()
        monthly_average_temp["dteday"] = pd.to_datetime(monthly_average_temp["dteday"].dt.to_timestamp())

        monthly_average_count_temp = monthly_average_count.merge(monthly_average_temp, on="dteday", how="left")

        factor_df = filtered_data[["cnt","season", "holiday","weekday","workingday","weathersit","temp","atemp","hum","windspeed"]].dropna()
        correlation_matrix = factor_df.corr()[["cnt"]].drop("cnt")

        st.subheader("Tren Rata-rata Peminjaman Sepeda per Bulan")
        fig1, ax1 = plt.subplots(figsize=(10,6))
        sns.lineplot(data=monthly_average_count, x="dteday", y="cnt", linestyle="-")
        ax1.set_xlabel("Bulan")
        ax1.set_ylabel("Rata-rata Peminjaman")
        ax1.set_title("Tren Rata-rata Peminjaman Sepeda per Bulan")
        plt.grid(linewidth=0.2)
        st.pyplot(fig1)

        st.subheader("Tren Penyewaan Sepeda di Berbagai Jam")
        fig2, ax2 = plt.subplots(figsize=(10,6))
        sns.barplot(data=filtered_data, x="hr", y="cnt", hue="weekday")
        ax2.set_xlabel("Jam")
        ax2.set_ylabel("Jumlah Peminjaman")
        ax2.set_title("Tren Penyewaan Sepeda di Berbagai Jam")
        plt.grid(linewidth=0.2)
        st.pyplot(fig2)

        st.subheader("Korelasi Atribut lain dengan Jumlah Peminjaman Sepeda")
        fig3, ax3 = plt.subplots(figsize=(3, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        ax3.set_title("Korelasi Atribut lain dengan Jumlah Peminjaman Sepeda")
        st.pyplot(fig3)

        st.subheader("Hubungan Antara Rata-rata Peminjaman Sepeda dan Temperatur")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=monthly_average_count_temp, x="dteday", y="cnt", label="cnt")
        sns.lineplot(data=monthly_average_count_temp, x="dteday", y="temp", label="temp")
        ax4.set_title("Hubungan Tren Rata-rata Peminjaman Sepeda dan Temperatur per Bulan")
        ax4.set_xlabel("Tanggal")
        ax4.set_ylabel("Rata-rata Peminjaman")
        ax4.legend()
        plt.grid(linewidth=0.2)
        st.pyplot(fig4)